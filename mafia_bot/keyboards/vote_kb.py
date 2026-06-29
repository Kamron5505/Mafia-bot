from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_vote_keyboard(game_id: int, players: list, voter_id: int) -> InlineKeyboardMarkup:
    """Ovoz berish uchun inline tugmalar"""
    builder = InlineKeyboardBuilder()
    for player in players:
        if player["user_id"] == voter_id:
            continue  # O'ziga ovoz bera olmaydi
        name = player.get("name", f"ID{player['user_id']}")
        builder.row(
            InlineKeyboardButton(
                text=name,
                callback_data=f"vote:{game_id}:{player['user_id']}"
            )
        )
    # Hech kimga ovoz bermaslik
    builder.row(
        InlineKeyboardButton(
            text="❌ Hech kim",
            callback_data=f"vote:{game_id}:0"
        ),
        InlineKeyboardButton(
            text="⏭ O'tkazib yuborish",
            callback_data=f"vote_skip:{game_id}"
        ),
    )
    return builder.as_markup()


def get_vote_results_keyboard() -> InlineKeyboardMarkup:
    """Ovoz natijalaridan keyin"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⏭ Davom etish", callback_data="vote:continue"),
    )
    return builder.as_markup()
