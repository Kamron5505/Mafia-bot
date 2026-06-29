import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.enums.chat_type import ChatType

from database.db import Database
from keyboards.main_menu import get_main_menu, get_profile_roles_menu, get_back_button
from keyboards.game_kb import get_roles_list_keyboard
from utils.messages import (
    WELCOME_TEXT, PROFILE_TEXT, RULES_TEXT, HELP_TEXT,
    ERROR_START_PRIVATE, GROUP_ONLY
)
from utils.role_selector import get_all_roles_by_category
from utils.game_logic import active_games, leave_game
from config import MIN_PLAYERS, MAX_PLAYERS

router = Router()
db = Database()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start buyrug'i - asosiy menyuni ko'rsatadi"""
    if message.chat.type != ChatType.PRIVATE:
        await message.answer(ERROR_START_PRIVATE)
        return
    
    user = message.from_user
    await db.create_player(user.id, user.username or "", user.first_name or "")
    
    await message.answer(
        WELCOME_TEXT,
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    """Profil buyrug'i"""
    user = message.from_user
    await show_profile(message, user.id)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam buyrug'i"""
    await message.answer(HELP_TEXT, parse_mode="Markdown")


@router.message(Command("rules"))
async def cmd_rules(message: Message):
    """Qoidalar buyrug'i"""
    text = RULES_TEXT.format(min_players=MIN_PLAYERS, max_players=MAX_PLAYERS)
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("leave"))
async def cmd_leave(message: Message):
    """O'yinni tark etish buyrug'i"""
    chat = message.chat
    user = message.from_user
    
    if chat.type == ChatType.PRIVATE:
        await message.answer(GROUP_ONLY)
        return
    
    # Faol o'yinni topish
    game_data = await db.get_active_game(chat.id)
    if not game_data:
        await message.answer("❌ Bu chatda faol o'yin yo'q.")
        return
    
    success = await leave_game(game_data["game_id"], user.id)
    if success:
        await message.answer(f"🚪 {user.first_name} o'yinni tark etdi.")
    else:
        await message.answer("❌ Siz o'yinda emassiz yoki o'yin lobbi bosqichida emas.")


# === Callback handlers ===

@router.callback_query(F.data.startswith("menu:"))
async def handle_menu(callback: CallbackQuery):
    """Asosiy menyu callback'lari"""
    action = callback.data.split(":")[1]
    
    if action == "back":
        await callback.message.edit_text(
            "🎮 **Mafiya O'yin Boti**\n\nKerakli bo'limni tanlang:",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    elif action == "language":
        await callback.message.edit_text(
            "🌐 **Til / Language**\n\nHozircha faqat O'zbek tili (lotin) qo'llab-quvvatlanadi.\n🇺🇿 O'zbek",
            reply_markup=get_back_button("menu:back"),
            parse_mode="Markdown"
        )
    elif action == "profile_roles":
        await callback.message.edit_text(
            "👤 Profil yoki 🎭 Rollarni tanlang:",
            reply_markup=get_profile_roles_menu(),
            parse_mode="Markdown"
        )
    elif action == "add_to_chat":
        await callback.message.edit_text(
            "🤖 **Botni guruhingizga qo'shish:**\n\n"
            "1. Botni guruhingizga admin qilib qo'shing\n"
            "2. Guruhda /startgame deb yozing\n"
            "3. O'yin boshlanadi va o'yinchilar qo'shilishi mumkin\n\n"
            "Bot username: @your_bot_username",
            reply_markup=get_back_button("menu:back"),
            parse_mode="Markdown"
        )
    elif action == "join_chat":
        await callback.message.edit_text(
            "🎲 **O'yinga qo'shilish:**\n\n"
            "O'yin boshlangan guruhga o'ting va\n"
            "\"✅ Qo'shilish\" tugmasini bosing.\n\n"
            "Yoki guruhda /startgame buyrug'ini kutib turing.",
            reply_markup=get_back_button("menu:back"),
            parse_mode="Markdown"
        )
    
    await callback.answer()


@router.callback_query(F.data.startswith("profile:"))
async def handle_profile(callback: CallbackQuery):
    """Profil callback'lari"""
    action = callback.data.split(":")[1]
    
    if action == "view":
        await show_profile(callback.message, callback.from_user.id, edit=True)
    
    await callback.answer()


@router.callback_query(F.data.startswith("roles:"))
async def handle_roles(callback: CallbackQuery):
    """Rollar callback'lari"""
    action = callback.data.split(":")[1]
    
    if action == "list":
        await callback.message.edit_text(
            "🎭 **Rollar kategoriyalari:**\n\nKategoriyani tanlang:",
            reply_markup=get_roles_list_keyboard(),
            parse_mode="Markdown"
        )
    elif action in ("mafia", "town", "neutral"):
        categories = get_all_roles_by_category()
        roles = categories.get(action, [])
        
        category_names = {
            "mafia": "🦈 Qora Kuchlar (Mafiya)",
            "town": "🛡 Oq Kuchlar (Shahar)",
            "neutral": "🌪 Neytrallar",
        }
        
        text = f"**{category_names.get(action, 'Rollar')}**\n\n"
        for role in roles:
            text += f"{role.emoji} **{role.title}** — {role.description[:80]}...\n"
        
        # Split into multiple messages if too long
        if len(text) > 4000:
            await callback.message.edit_text(
                text[:4000] + "\n\n...davomi bor",
                reply_markup=get_back_button("roles:list"),
                parse_mode="Markdown"
            )
        else:
            await callback.message.edit_text(
                text,
                reply_markup=get_back_button("roles:list"),
                parse_mode="Markdown"
            )
    
    await callback.answer()


async def show_profile(message: Message, user_id: int, edit: bool = False):
    """Profil ma'lumotlarini ko'rsatish"""
    player = await db.get_player(user_id)
    
    if not player:
        text = "👤 **PROFIL**\n\nSiz hali o'yin o'ynamagansiz. Botni ishga tushirish uchun /start ni bosing."
        if edit:
            await message.edit_text(text, parse_mode="Markdown")
        else:
            await message.answer(text, parse_mode="Markdown")
        return
    
    games = player["games_played"] or 0
    wins = player["wins"] or 0
    losses = player["losses"] or 0
    win_rate = round((wins / games * 100)) if games > 0 else 0
    
    achievements = player["achievements"] or ""
    achievements_display = achievements.replace("|", " | ") if achievements else "Yutuqlar yo'q"
    
    fav_role = player["favorite_role"] or "—"
    
    text = PROFILE_TEXT.format(
        games_played=games,
        wins=wins,
        win_rate=win_rate,
        losses=losses,
        favorite_role=fav_role,
        mafia_games=player["mafia_games"] or 0,
        town_games=player["town_games"] or 0,
        neutral_games=player["neutral_games"] or 0,
        achievements=achievements_display,
    )
    
    if edit:
        await message.edit_text(text, parse_mode="Markdown")
    else:
        await message.answer(text, parse_mode="Markdown")
