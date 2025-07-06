import logging
from storage.sqlite import Database

logger = logging.getLogger(__name__)

class SettingsService:
    def __init__(self, db: Database):
        self.db = db 

    def set_timezone(self, user_id: int, timezone: str) -> None:
        self.db.set_timezone(user_id, timezone)

    def get_timezone(self, user_id: int) -> str:
        return self.db.get_timezone(user_id)

    def set_chat_timezone(self, chat_id: int, timezone: str) -> None:
        self.db.set_chat_timezone(chat_id, timezone)

    def get_chat_timezone(self, chat_id: int) -> str:
        return self.db.get_chat_timezone(chat_id) 