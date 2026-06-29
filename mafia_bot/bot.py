import asyncio
import logging
import sys

# UTF-8 sozlash
if sys.stdout.encoding and sys.stdout.encoding.upper() not in ("UTF-8", "UTF8"):
    sys.stdout.reconfigure(encoding="utf-8")

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import BOT_TOKEN
from database.db import Database
from handlers import start, game, night, day, admin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


async def on_startup():
    """Bot ishga tushganda bajariladigan ishlar"""
    logger.info("🚀 Bot ishga tushmoqda...")
    db = Database()
    await db.connect()

    # Qayta tiklash: avvalgi faol o'yinlarni tugatish
    active_games = await db.get_active_games_for_recovery()
    for g in active_games:
        logger.info(f"Qayta tiklash: o'yin #{g['game_id']} ({g['status']})")
        await db.end_game(g["game_id"])

    logger.info("✅ Bot ishga tushdi!")


async def set_bot_commands(bot: Bot):
    """Bot komandalarini o'rnatish"""
    commands = [
        BotCommand(command="start", description="🔄 Botni ishga tushirish"),
        BotCommand(command="profile", description="👤 Profilim"),
        BotCommand(command="help", description="❓ Yordam"),
        BotCommand(command="rules", description="📜 Qoidalar"),
        BotCommand(command="language", description="🌐 Tilni o'zgartirish"),
        BotCommand(command="admin", description="👑 Admin panel"),
        BotCommand(command="startgame", description="🎮 O'yin boshlash (guruh)"),
        BotCommand(command="forcestart", description="⏩ Majburiy start (guruh)"),
        BotCommand(command="endgame", description="⛔ O'yinni tugatish (guruh)"),
        BotCommand(command="stats", description="📊 O'yin statistikasi (guruh)"),
        BotCommand(command="players", description="👥 O'yinchilar ro'yxati (guruh)"),
        BotCommand(command="leave", description="🚪 O'yinni tark etish"),
        BotCommand(command="vote", description="🗳 Ovoz berish"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Asosiy bot funksiyasi"""
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )

    await set_bot_commands(bot)

    dp = Dispatcher(storage=MemoryStorage())

    # Routerlarni ulash
    dp.include_routers(
        start.router,
        game.router,
        night.router,
        day.router,
        admin.router,
    )

    dp.startup.register(on_startup)

    logger.info("🤖 Bot ishlayapti...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot to'xtatildi.")
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}")
        sys.exit(1)
