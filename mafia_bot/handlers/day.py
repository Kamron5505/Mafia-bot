import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from database.db import Database
from utils.game_logic import active_games
from utils.messages import VOTE_CAST

router = Router()
db = Database()
logger = logging.getLogger(__name__)


@router.message(Command("vote"))
async def cmd_vote(message: Message):
    """Ovoz berish buyrug'i"""
    chat = message.chat
    user = message.from_user
    
    # Faol o'yinni topish
    game_data = await db.get_active_game(chat.id)
    if not game_data:
        await message.answer("❌ Bu chatda faol o'yin yo'q.")
        return
    
    game = active_games.get(game_data["game_id"])
    if not game or game["phase"] != "voting":
        await message.answer("❌ Hozir ovoz berish fazasi emas.")
        return
    
    if user.id not in game["players"]:
        await message.answer("❌ Siz o'yinda emassiz.")
        return
    
    if not game["players"][user.id]["alive"]:
        await message.answer("💀 Siz o'lgansiz, ovoz bera olmaysiz.")
        return
    
    if user.id in game["votes_cast"]:
        await message.answer("❌ Siz allaqachon ovoz bergansiz.")
        return
    
    # Ovoz berish tugmalarini yuborish
    alive_players = [p for p in game["players"].values() if p["alive"] and p["user_id"] != user.id]
    from keyboards.vote_kb import get_vote_keyboard
    await message.answer(
        "🗳 **Ovoz berish:** Kim chiqarilishini tanlang:",
        reply_markup=get_vote_keyboard(game_data["game_id"], alive_players, user.id),
        parse_mode="Markdown"
    )
