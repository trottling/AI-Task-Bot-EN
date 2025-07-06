from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from storage.sqlite import Database


class HasAccessFilter(BaseFilter):
    def __init__(self, admins: list[int], db: Database) -> None:
        self.admins = admins
        self.db = db

    async def __call__(self, event) -> bool:
        # For regular messages
        if isinstance(event, Message):

            if event.from_user.id in self.admins:
                return True

            if event.chat.type == "private":
                return self.db.has_access(event.from_user.id)

            return self.db.has_chat_access(event.chat.id)

        # For callback requests
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            chat = event.message.chat

            if user_id in self.admins:
                return True

            if chat.type == "private":
                return self.db.has_access(user_id)

            return self.db.has_chat_access(chat.id)

        return False
