from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_lobby_keyboard(game_id: int, player_count: int) -> InlineKeyboardMarkup:
    """Lobby davridagi tugmalar"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Qo'shilish", callback_data=f"join:{game_id}"),
        InlineKeyboardButton(text="🚪 Chiqish", callback_data=f"leave:{game_id}"),
    )
    return builder.as_markup()


def get_game_action_keyboard(game_id: int, is_alive: bool = True) -> InlineKeyboardMarkup:
    """O'yin davridagi tugmalar"""
    builder = InlineKeyboardBuilder()
    if is_alive:
        builder.row(
            InlineKeyboardButton(text="🗳 Ovoz berish", callback_data=f"vote_menu:{game_id}"),
        )
    builder.row(
        InlineKeyboardButton(text="👤 Profil", callback_data="profile:view"),
        InlineKeyboardButton(text="🚪 Chiqish", callback_data=f"leave:{game_id}"),
    )
    return builder.as_markup()


def get_night_action_keyboard(game_id: int, players: list, action_type: str) -> InlineKeyboardMarkup:
    """Kecha harakati uchun o'yinchilar ro'yxati"""
    builder = InlineKeyboardBuilder()
    for player in players:
        name = player.get("name", f"ID{player['user_id']}")
        builder.row(
            InlineKeyboardButton(
                text=name,
                callback_data=f"night_action:{game_id}:{action_type}:{player['user_id']}"
            )
        )
    builder.row(
        InlineKeyboardButton(text="⏭ O'tkazib yuborish", callback_data=f"night_skip:{game_id}"),
    )
    return builder.as_markup()


def get_roles_list_keyboard() -> InlineKeyboardMarkup:
    """Rollar ro'yxati (kategoriyalar bo'yicha)"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🦈 Qora Kuchlar", callback_data="roles:mafia"),
    )
    builder.row(
        InlineKeyboardButton(text="🛡 Oq Kuchlar", callback_data="roles:town"),
    )
    builder.row(
        InlineKeyboardButton(text="🌪 Neytrallar", callback_data="roles:neutral"),
    )
    builder.row(
        InlineKeyboardButton(text="◀ Orqaga", callback_data="menu:back"),
    )
    return builder.as_markup()


def get_mafia_chat_kill_keyboard(game_id: int, targets: list) -> InlineKeyboardMarkup:
    """Mafiya guruh chatida o'ldirish uchun ovoz berish"""
    builder = InlineKeyboardBuilder()
    for target in targets:
        name = target.get("name", f"ID{target['user_id']}")
        builder.row(
            InlineKeyboardButton(
                text=name,
                callback_data=f"mafia_vote_kill:{game_id}:{target['user_id']}"
            )
        )
    return builder.as_markup()
