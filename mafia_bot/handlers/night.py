import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from database.db import Database
from utils.game_logic import active_games
from utils.messages import NIGHT_ACTION_DONE, NIGHT_TIMEOUT

router = Router()
db = Database()
logger = logging.getLogger(__name__)


@router.message(Command("night"))
async def cmd_night_info(message: Message):
    """Kecha haqida ma'lumot"""
    user_id = message.from_user.id
    
    # Foydalanuvchi qaysi o'yinda ekanligini topish
    for game_id, game in active_games.items():
        if user_id in game["players"] and game["phase"] == "night":
            player = game["players"][user_id]
            role = player.get("role")
            
            if role and role.night_action:
                await message.answer(
                    f"🌙 Hozir kecha. Sizning rolingiz: {role.full_name()}\n\n"
                    f"Harakatingizni bajarish uchun shaxsiy xabaringizdagi tugmalardan foydalaning.",
                    parse_mode="Markdown"
                )
            else:
                await message.answer(
                    "🌙 Hozir kecha. Sizning maxsus harakatingiz yo'q. Ertalabgacha kuting.",
                    parse_mode="Markdown"
                )
            return
    
    await message.answer("❌ Siz faol o'yinda emassiz yoki hozir kecha fazasi emas.")
