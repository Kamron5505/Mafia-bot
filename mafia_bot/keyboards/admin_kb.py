from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_panel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Karta qo'shish", callback_data="apanel:add_card"),
        InlineKeyboardButton(text="📢 Kanal qo'shish", callback_data="apanel:add_channel"),
    )
    builder.row(
        InlineKeyboardButton(text="🔗 Referallar", callback_data="apanel:referrals"),
        InlineKeyboardButton(text="📋 Kanallar ro'yxati", callback_data="apanel:list_channels"),
    )
    builder.row(
        InlineKeyboardButton(text="💳 Kartalar ro'yxati", callback_data="apanel:list_cards"),
        InlineKeyboardButton(text="📊 Statistika", callback_data="apanel:stats"),
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main"),
    )
    return builder.as_markup()


def admin_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Admin panel", callback_data="apanel:panel"),
    )
    return builder.as_markup()


def cancel_kb(action: str = "") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    data = f"apanel:cancel_{action}" if action else "apanel:cancel"
    builder.row(
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data=data),
    )
    return builder.as_markup()
