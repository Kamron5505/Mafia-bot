from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.db import Database
from utils.messages import GAME_STATS
from utils.state import active_games

router = Router()
db = Database()


@router.message(Command("endgame"))
async def cmd_endgame(message: Message):
    chat = message.chat
    if chat.type == "private":
        await message.answer("❌ Bu buyruq faqat guruhda ishlaydi.")
        return

    member = await chat.get_member(message.from_user.id)
    if member.status not in ("creator", "administrator"):
        await message.answer("❌ Faqat guruh adminlari o'yinni tugata oladi.")
        return

    game_id = None
    for gid, g in active_games.items():
        if g.get("chat_id") == chat.id and g["phase"] != "ended":
            game_id = gid
            break

    if not game_id:
        await message.answer("❌ Faol o'yin topilmadi.")
        return

    await db.end_game(game_id)
    game = active_games.pop(game_id, None)

    if game:
        from utils.state import game_timers
        game_timers.pop(game_id, None)

    await message.answer("✅ O'yin tugatildi.")


@router.message(Command("players"))
async def cmd_players(message: Message):
    chat = message.chat
    if chat.type == "private":
        await message.answer("Bu buyruq faqat guruhda ishlaydi.")
        return

    for gid, g in active_games.items():
        if g.get("chat_id") == chat.id:
            players = [
                f"{'✅' if pd['alive'] else '💀'} {pd.get('name', f'ID{uid}')}"
                for uid, pd in g["players"].items()
            ]
            text = "👥 *O'yinchilar:*\n" + "\n".join(players) if players else "Hali hech kim yo'q"
            await message.answer(text)
            return

    await message.answer("❌ Faol o'yin topilmadi.")


@router.callback_query(F.data.startswith("admin:"))
async def handle_admin_actions(callback: CallbackQuery):
    action = callback.data.split(":")[1]

    if action == "end":
        await cmd_endgame(callback.message)
    elif action == "stats":
        await cmd_stats(callback.message)

    await callback.answer()


async def cmd_stats(message: Message):
    for gid, g in active_games.items():
        if g.get("chat_id") == message.chat.id:
            alive = []
            dead = []
            for uid, pd in g["players"].items():
                name = pd.get("name", f"ID{uid}")
                entry = f"{pd['role'].short_name()} — {name}"
                if pd["alive"]:
                    alive.append(entry)
                else:
                    dead.append(entry)

            events = await db.get_events(gid)
            event_text = "\n".join(f"• {e['description']}" for e in events[-5:]) or "Hodisalar yo'q"

            text = GAME_STATS.format(
                roles=", ".join(pd['role'].short_name() for pd in g["players"].values()),
                events=event_text,
                alive=len(alive),
                alive_list="\n".join(alive) if alive else "—",
                dead_list="\n".join(dead) if dead else "—",
            )
            await message.answer(text)
            return

    await message.answer("❌ Faol o'yin topilmadi.")
