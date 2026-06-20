import os
import aiosqlite
from config import DB_PATH


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = None
        return cls._instance

    async def connect(self):
        if self.conn is None:
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            self.conn = await aiosqlite.connect(DB_PATH)
            self.conn.row_factory = aiosqlite.Row
            await self._create_tables()
        return self.conn

    async def _create_tables(self):
        await self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS players (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                games_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                mafia_games INTEGER DEFAULT 0,
                town_games INTEGER DEFAULT 0,
                neutral_games INTEGER DEFAULT 0,
                favorite_role TEXT DEFAULT '',
                achievements TEXT DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                status TEXT DEFAULT 'lobby',
                phase TEXT DEFAULT 'lobby',
                night_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                roles_json TEXT DEFAULT '[]',
                players_json TEXT DEFAULT '[]'
            );

            CREATE TABLE IF NOT EXISTS game_players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                user_id INTEGER,
                role_name TEXT,
                role_title TEXT DEFAULT '',
                team TEXT DEFAULT 'town',
                alive INTEGER DEFAULT 1,
                has_voted INTEGER DEFAULT 0,
                vote_target INTEGER DEFAULT NULL,
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            );

            CREATE TABLE IF NOT EXISTS game_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                event_type TEXT,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            );

            CREATE TABLE IF NOT EXISTS night_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                night INTEGER DEFAULT 0,
                user_id INTEGER,
                action_type TEXT,
                target_id INTEGER DEFAULT NULL,
                resolved INTEGER DEFAULT 0,
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            );
        """)
        await self.conn.commit()

    async def get_player(self, user_id: int):
        cur = await self.conn.execute(
            "SELECT * FROM players WHERE user_id = ?", (user_id,)
        )
        return await cur.fetchone()

    async def create_player(self, user_id: int, username: str = "", first_name: str = ""):
        await self.conn.execute(
            """INSERT OR IGNORE INTO players (user_id, username, first_name)
               VALUES (?, ?, ?)""",
            (user_id, username, first_name),
        )
        await self.conn.commit()

    async def update_player_stats(self, user_id: int, won: bool, role_team: str, role_name: str):
        player = await self.get_player(user_id)
        if not player:
            return

        games = player["games_played"] + 1
        wins = player["wins"] + (1 if won else 0)
        losses = player["losses"] + (0 if won else 1)
        mafia = player["mafia_games"] + (1 if role_team == "mafia" else 0)
        town = player["town_games"] + (1 if role_team == "town" else 0)
        neutral = player["neutral_games"] + (1 if role_team == "neutral" else 0)

        await self.conn.execute(
            """UPDATE players SET games_played=?, wins=?, losses=?,
               mafia_games=?, town_games=?, neutral_games=?,
               favorite_role=?
               WHERE user_id=?""",
            (games, wins, losses, mafia, town, neutral, role_name, user_id),
        )
        await self.conn.commit()

    async def add_achievement(self, user_id: int, achievement: str):
        player = await self.get_player(user_id)
        if not player:
            return
        current = player["achievements"] or ""
        if achievement in current:
            return
        new_ach = f"{current}|{achievement}" if current else achievement
        await self.conn.execute(
            "UPDATE players SET achievements=? WHERE user_id=?",
            (new_ach, user_id),
        )
        await self.conn.commit()

    async def create_game(self, chat_id: int):
        cur = await self.conn.execute(
            "INSERT INTO games (chat_id, status, phase) VALUES (?, 'lobby', 'lobby')",
            (chat_id,),
        )
        await self.conn.commit()
        return cur.lastrowid

    async def get_active_game(self, chat_id: int):
        cur = await self.conn.execute(
            "SELECT * FROM games WHERE chat_id=? AND status IN ('lobby','night','day','voting') ORDER BY game_id DESC LIMIT 1",
            (chat_id,),
        )
        return await cur.fetchone()

    async def get_game(self, game_id: int):
        cur = await self.conn.execute(
            "SELECT * FROM games WHERE game_id=?", (game_id,)
        )
        return await cur.fetchone()

    async def update_game_status(self, game_id: int, status: str, phase: str = None):
        if phase:
            await self.conn.execute(
                "UPDATE games SET status=?, phase=? WHERE game_id=?",
                (status, phase, game_id),
            )
        else:
            await self.conn.execute(
                "UPDATE games SET status=? WHERE game_id=?",
                (status, game_id),
            )
        await self.conn.commit()

    async def add_player_to_game(self, game_id: int, user_id: int, role_name: str = "", role_title: str = "", team: str = "town"):
        await self.conn.execute(
            """INSERT OR IGNORE INTO game_players (game_id, user_id, role_name, role_title, team)
               VALUES (?, ?, ?, ?, ?)""",
            (game_id, user_id, role_name, role_title, team),
        )
        await self.conn.commit()

    async def get_game_players(self, game_id: int):
        cur = await self.conn.execute(
            "SELECT * FROM game_players WHERE game_id=?", (game_id,)
        )
        return await cur.fetchall()

    async def get_alive_players(self, game_id: int):
        cur = await self.conn.execute(
            "SELECT * FROM game_players WHERE game_id=? AND alive=1", (game_id,)
        )
        return await cur.fetchall()

    async def get_player_in_game(self, game_id: int, user_id: int):
        cur = await self.conn.execute(
            "SELECT * FROM game_players WHERE game_id=? AND user_id=?",
            (game_id, user_id),
        )
        return await cur.fetchone()

    async def kill_player(self, game_id: int, user_id: int):
        await self.conn.execute(
            "UPDATE game_players SET alive=0 WHERE game_id=? AND user_id=?",
            (game_id, user_id),
        )
        await self.conn.commit()

    async def record_event(self, game_id: int, event_type: str, description: str):
        await self.conn.execute(
            "INSERT INTO game_events (game_id, event_type, description) VALUES (?, ?, ?)",
            (game_id, event_type, description),
        )
        await self.conn.commit()

    async def get_events(self, game_id: int):
        cur = await self.conn.execute(
            "SELECT * FROM game_events WHERE game_id=? ORDER BY timestamp", (game_id,)
        )
        return await cur.fetchall()

    async def save_night_action(self, game_id: int, night: int, user_id: int, action_type: str, target_id: int = None):
        await self.conn.execute(
            "INSERT INTO night_actions (game_id, night, user_id, action_type, target_id) VALUES (?, ?, ?, ?, ?)",
            (game_id, night, user_id, action_type, target_id),
        )
        await self.conn.commit()

    async def get_night_actions(self, game_id: int, night: int):
        cur = await self.conn.execute(
            "SELECT * FROM night_actions WHERE game_id=? AND night=? AND resolved=0",
            (game_id, night),
        )
        return await cur.fetchall()

    async def resolve_night_action(self, action_id: int):
        await self.conn.execute(
            "UPDATE night_actions SET resolved=1 WHERE id=?", (action_id,)
        )
        await self.conn.commit()

    async def end_game(self, game_id: int):
        await self.conn.execute(
            "UPDATE games SET status='ended', phase='ended' WHERE game_id=?",
            (game_id,),
        )
        await self.conn.commit()

    async def get_active_games_for_recovery(self):
        cur = await self.conn.execute(
            "SELECT * FROM games WHERE status IN ('night','day','voting')"
        )
        return await cur.fetchall()

    async def close(self):
        if self.conn:
            await self.conn.close()
            self.conn = None

    async def set_vote(self, game_id: int, user_id: int, target_id: int):
        await self.conn.execute(
            "UPDATE game_players SET has_voted=1, vote_target=? WHERE game_id=? AND user_id=?",
            (target_id, game_id, user_id),
        )
        await self.conn.commit()

    async def reset_votes(self, game_id: int):
        await self.conn.execute(
            "UPDATE game_players SET has_voted=0, vote_target=NULL WHERE game_id=?",
            (game_id,),
        )
        await self.conn.commit()
