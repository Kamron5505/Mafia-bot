from typing import Optional, List


class BaseRole:
    """Barcha rollar uchun asosiy klass"""

    name: str = ""
    title: str = ""
    emoji: str = ""
    team: str = ""  # "mafia", "town", "neutral"
    description: str = ""
    night_action: bool = False
    action_type: str = ""
    passive: bool = False

    def __init__(self):
        pass

    def short_name(self) -> str:
        return f"{self.emoji} {self.title}"

    def full_name(self) -> str:
        return f"{self.emoji} **{self.title}** ({self.name})"

    def get_description(self) -> str:
        return f"{self.full_name()}\n\n{self.description}\n\nJamoa: {self.team_name()}"

    def team_name(self) -> str:
        teams = {
            "mafia": "🦈 Qora Kuchlar",
            "town": "🛡 Oq Kuchlar",
            "neutral": "🌪 Neytral",
        }
        return teams.get(self.team, "Noma'lum")

    def can_act_at_night(self) -> bool:
        return self.night_action

    def get_action_players(self, alive_players: List[dict]) -> List[dict]:
        """Kecha harakati uchun tirik o'yinchilar ro'yxati"""
        return [p for p in alive_players if not self._is_self(p)]

    def _is_self(self, player: dict) -> bool:
        return False  # subclass lar o'zini chiqarib tashlashi mumkin
