import asyncio
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums.chat_type import ChatType
from aiogram.exceptions import TelegramForbiddenError

from database.db import Database
from keyboards.game_kb import get_lobby_keyboard, get_night_action_keyboard
from keyboards.vote_kb import get_vote_keyboard
from utils.messages import (
    GAME_STARTED, ROLE_REVEAL,
    NIGHT_FALL, NIGHT_ACTION_REQUIRED, NIGHT_NO_ACTION,
    DAY_BREAK, DAY_BREAK_DEATH,
    VOTE_PHASE, VOTE_RESULTS, VOTE_ELIMINATE,
    GAME_OVER, MAFIA_WIN, TOWN_WIN, NEUTRAL_WIN,
    NOT_ENOUGH_PLAYERS, PLAYER_JOINED,
    ALREADY_IN_GAME, GAME_FULL, NO_ACTIVE_GAME,
    ERROR_OCCURRED, VOTE_CAST, PLAYERS_LIST
)
from utils.game_logic import (
    active_games, game_timers, create_game, join_game, leave_game,
    start_game, start_night, process_night_actions, start_day,
    cast_vote, skip_vote, process_votes, format_vote_results,
    get_alive_players_list, check_win_condition,
    end_game_cleanup, update_player_stats_on_game_end
)
from config import GAME_JOIN_TIME, DAY_DISCUSSION_TIME, VOTE_TIME, NIGHT_ACTION_TIME, MIN_PLAYERS, MAX_PLAYERS

router = Router()
db = Database()
logger = logging.getLogger(__name__)


@router.message(Command("startgame"))
async def cmd_startgame(message: Message):
    """O'yin boshlash (faqat guruhda)"""
    chat = message.chat
    if chat.type == ChatType.PRIVATE:
        await message.answer("❌ Bu buyruq faqat guruhda ishlaydi.")
        return

    member = await chat.get_member(message.from_user.id)
    if member.status not in ("creator", "administrator"):
        await message.answer("❌ Faqat guruh adminlari o'yin boshlay oladi.")
        return

    existing = await db.get_active_game(chat.id)
    if existing:
        await message.answer("❌ Bu chatda allaqachon faol o'yin bor!")
        return

    try:
        game_id = await create_game(chat.id)
    except Exception as e:
        logger.error(f"O'yin yaratishda xatolik: {e}")
        await message.answer(ERROR_OCCURRED)
        return

    game = active_games[game_id]
    game["chat_id"] = chat.id
    game["message_id"] = message.message_id

    text = GAME_STARTED.format(time=GAME_JOIN_TIME, count=0, players="Hali hech kim yo'q")
    msg = await message.answer(text, reply_markup=get_lobby_keyboard(game_id, 0), parse_mode="Markdown")
    game["lobby_message_id"] = msg.message_id

    task = asyncio.create_task(lobby_timer(game_id, chat.id))
    game_timers[game_id] = task


async def lobby_timer(game_id: int, chat_id: int):
    """Lobby taymerini boshqaradi"""
    try:
        await asyncio.sleep(GAME_JOIN_TIME)

        game = active_games.get(game_id)
        if not game or game["phase"] != "lobby":
            return

        player_count = len(game["players"])
        if player_count < MIN_PLAYERS:
            from aiogram import Bot
            from config import BOT_TOKEN
            bot = Bot(token=BOT_TOKEN)
            await bot.send_message(
                chat_id,
                NOT_ENOUGH_PLAYERS.format(min_players=MIN_PLAYERS, count=player_count),
                parse_mode="Markdown"
            )
            await end_game_cleanup(game_id)
            await bot.session.close()
            return

        await force_start_game(game_id, chat_id)

    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.error(f"Lobby taymerida xatolik: {e}")


@router.message(Command("forcestart"))
async def cmd_forcestart(message: Message):
    """Majburiy start"""
    chat = message.chat
    if chat.type == ChatType.PRIVATE:
        await message.answer("❌ Bu buyruq faqat guruhda ishlaydi.")
        return

    member = await chat.get_member(message.from_user.id)
    if member.status not in ("creator", "administrator"):
        await message.answer("❌ Faqat guruh adminlari majburiy start qila oladi.")
        return

    game_data = await db.get_active_game(chat.id)
    if not game_data:
        await message.answer(NO_ACTIVE_GAME)
        return

    game_id = game_data["game_id"]
    game = active_games.get(game_id)
    if not game or game["phase"] != "lobby":
        await message.answer("❌ O'yin lobbi bosqichida emas.")
        return

    player_count = len(game["players"])
    if player_count < MIN_PLAYERS:
        await message.answer(NOT_ENOUGH_PLAYERS.format(min_players=MIN_PLAYERS, count=player_count))
        return

    task = game_timers.pop(game_id, None)
    if task:
        task.cancel()

    await message.answer("⏩ **Majburiy start!** O'yin boshlanmoqda...", parse_mode="Markdown")
    await force_start_game(game_id, chat.id)


async def force_start_game(game_id: int, chat_id: int):
    """O'yinni majburiy boshlash"""
    from aiogram import Bot
    from config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)

    success = await start_game(game_id)
    if not success:
        await bot.send_message(chat_id, ERROR_OCCURRED, parse_mode="Markdown")
        await bot.session.close()
        return

    game = active_games[game_id]

    try:
        await bot.edit_message_reply_markup(chat_id, game.get("lobby_message_id"), reply_markup=None)
    except Exception:
        pass

    # Rollarni yuborish
    for user_id, player in game["players"].items():
        role = player["role"]
        if role:
            try:
                action_info = "Kechasi harakat qilishingiz kerak!" if role.night_action else "Passiv rol, kechasi uxlaysiz."
                await bot.send_message(
                    user_id,
                    ROLE_REVEAL.format(
                        role_info=role.full_name(),
                        role_full=role.full_name(),
                        description=role.description,
                        action_info=action_info,
                    ),
                    parse_mode="Markdown"
                )
            except TelegramForbiddenError:
                logger.warning(f"Foydalanuvchi {user_id} botni bloklagan")
            except Exception as e:
                logger.error(f"Rol yuborishda xatolik {user_id}: {e}")

    await bot.send_message(chat_id, "🎯 **O'YIN BOSHLANDI!** Rollar tarqatildi. Shaxsiy xabarlaringizni tekshiring.", parse_mode="Markdown")

    # Birinchi kechani boshlash va kecha harakatlarini yuborish
    await start_night(game_id)
    await bot.send_message(chat_id, NIGHT_FALL.format(night_count=1), parse_mode="Markdown")
    await send_night_actions(game_id, bot)

    # Kechadan keyin kunduzgi fazaga o'tish
    await send_day_phase(game_id)

    await bot.session.close()


@router.callback_query(F.data.startswith("join:"))
async def handle_join(callback: CallbackQuery):
    """O'yinga qo'shilish"""
    game_id = int(callback.data.split(":")[1])
    user = callback.from_user
    game = active_games.get(game_id)

    if not game or game["phase"] != "lobby":
        await callback.answer("❌ O'yin topilmadi yoki boshlanib ketgan.", show_alert=True)
        return

    if user.id in game["players"]:
        await callback.answer(ALREADY_IN_GAME, show_alert=True)
        return

    if len(game["players"]) >= MAX_PLAYERS:
        await callback.answer(GAME_FULL.format(max=MAX_PLAYERS), show_alert=True)
        return

    name = user.first_name or user.username or f"ID{user.id}"
    success = await join_game(game_id, user.id, name)

    if success:
        await callback.answer(f"✅ O'yinga qo'shildingiz!", show_alert=False)
        await update_lobby_message(game_id)
    else:
        await callback.answer("❌ Qo'shilishda xatolik.", show_alert=True)


@router.callback_query(F.data.startswith("leave:"))
async def handle_leave(callback: CallbackQuery):
    """O'yinni tark etish"""
    game_id = int(callback.data.split(":")[1])
    user = callback.from_user
    game = active_games.get(game_id)

    if not game:
        await callback.answer(NO_ACTIVE_GAME, show_alert=True)
        return

    success = await leave_game(game_id, user.id)
    if success:
        await callback.answer("✅ O'yinni tark etdingiz.", show_alert=False)
        await update_lobby_message(game_id)
    else:
        await callback.answer("❌ Siz o'yinda emassiz.", show_alert=True)


async def update_lobby_message(game_id: int):
    """Lobby xabarini yangilaydi"""
    from aiogram import Bot
    from config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)

    game = active_games.get(game_id)
    if not game or game["phase"] != "lobby":
        await bot.session.close()
        return

    players_list = "\n".join([
        f"👤 {p['name']}" for p in game["players"].values()
    ]) if game["players"] else "Hali hech kim yo'q"

    text = GAME_STARTED.format(
        time=GAME_JOIN_TIME,
        count=len(game["players"]),
        players=players_list
    )

    try:
        await bot.edit_message_text(
            text,
            chat_id=game["chat_id"],
            message_id=game["lobby_message_id"],
            reply_markup=get_lobby_keyboard(game_id, len(game["players"])),
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Lobby xabarini yangilashda xatolik: {e}")

    await bot.session.close()


async def send_night_actions(game_id: int, bot):
    """Kecha harakatlarini yuboradi va 30 soniya kutadi"""
    game = active_games.get(game_id)
    if not game:
        return

    alive_players = [p for p in game["players"].values() if p["alive"]]

    for player in alive_players:
        role = player.get("role")
        if not role:
            continue

        try:
            if role.night_action:
                targets = [p for p in alive_players if p["user_id"] != player["user_id"]]
                if targets:
                    await bot.send_message(
                        player["user_id"],
                        NIGHT_ACTION_REQUIRED.format(
                            role_full=role.full_name(),
                            description=role.description
                        ),
                        reply_markup=get_night_action_keyboard(game_id, targets, role.action_type),
                        parse_mode="Markdown"
                    )
                else:
                    await bot.send_message(
                        player["user_id"],
                        NIGHT_NO_ACTION,
                        parse_mode="Markdown"
                    )
            else:
                await bot.send_message(
                    player["user_id"],
                    NIGHT_NO_ACTION,
                    parse_mode="Markdown"
                )
        except TelegramForbiddenError:
            logger.warning(f"Foydalanuvchi {player['user_id']} botni bloklagan")
        except Exception as e:
            logger.error(f"Kecha harakati yuborishda xatolik: {e}")

    # 30 soniya kutish (kecha harakatlari uchun)
    await asyncio.sleep(NIGHT_ACTION_TIME)


async def send_day_phase(game_id: int):
    """Kunduzgi fazani yuboradi"""
    from aiogram import Bot
    from config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)

    game = active_games.get(game_id)
    if not game:
        await bot.session.close()
        return

    chat_id = game["chat_id"]

    deaths = await process_night_actions(game_id)
    death_text = await start_day(game_id, deaths)

    if death_text == "game_over":
        await bot.session.close()
        return

    if deaths:
        victims = []
        for uid in deaths:
            p = game["players"].get(uid)
            if p:
                victims.append(p["name"])

        msg = DAY_BREAK_DEATH.format(
            night_count=game["night_count"],
            victim=", ".join(victims),
            death_reason=death_text
        )
    else:
        msg = DAY_BREAK.format(night_count=game["night_count"])

    await bot.send_message(chat_id, msg, parse_mode="Markdown")

    # 5 daqiqa muhokama
    await asyncio.sleep(DAY_DISCUSSION_TIME)

    # Ovoz berish fazasi
    game = active_games.get(game_id)
    if not game or game["phase"] != "day":
        await bot.session.close()
        return

    await start_voting_phase(game_id, bot)


async def start_voting_phase(game_id: int, bot):
    """Ovoz berish fazasini boshlaydi"""
    game = active_games.get(game_id)
    if not game:
        return

    game["phase"] = "voting"
    game["vote_counts"] = {}
    game["votes_cast"] = set()

    db = Database()
    await db.update_game_status(game_id, "active", "voting")

    chat_id = game["chat_id"]
    alive_players = get_alive_players_list(game_id)

    msg = VOTE_PHASE.format(time=VOTE_TIME)
    await bot.send_message(chat_id, msg, parse_mode="Markdown")

    for player in alive_players:
        try:
            await bot.send_message(
                player["user_id"],
                "🗳 **Ovoz berish vaqti!** Kim chiqarilishini tanlang:",
                reply_markup=get_vote_keyboard(game_id, alive_players, player["user_id"]),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ovoz berish xabarini yuborishda xatolik: {e}")

    await asyncio.sleep(VOTE_TIME)

    await process_vote_results(game_id, bot)


async def process_vote_results(game_id: int, bot):
    """Ovoz natijalarini hisoblaydi va e'lon qiladi"""
    game = active_games.get(game_id)
    if not game:
        return

    chat_id = game["chat_id"]
    result = await process_votes(game_id)

    if result and result.get("eliminated"):
        eliminated = result["player"]

        vote_details = format_vote_results(game_id)
        await bot.send_message(
            chat_id,
            VOTE_RESULTS.format(
                vote_details=vote_details,
                JUDGEMENT=""
            ),
            parse_mode="Markdown"
        )

        role_short = eliminated["role"].short_name() if eliminated.get("role") else "?"
        await bot.send_message(
            chat_id,
            VOTE_ELIMINATE.format(
                player=eliminated["name"],
                role_full=role_short,
                death_story=f"{eliminated['name']} o'yindan chiqarildi!"
            ),
            parse_mode="Markdown"
        )

        winner = await check_win_condition(game_id)
        if winner:
            await end_game_procedure(game_id, winner, bot)
            await bot.session.close()
            return
    else:
        await bot.send_message(
            chat_id,
            VOTE_RESULTS.format(
                vote_details="Hech kim yetarli ovoz olmadi.",
                JUDGEMENT="⏭ Hech kim chiqarilmaydi."
            ),
            parse_mode="Markdown"
        )

    # Keyingi kechani boshlash
    night = game["night_count"] + 1
    await bot.send_message(chat_id, NIGHT_FALL.format(night_count=night), parse_mode="Markdown")

    await start_night(game_id)
    # Kecha harakatlarini yuborish va kutish
    await send_night_actions(game_id, bot)
    # Keyin kunduzgi faza
    await send_day_phase(game_id)

    await bot.session.close()


async def end_game_procedure(game_id: int, winner: str, bot):
    """O'yin tugash jarayoni"""
    game = active_games.get(game_id)
    if not game:
        return

    chat_id = game["chat_id"]

    result_texts = {
        "mafia": MAFIA_WIN,
        "town": TOWN_WIN,
        "neutral": NEUTRAL_WIN,
    }
    result_text = result_texts.get(winner, "O'yin tugadi!")

    # O'yinchilar statistikasini yangilash
    await update_player_stats_on_game_end(game_id, winner)

    # Barcha rollarni ko'rsatish
    all_roles = []
    for uid, p in game["players"].items():
        status = "✅" if p["alive"] else "💀"
        role_name = p["role"].short_name() if p.get("role") else "?"
        all_roles.append(f"{status} {p['name']} — {role_name}")

    await bot.send_message(
        chat_id,
        GAME_OVER.format(
            GAME_RESULT=result_text,
            all_roles="\n".join(all_roles),
            total_players=len(game["players"]),
            nights=game["night_count"]
        ),
        parse_mode="Markdown"
    )

    await end_game_cleanup(game_id)


# === Callback handlers ===

@router.callback_query(F.data.startswith("vote:"))
async def handle_vote(callback: CallbackQuery):
    """Ovoz berish callback'i"""
    parts = callback.data.split(":")
    if len(parts) < 3:
        await callback.answer("❌ Xatolik yuz berdi.", show_alert=True)
        return

    game_id = int(parts[1])
    target_id = int(parts[2])
    voter_id = callback.from_user.id

    success = await cast_vote(game_id, voter_id, target_id)

    if success:
        await callback.answer(VOTE_CAST, show_alert=True)
        try:
            await callback.message.edit_text("✅ **Ovozingiz qabul qilindi!** Natijalarni kuting.", parse_mode="Markdown")
        except Exception:
            pass
    else:
        await callback.answer("❌ Ovoz berishda xatolik. Allaqachon ovoz bergansiz yoki o'yinda emassiz.", show_alert=True)


@router.callback_query(F.data.startswith("vote_skip:"))
async def handle_vote_skip(callback: CallbackQuery):
    """Ovozni o'tkazib yuborish"""
    parts = callback.data.split(":")
    if len(parts) < 2:
        await callback.answer("❌ Xatolik.", show_alert=True)
        return

    game_id = int(parts[1])
    voter_id = callback.from_user.id

    success = await skip_vote(game_id, voter_id)
    if success:
        await callback.answer("⏭ Ovoz o'tkazib yuborildi.", show_alert=True)
        try:
            await callback.message.edit_text("⏭ **Ovoz o'tkazib yuborildi.**", parse_mode="Markdown")
        except Exception:
            pass
    else:
        await callback.answer("❌ Xatolik yuz berdi.", show_alert=True)


@router.callback_query(F.data == "vote:continue")
async def handle_vote_continue(callback: CallbackQuery):
    """Ovoz natijalaridan keyin davom etish"""
    await callback.answer("⏭ Davom etilmoqda...", show_alert=False)
    try:
        await callback.message.delete()
    except Exception:
        pass


@router.callback_query(F.data.startswith("night_action:"))
async def handle_night_action(callback: CallbackQuery):
    """Kecha harakati callback'i"""
    parts = callback.data.split(":")
    if len(parts) < 4:
        await callback.answer("❌ Xatolik.", show_alert=True)
        return

    game_id = int(parts[1])
    action_type = parts[2]
    target_id = int(parts[3])
    user_id = callback.from_user.id

    game = active_games.get(game_id)
    if not game:
        await callback.answer(NO_ACTIVE_GAME, show_alert=True)
        return

    if game["phase"] != "night":
        await callback.answer("❌ Hozir kecha fazasi emas.", show_alert=True)
        return

    await db.save_night_action(game_id, game["night_count"], user_id, action_type, target_id)

    if action_type == "mafia_kill":
        game["mafia_kill_target"] = target_id

    await callback.answer("✅ Harakatingiz qabul qilindi!", show_alert=True)

    try:
        await callback.message.edit_text(
            "✅ **Harakatingiz qabul qilindi!** Ertalab natijalarni kuting.",
            parse_mode="Markdown"
        )
    except Exception:
        pass


@router.callback_query(F.data.startswith("night_skip:"))
async def handle_night_skip(callback: CallbackQuery):
    """Kecha harakatini o'tkazib yuborish"""
    await callback.answer("⏭ Harakat o'tkazib yuborildi.", show_alert=True)
    try:
        await callback.message.edit_text(
            "⏭ **Harakat o'tkazib yuborildi.**",
            parse_mode="Markdown"
        )
    except Exception:
        pass


# === Group commands ===

@router.message(Command("players"))
async def cmd_players(message: Message):
    """O'yinchilar ro'yxati"""
    chat = message.chat
    if chat.type == ChatType.PRIVATE:
        await message.answer("❌ Bu buyruq faqat guruhda ishlaydi.")
        return

    game_data = await db.get_active_game(chat.id)
    if not game_data:
        await message.answer(NO_ACTIVE_GAME)
        return

    game = active_games.get(game_data["game_id"])
    if not game:
        await message.answer(NO_ACTIVE_GAME)
        return

    players = [
        f"{'✅' if p['alive'] else '💀'} {p.get('name', f'ID{uid}')}"
        for uid, p in game["players"].items()
    ]

    text = PLAYERS_LIST.format(players="\n".join(players)) if players else "👥 Hali hech kim yo'q"
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """O'yin statistikasi"""
    chat = message.chat
    if chat.type == ChatType.PRIVATE:
        await message.answer("❌ Bu buyruq faqat guruhda ishlaydi.")
        return

    game_data = await db.get_active_game(chat.id)
    if not game_data:
        await message.answer(NO_ACTIVE_GAME)
        return

    game = active_games.get(game_data["game_id"])
    if not game:
        await message.answer(NO_ACTIVE_GAME)
        return

    alive_list = []
    dead_list = []

    for uid, p in game["players"].items():
        name = p.get("name", f"ID{uid}")
        role_name = p["role"].short_name() if p.get("role") else "?"
        entry = f"{role_name} — {name}"
        if p["alive"]:
            alive_list.append(entry)
        else:
            dead_list.append(entry)

    events = await db.get_events(game_data["game_id"])
    event_text = "\n".join(f"• {e['description']}" for e in events[-5:]) or "Hodisalar yo'q"

    text = f"""
📊 **O'YIN STATISTIKASI**

🎭 Rollar: {', '.join(p['role'].short_name() for p in game['players'].values() if p.get('role'))}

📅 Hodisalar:
{event_text}

👥 Tirik: {len(alive_list)}
{chr(10).join(alive_list) if alive_list else '—'}

💀 O'lgan: {len(dead_list)}
{chr(10).join(dead_list) if dead_list else '—'}
"""
    await message.answer(text, parse_mode="Markdown")
