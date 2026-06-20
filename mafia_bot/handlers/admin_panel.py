import string
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import Database
from config import ADMIN_IDS
from keyboards.admin_kb import admin_panel_kb, admin_back_kb, cancel_kb
from keyboards.main_menu import main_menu_kb

router = Router()
db = Database()


class AdminStates(StatesGroup):
    waiting_card_name = State()
    waiting_card_desc = State()
    waiting_card_price = State()
    waiting_card_duration = State()
    waiting_channel_id = State()
    waiting_channel_username = State()
    waiting_referral_target = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        return
    if message.chat.type != "private":
        await message.answer("❌ Admin panel faqat shaxsiy chatda ishlaydi.")
        return
    await message.answer(
        "👑 *Admin panel*\n\nQuyidagi amallardan birini tanlang:",
        reply_markup=admin_panel_kb(),
    )


@router.callback_query(F.data == "apanel:panel")
async def back_to_admin_panel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌", show_alert=True)
        return
    await callback.message.edit_text(
        "👑 *Admin panel*\n\nQuyidagi amallardan birini tanlang:",
        reply_markup=admin_panel_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("apanel:"))
async def handle_admin_callbacks(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌", show_alert=True)
        return

    action = callback.data.split(":")[1]

    if action == "add_card":
        await state.set_state(AdminStates.waiting_card_name)
        await callback.message.edit_text(
            "💳 *Yangi karta qo'shish*\n\nKarta nomini kiriting:",
            reply_markup=cancel_kb("add_card"),
        )
        await callback.answer()

    elif action == "add_channel":
        await state.set_state(AdminStates.waiting_channel_id)
        await callback.message.edit_text(
            "📢 *Kanal qo'shish*\n\nKanal ID sini kiriting (masalan: -1001234567890):",
            reply_markup=cancel_kb("add_channel"),
        )
        await callback.answer()

    elif action == "referrals":
        await show_referral_stats(callback.message)
        await callback.answer()

    elif action == "list_channels":
        await list_channels(callback.message)
        await callback.answer()

    elif action == "list_cards":
        await list_cards(callback.message)
        await callback.answer()

    elif action == "stats":
        await show_admin_stats(callback.message)
        await callback.answer()

    elif action == "cancel" or action.startswith("cancel_"):
        await state.clear()
        await callback.message.edit_text(
            "👑 *Admin panel*\n\nQuyidagi amallardan birini tanlang:",
            reply_markup=admin_panel_kb(),
        )
        await callback.answer()


@router.message(AdminStates.waiting_card_name)
async def process_card_name(message: Message, state: FSMContext):
    await state.update_data(card_name=message.text)
    await state.set_state(AdminStates.waiting_card_desc)
    await message.answer(
        "Karta tavsifini kiriting:",
        reply_markup=cancel_kb("add_card"),
    )


@router.message(AdminStates.waiting_card_desc)
async def process_card_desc(message: Message, state: FSMContext):
    await state.update_data(card_desc=message.text)
    await state.set_state(AdminStates.waiting_card_price)
    await message.answer(
        "Karta narxini kiriting (so'm):",
        reply_markup=cancel_kb("add_card"),
    )


@router.message(AdminStates.waiting_card_price)
async def process_card_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Iltimos, son kiriting!", reply_markup=cancel_kb("add_card"))
        return
    await state.update_data(card_price=int(message.text))
    await state.set_state(AdminStates.waiting_card_duration)
    await message.answer(
        "Karta muddatini kiriting (kunlarda):",
        reply_markup=cancel_kb("add_card"),
    )


@router.message(AdminStates.waiting_card_duration)
async def process_card_duration(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Iltimos, son kiriting!", reply_markup=cancel_kb("add_card"))
        return
    data = await state.get_data()
    card_id = await db.add_card(
        name=data["card_name"],
        description=data["card_desc"],
        price=data["card_price"],
        duration_days=int(message.text),
    )
    await state.clear()
    await message.answer(
        f"✅ Karta qo'shildi!\n\n"
        f"ID: {card_id}\n"
        f"Nomi: {data['card_name']}\n"
        f"Narxi: {data['card_price']} so'm\n"
        f"Muddati: {message.text} kun",
        reply_markup=admin_panel_kb(),
    )


@router.message(AdminStates.waiting_channel_id)
async def process_channel_id(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.startswith("-") and text[1:].isdigit() or text.lstrip("-").isdigit():
        channel_id = int(text)
        await state.update_data(channel_id=channel_id)
        await state.set_state(AdminStates.waiting_channel_username)
        await message.answer(
            "Kanal username'ini kiriting (masalan: @my_channel yoki https://t.me/my_channel):",
            reply_markup=cancel_kb("add_channel"),
        )
    else:
        await message.answer("❌ Noto'g'ri ID. Iltimos, kanal ID sini kiriting:", reply_markup=cancel_kb("add_channel"))


@router.message(AdminStates.waiting_channel_username)
async def process_channel_username(message: Message, state: FSMContext):
    data = await state.get_data()
    username = message.text.strip().replace("https://t.me/", "@").replace("@", "")
    if username:
        username = "@" + username
    await db.add_channel(
        channel_id=data["channel_id"],
        channel_username=username,
        title=message.text,
    )
    await state.clear()
    await message.answer(
        f"✅ Kanal qo'shildi!\n\n"
        f"ID: {data['channel_id']}\n"
        f"Username: {username}",
        reply_markup=admin_panel_kb(),
    )


async def show_referral_stats(message: Message):
    user_id = message.from_user.id
    code_data = await db.get_referral_code_by_user(user_id)
    code = ""
    if not code_data:
        code = generate_referral_code()
        await db.create_referral_code(user_id, code)
    else:
        code = code_data["code"]
    count = await db.get_referral_count(user_id)
    referrals = await db.get_referrals(user_id)
    bot_username = (await message.bot.me()).username
    text = (
        f"🔗 *Referal tizimi*\n\n"
        f"Sizning kodingiz: `{code}`\n"
        f"Taklif qilinganlar: {count} ta\n\n"
        f"Havola:\n"
        f"`https://t.me/{bot_username}?start=ref_{code}`\n\n"
    )
    if referrals:
        text += "📋 *Taklif qilinganlar:*\n"
        for ref in referrals[:10]:
            text += f"• ID{ref['referred_id']}\n"
    await message.edit_text(text, reply_markup=admin_back_kb())


def generate_referral_code() -> str:
    letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for _ in range(6))


async def list_channels(message: Message):
    channels = await db.get_all_channels()
    if not channels:
        text = "📢 *Kanallar ro'yxati*\n\nHali kanal qo'shilmagan."
    else:
        text = "📢 *Kanallar ro'yxati:*\n\n"
        for ch in channels:
            text += (
                f"• {ch['title'] or ch['channel_username'] or ch['channel_id']}\n"
                f"  ID: {ch['channel_id']}\n"
                f"  Status: {'✅ Majburiy' if ch['is_required'] else '❌ Majburiy emas'}\n\n"
            )
    await message.edit_text(text, reply_markup=admin_back_kb())


async def list_cards(message: Message):
    cards = await db.get_cards()
    if not cards:
        text = "💳 *Kartalar ro'yxati*\n\nHali karta qo'shilmagan."
    else:
        text = "💳 *Kartalar ro'yxati:*\n\n"
        for card in cards:
            text += (
                f"ID {card['id']}: *{card['name']}*\n"
                f"  {card['description']}\n"
                f"  Narxi: {card['price']} so'm\n"
                f"  Muddati: {card['duration_days']} kun\n\n"
            )
    await message.edit_text(text, reply_markup=admin_back_kb())


async def show_admin_stats(message: Message):
    from roles.base_role import get_all_roles
    cards = await db.get_cards()
    channels = await db.get_all_channels()
    text = (
        f"📊 *Admin statistika*\n\n"
        f"🎭 Rollar soni: {len(get_all_roles())}\n"
        f"💳 Kartalar: {len(cards)} ta\n"
        f"📢 Kanallar: {len(channels)} ta\n"
    )
    await message.edit_text(text, reply_markup=admin_back_kb())
