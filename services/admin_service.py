import logging

from storage.sqlite import Database

logger = logging.getLogger(__name__)

class AdminService:
    def __init__(self, db: Database):
        self.db = db

    def get_users_count(self) -> int:
        count = self.db.count_users()
        return count[0] if count else 0

    def get_reqs_count(self) -> int:
        count = self.db.count_reqs()
        return count[0] if count else 0

    def set_user_access(self, user_id: int, allowed: bool) -> dict:
        try:
            self.db.set_access(user_id, allowed)
            return {"success": True}
        except Exception as e:
            logger.exception(f"Error changing user access: {e}")
            return {"success": False, "error": str(e)}

    def set_chat_access(self, chat_id: int, allowed: bool) -> dict:
        try:
            self.db.set_chat_access(chat_id, allowed)
            return {"success": True}
        except Exception as e:
            logger.exception(f"Error changing chat access: {e}")
            return {"success": False, "error": str(e)}