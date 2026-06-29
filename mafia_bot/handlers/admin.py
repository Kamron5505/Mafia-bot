import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums.chat_type import ChatType

from database.db import Database
from utils.game_logic import active_games, game_timers, end_game_cleanup
from utils.messages import (
    GROUP_ONLY, ADMIN_ONLY, NO_ACTIVE_GAME, GAME_ENDED,
    GAME_STATS
)

router = Router()
db = Database()
logger = logging.getLogger(__name__)


@router.message(Command("endgame"))
async def cmd_endgame(message: Message):
    """O'yinni tugatish"""
    chat = message.chat
    if chat.type == ChatType.PRIVATE:
        await message.answer(GROUP_ONLY)
        return

    member = await chat.get_member(message.from_user.id)
    if member.status not in ("creator", "administrator"):
        await message.answer(ADMIN_ONLY)
        return

    game_data = await db.get_active_game(chat.id)
    if not game_data:
        await message.answer(NO_ACTIVE_GAME)
        return

    game_id = game_data["game_id"]
    
    # Taymerni bekor qilish
    task = game_timers.pop(game_id, None)
    if task:
        task.cancel()
    
    await end_game_cleanup(game_id)
    await message.answer(GAME_ENDED)


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Admin panel"""
    chat = message.chat
    if chat.type == ChatType.PRIVATE:
        # Shaxsiy xabarda admin panel
        from config import ADMIN_IDS
        if message.from_user.id not in ADMIN_IDS:
            await message.answer("❌ Siz admin emassiz.")
            return
        
        await message.answer(
            "👑 **Admin Panel**\n\n"
            "Mavjud buyruqlar:\n"
            "/stats - O'yin statistikasi\n"
            "/endgame - O'yinni tugatish\n"
            "/players - O'yinchilar ro'yxati",
            parse_mode="Markdown"
        )
    else:
        await message.answer("👑 Admin panel uchun /endgame, /stats, /players buyruqlaridan foydalaning.")


@router.callback_query(F.data.startswith("admin:"))
async def handle_admin_actions(callback: CallbackQuery):
    """Admin tugmalari"""
    action = callback.data.split(":")[1]
    
    if action == "end":
        await cmd_endgame(callback.message)
    elif action == "stats":
        # Statistikani ko'rsatish
        chat = callback.message.chat
        game_data = await db.get_active_game(chat.id)
        if not game_data:
            await callback.message.answer(NO_ACTIVE_GAME)
        else:
            game = active_games.get(game_data["game_id"])
            if game:
                players = game["players"]
                roles_str = ", ".join(
                    p["role"].short_name() for p in players.values() if p.get("role")
                )
                
                events = await db.get_events(game_data["game_id"])
                event_text = "\n".join(f"• {e['description']}" for e in events[-5:]) or "Hodisalar yo'q"
                
                alive = [p for p in players.values() if p["alive"]]
                dead = [p for p in players.values() if not p["alive"]]
                
                text = GAME_STATS.format(
                    roles=roles_str,
                    events=event_text,
                    alive=len(alive),
                    alive_list="\n".join(f"✅ {p['name']}" for p in alive) if alive else "—",
                    dead_list="\n".join(f"💀 {p['name']}" for p in dead) if dead else "—",
                )
                await callback.message.answer(text, parse_mode="Markdown")
    
    await callback.answer()
