import asyncio
import logging
import sys

if sys.stdout.encoding and sys.stdout.encoding.upper() not in ("UTF-8", "UTF8"):
    sys.stdout.reconfigure(encoding="utf-8")

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import Database
from handlers import start, game, night, day, admin, admin_panel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


async def on_startup():
    logger.info("🚀 Bot ishga tushmoqda...")
    db = Database()
    await db.connect()

    active_games = await db.get_active_games_for_recovery()
    for g in active_games:
        logger.info(f"Qayta tiklash: o'yin #{g['game_id']} ({g['status']})")
        await db.end_game(g["game_id"])

    logger.info("✅ Bot ishga tushdi!")


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start.router,
        game.router,
        night.router,
        day.router,
        admin.router,
        admin_panel.router,
    )

    dp.startup.register(on_startup)

    logger.info("🤖 Bot ishlayapti...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot to'xtatildi.")
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}")
        sys.exit(1)
