import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = "data/mafia_bot.db"

GAME_JOIN_TIME = 60
DAY_DISCUSSION_TIME = 300
VOTE_TIME = 60
NIGHT_ACTION_TIME = 30

MIN_PLAYERS = 6
MAX_PLAYERS = 30

ROLES_PER_GAME = 12

ADMIN_IDS = []
