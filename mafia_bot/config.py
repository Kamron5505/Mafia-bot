import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8954728309:AAHhv2kHbP46KYOVnwtPcfHFuWim0Kb0ZIM")
DB_PATH = "mafia_bot/data/mafia_bot.db"

# Vaqt sozlamalari (soniyalarda)
GAME_JOIN_TIME = 60
DAY_DISCUSSION_TIME = 300
VOTE_TIME = 60
NIGHT_ACTION_TIME = 30

# O'yin chegaralari
MIN_PLAYERS = 6
MAX_PLAYERS = 30

# Har bir o'yin uchun tanlanadigan rollar soni
ROLES_PER_GAME = 6

# Admin ID lar (agar kerak bo'lsa)
ADMIN_IDS = [7597422591, 8784918764]
