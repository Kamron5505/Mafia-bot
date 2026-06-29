from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu() -> InlineKeyboardMarkup:
    """Asosiy menyu"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎮 Chatga o'yin qo'shish", callback_data="menu:add_to_chat"),
    )
    builder.row(
        InlineKeyboardButton(text="🎲 Chatga kirish", callback_data="menu:join_chat"),
    )
    builder.row(
        InlineKeyboardButton(text="🌐 Til / Language", callback_data="menu:language"),
        InlineKeyboardButton(text="👤 Profil | 🎭 Rollar", callback_data="menu:profile_roles"),
    )
    return builder.as_markup()


def get_profile_roles_menu() -> InlineKeyboardMarkup:
    """Profil va rollar menyusi"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👤 Profil", callback_data="profile:view"),
        InlineKeyboardButton(text="🎭 Rollar", callback_data="roles:list"),
    )
    builder.row(
        InlineKeyboardButton(text="◀ Orqaga", callback_data="menu:back"),
    )
    return builder.as_markup()


def get_back_button(callback_data: str = "menu:back") -> InlineKeyboardMarkup:
    """Orqaga tugmasi"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="◀ Orqaga", callback_data=callback_data),
    )
    return builder.as_markup()
