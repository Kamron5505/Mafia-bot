import asyncio
import random
import logging
from typing import Dict, Optional, List, Any, Set

from database.db import Database
from utils.messages import DEATH_STORIES
from utils.role_selector import select_roles, get_role_by_name
from roles.base_role import BaseRole

logger = logging.getLogger(__name__)

# Global game state (in-memory)
active_games: Dict[int, Dict[str, Any]] = {}
game_timers: Dict[int, asyncio.Task] = {}


async def create_game(chat_id: int) -> int:
    """Yangi o'yin yaratadi va DB ga saqlaydi"""
    db = Database()
    game_id = await db.create_game(chat_id)
    active_games[game_id] = {
        "game_id": game_id,
        "chat_id": chat_id,
        "players": {},
        "phase": "lobby",
        "night_count": 0,
        "roles": [],
        "vote_counts": {},
        "votes_cast": set(),
        "mafia_kill_target": None,
        "healed_target": None,
        "lobby_message_id": None,
        "message_id": None,
    }
    return game_id


async def join_game(game_id: int, user_id: int, name: str) -> bool:
    """O'yinchini o'yinga qo'shadi"""
    game = active_games.get(game_id)
    if not game:
        return False
    if game["phase"] != "lobby":
        return False
    if len(game["players"]) >= 30:
        return False
    if user_id in game["players"]:
        return False

    game["players"][user_id] = {
        "user_id": user_id,
        "name": name,
        "alive": True,
        "has_voted": False,
        "vote_target": None,
        "role": None,
    }

    db = Database()
    await db.add_player_to_game(game_id, user_id)
    return True


async def leave_game(game_id: int, user_id: int) -> bool:
    """O'yinchini o'yindan chiqaradi"""
    game = active_games.get(game_id)
    if not game:
        return False
    if user_id not in game["players"]:
        return False
    if game["phase"] != "lobby":
        return False

    del game["players"][user_id]
    return True


async def start_game(game_id: int) -> bool:
    """O'yinni boshlaydi va rollarni taqsimlaydi"""
    game = active_games.get(game_id)
    if not game:
        return False

    player_count = len(game["players"])
    if player_count < 6:
        return False

    # Rollarni tanlash
    roles = select_roles(player_count)
    game["roles"] = roles

    # Rollarni o'yinchilarga taqsimlash
    player_ids = list(game["players"].keys())
    random.shuffle(player_ids)

    db = Database()

    for i, user_id in enumerate(player_ids):
        if i < len(roles):
            role = roles[i]
        else:
            role = get_role_by_name("Dengizchi")

        game["players"][user_id]["role"] = role

        await db.add_player_to_game(
            game_id, user_id,
            role_name=role.name,
            role_title=role.title,
            team=role.team
        )

    game["phase"] = "night"
    game["night_count"] = 0
    await db.update_game_status(game_id, "active", "night")
    await db.record_event(game_id, "game_start", f"O'yin boshlandi. {player_count} o'yinchi.")

    return True


async def start_night(game_id: int) -> None:
    """Kecha fazasini boshlaydi"""
    game = active_games.get(game_id)
    if not game:
        return

    game["night_count"] += 1
    game["phase"] = "night"
    game["mafia_kill_target"] = None
    game["healed_target"] = None

    db = Database()
    await db.update_game_status(game_id, "active", "night")
    await db.record_event(game_id, "night_start", f"{game['night_count']}-kecha boshlandi.")


async def process_night_actions(game_id: int) -> Dict[int, str]:
    """
    Kecha harakatlarini qayta ishlaydi va o'lganlarni aniqlaydi.
    
    Harakatlar tartibi:
    1. Bloklash (hook)
    2. Himoya (bodyguard, jail, give_armor)
    3. Davolash (heal)
    4. Hujum (mafia_kill, serial_kill, demon_kill)
    5. Zaharlash (poison)
    6. Tekshiruv (investigate)
    """
    game = active_games.get(game_id)
    if not game:
        return {}

    db = Database()
    night = game["night_count"]
    deaths: Dict[int, str] = {}

    # 1. Kecha harakatlarini yig'ish
    night_actions = await db.get_night_actions(game_id, night)

    # Yig'ilgan harakatlar
    mafia_kills: Set[int] = set()
    blocked_players: Set[int] = set()
    healed_players: Set[int] = set()
    protected_players: Set[int] = set()
    poisoned_players: Dict[int, str] = {}
    solo_kills: Dict[int, str] = {}

    for action in night_actions:
        action_type = action["action_type"]
        user_id = action["user_id"]
        target_id = action["target_id"]

        if target_id is None:
            await db.resolve_night_action(action["id"])
            continue

        role = game["players"].get(user_id, {}).get("role")
        if not role:
            await db.resolve_night_action(action["id"])
            continue

        # Harakatlarni kategoriya bo'yicha yig'ish
        if action_type == "mafia_kill":
            mafia_kills.add(target_id)
        elif action_type in ("serial_kill", "demon_kill"):
            solo_kills[target_id] = "🌪 Manyak" if action_type == "serial_kill" else "🐙 Kraken"
        elif action_type == "heal":
            healed_players.add(target_id)
            game["healed_target"] = target_id
        elif action_type == "hook":
            blocked_players.add(target_id)
        elif action_type == "bodyguard":
            protected_players.add(target_id)
        elif action_type == "poison":
            poisoned_players[target_id] = "🧪 Zaharlangan"
        elif action_type == "jail":
            protected_players.add(target_id)
            blocked_players.add(target_id)  # Qamoqqa olingan harakat qila olmaydi
        elif action_type == "give_armor":
            protected_players.add(target_id)

        await db.resolve_night_action(action["id"])

    # 2. Bloklangan o'yinchilarni tekshirish
    for blocked_id in blocked_players:
        if blocked_id in mafia_kills:
            mafia_kills.remove(blocked_id)

    # 3. Himoya va davolashni qo'llash
    for heal_id in healed_players:
        if heal_id in mafia_kills:
            mafia_kills.remove(heal_id)
        if heal_id in solo_kills:
            del solo_kills[heal_id]

    for protect_id in protected_players:
        if protect_id in mafia_kills:
            mafia_kills.remove(protect_id)
        if protect_id in solo_kills:
            del solo_kills[protect_id]

    # 4. O'limlarni hisoblash
    for target_id in mafia_kills:
        deaths[target_id] = "🦈 Mafiya tomonidan o'ldirildi"

    for target_id, killer in solo_kills.items():
        deaths[target_id] = f"{killer} tomonidan o'ldirildi"

    for target_id, reason in poisoned_players.items():
        deaths[target_id] = reason

    # 5. O'lganlarni belgilash
    for user_id in list(deaths.keys()):
        if user_id in game["players"] and game["players"][user_id]["alive"]:
            game["players"][user_id]["alive"] = False
            await db.kill_player(game_id, user_id)

    return deaths


async def start_day(game_id: int, deaths: Dict[int, str]) -> str:
    """Kunduzgi fazani boshlaydi"""
    game = active_games.get(game_id)
    if not game:
        return ""

    game["phase"] = "day"
    game["vote_counts"] = {}
    game["votes_cast"] = set()

    db = Database()
    await db.update_game_status(game_id, "active", "day")
    await db.reset_votes(game_id)

    if deaths:
        death_texts = []
        for uid, reason in deaths.items():
            player = game["players"].get(uid)
            if player:
                story = random.choice(DEATH_STORIES).format(player=player["name"])
                role_display = player['role'].short_name() if player['role'] else "Noma'lum"
                death_texts.append(
                    f"☠️ {player['name']} halok bo'ldi!\n"
                    f"🎭 Rol: {role_display}\n"
                    f"{reason}\n\n{story}"
                )
                await db.record_event(
                    game_id, "death",
                    f"{player['name']} ({player['role'].short_name() if player['role'] else '?'}) halok bo'ldi: {reason}"
                )

        winner = await check_win_condition(game_id)
        if winner:
            return "game_over"

        return "\n\n".join(death_texts)
    else:
        await db.record_event(game_id, "day_start", f"{game['night_count']}-kecha hech kim o'lmadi.")
        return ""


async def cast_vote(game_id: int, voter_id: int, target_id: int) -> bool:
    """Ovoz berish"""
    game = active_games.get(game_id)
    if not game:
        return False

    if game["phase"] != "voting":
        return False
    if voter_id not in game["players"]:
        return False
    if not game["players"][voter_id]["alive"]:
        return False
    if voter_id in game["votes_cast"]:
        return False

    game["votes_cast"].add(voter_id)

    if target_id == 0:
        game["players"][voter_id]["has_voted"] = True
        game["players"][voter_id]["vote_target"] = None
    else:
        game["players"][voter_id]["has_voted"] = True
        game["players"][voter_id]["vote_target"] = target_id
        game["vote_counts"][target_id] = game["vote_counts"].get(target_id, 0) + 1

    db = Database()
    await db.set_vote(game_id, voter_id, target_id)
    return True


async def skip_vote(game_id: int, voter_id: int) -> bool:
    """Ovozni o'tkazib yuborish"""
    game = active_games.get(game_id)
    if not game:
        return False
    if game["phase"] != "voting":
        return False
    if voter_id not in game["players"]:
        return False
    if not game["players"][voter_id]["alive"]:
        return False
    if voter_id in game["votes_cast"]:
        return False

    game["votes_cast"].add(voter_id)
    game["players"][voter_id]["has_voted"] = True
    game["players"][voter_id]["vote_target"] = None
    return True


async def process_votes(game_id: int) -> Optional[Dict]:
    """Ovoz natijalarini hisoblaydi"""
    game = active_games.get(game_id)
    if not game:
        return None

    alive_players = {uid: p for uid, p in game["players"].items() if p["alive"]}
    total_alive = len(alive_players)
    needed_votes = total_alive // 2 + 1

    vote_counts = game["vote_counts"]

    if not vote_counts:
        return {"eliminated": None, "tied": False, "details": "Hech kim ovoz bermadi."}

    max_votes = max(vote_counts.values())
    top_candidates = [uid for uid, count in vote_counts.items() if count == max_votes]

    if len(top_candidates) > 1 or max_votes < needed_votes:
        return {"eliminated": None, "tied": True, "details": "Ovozlar teng yoki yetarli emas."}

    eliminated_id = top_candidates[0]
    eliminated = game["players"].get(eliminated_id)

    if eliminated:
        eliminated["alive"] = False
        db = Database()
        await db.kill_player(game_id, eliminated_id)
        await db.record_event(
            game_id, "elimination",
            f"{eliminated['name']} ({eliminated['role'].short_name() if eliminated['role'] else '?'}) ovoz berish orqali chiqarildi."
        )

        # Bombachi tekshiruvi
        if eliminated.get("role") and eliminated["role"].name == "Bombachi":
            alive = [uid for uid, p in game["players"].items() if p["alive"] and uid != eliminated_id]
            if alive:
                bomb_victim = random.choice(alive)
                game["players"][bomb_victim]["alive"] = False
                await db.kill_player(game_id, bomb_victim)
                await db.record_event(
                    game_id, "bomb",
                    f"{eliminated['name']} portladi va {game['players'][bomb_victim]['name']} ni o'ldirdi!"
                )

        return {"eliminated": eliminated_id, "player": eliminated, "tied": False}

    return {"eliminated": None, "tied": False, "details": "Xatolik yuz berdi."}


async def check_win_condition(game_id: int) -> Optional[str]:
    """G'alaba shartini tekshiradi"""
    game = active_games.get(game_id)
    if not game:
        return None

    alive_players = {uid: p for uid, p in game["players"].items() if p["alive"]}
    total_alive = len(alive_players)

    mafia_count = sum(1 for p in alive_players.values() if p.get("role") and p["role"].team == "mafia")
    town_count = sum(1 for p in alive_players.values() if p.get("role") and p["role"].team == "town")
    neutral_count = sum(1 for p in alive_players.values() if p.get("role") and p["role"].team == "neutral")

    # Mafiya g'alabasi
    if mafia_count >= town_count and mafia_count > 0:
        return "mafia"

    # Shahar g'alabasi
    if mafia_count == 0 and total_alive > 0:
        if neutral_count == total_alive and neutral_count > 0:
            return "neutral"
        return "town"

    # Neytral g'alabasi
    if neutral_count == total_alive and total_alive > 0:
        return "neutral"

    return None


def format_vote_results(game_id: int) -> str:
    """Ovoz natijalarini formatlaydi"""
    game = active_games.get(game_id)
    if not game:
        return ""

    details = []
    for uid, count in game.get("vote_counts", {}).items():
        player = game["players"].get(uid)
        if player:
            details.append(f"{player['name']}: {count} ovoz")

    return "\n".join(details) if details else "Ovozlar yo'q."


def get_alive_players_list(game_id: int) -> List[Dict]:
    """Tirik o'yinchilar ro'yxati"""
    game = active_games.get(game_id)
    if not game:
        return []
    return [p for uid, p in game["players"].items() if p["alive"]]


def get_all_players_list(game_id: int) -> List[Dict]:
    """Barcha o'yinchilar ro'yxati"""
    game = active_games.get(game_id)
    if not game:
        return []
    return list(game["players"].values())


def get_game_stats_summary(game_id: int) -> str:
    """O'yin statistikasini qaytaradi"""
    game = active_games.get(game_id)
    if not game:
        return ""

    lines = []
    for uid, p in game["players"].items():
        status = "✅" if p["alive"] else "💀"
        role_name = p["role"].short_name() if p["role"] else "?"
        lines.append(f"{status} {p['name']} — {role_name}")

    return "\n".join(lines)


async def end_game_cleanup(game_id: int):
    """O'yinni tozalash va DB yangilash"""
    game = active_games.pop(game_id, None)
    if game:
        db = Database()
        await db.end_game(game_id)
        game_timers.pop(game_id, None)


async def update_player_stats_on_game_end(game_id: int, winner: str):
    """O'yin tugaganda barcha o'yinchilarning statistikasini yangilaydi"""
    game = active_games.get(game_id)
    if not game:
        return

    db = Database()
    for uid, player in game["players"].items():
        role = player.get("role")
        if not role:
            continue

        won = False
        if winner == "mafia" and role.team == "mafia":
            won = True
        elif winner == "town" and role.team == "town":
            won = True
        elif winner == "neutral" and role.team == "neutral":
            won = True

        await db.update_player_stats(
            uid,
            won=won,
            role_team=role.team,
            role_name=role.title
        )

        # Yutuqlarni tekshirish
        player_db = await db.get_player(uid)
        if player_db:
            games = (player_db["games_played"] or 0) + 1
            wins = player_db["wins"] or 0
            if won:
                if wins == 0 and games == 1:
                    await db.add_achievement(uid, "🎯 Birinchi g'alaba")
                if games == 10:
                    await db.add_achievement(uid, "🔱 10 ta o'yin")
