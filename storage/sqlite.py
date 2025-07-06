import logging
import sqlite3
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, path_to_db: str) -> None:
        self.path_to_db: str = path_to_db
        self._init_db()

    def _init_db(self) -> None:
        # Creating all necessary tables
        create_users = """
                       CREATE TABLE IF NOT EXISTS Users
                       (
                           is_allowed  INTEGER DEFAULT 0,
                           telegram_id INTEGER PRIMARY KEY,
                           full_name   TEXT,
                           timezone    TEXT DEFAULT '+3'
                       );
                       """
        create_chats = """
                       CREATE TABLE IF NOT EXISTS Chats
                       (
                           is_allowed INTEGER DEFAULT 0,
                           chat_id    INTEGER PRIMARY KEY,
                           title      TEXT,
                           timezone   TEXT DEFAULT '+3'
                       ); \
                       """
        create_requests = """
                          CREATE TABLE IF NOT EXISTS REQUESTS
                          (
                              id          INTEGER PRIMARY KEY AUTOINCREMENT,
                              req_time    TEXT,
                              req_text    TEXT,
                              req_user_id INTEGER,
                              req_resp    TEXT
                          );
                          """

        with sqlite3.connect(self.path_to_db) as connection:
            cursor = connection.cursor()
            cursor.execute(create_users)
            cursor.execute(create_chats)
            cursor.execute(create_requests)
            connection.commit()

    def execute(
            self,
            sql: str,
            parameters: Optional[tuple[Any, ...]] = None,
            *,
            fetchone: bool = False,
            fetchall: bool = False,
            commit: bool = False,
            ) -> Any:
        """
        A universal method for executing SQL queries.
        """
        parameters = parameters or ()
        data = None
        with sqlite3.connect(self.path_to_db) as connection:
            connection.set_trace_callback(logger.debug)
            cursor = connection.cursor()
            cursor.execute(sql, parameters)

            if commit:
                connection.commit()
            if fetchone:
                data = cursor.fetchone()
            if fetchall:
                data = cursor.fetchall()

        return data

    def add_user(self, telegram_id: int, full_name: str, is_allowed: bool = False) -> None:
        if self.user_exists(telegram_id):
            logger.info(f"User {telegram_id} already exists", )
            return
        sql = "INSERT INTO Users(telegram_id, full_name, is_allowed) VALUES(?, ?, ?);"
        self.execute(sql, (telegram_id, full_name, int(is_allowed)), commit=True)

    def user_exists(self, telegram_id: int) -> bool:
        sql = "SELECT 1 FROM Users WHERE telegram_id = ? LIMIT 1;"
        return self.execute(sql, (telegram_id,), fetchone=True) is not None

    def has_access(self, telegram_id: int) -> bool:
        sql = "SELECT is_allowed FROM Users WHERE telegram_id = ? LIMIT 1;"
        row = self.execute(sql, (telegram_id,), fetchone=True)
        return bool(row and row[0])

    def set_access(self, telegram_id: int, allowed: bool) -> None:
        if self.user_exists(telegram_id):
            sql = "UPDATE Users SET is_allowed = ? WHERE telegram_id = ?;"
            self.execute(sql, (int(allowed), telegram_id), commit=True)
        else:
            self.add_user(telegram_id, "", allowed)

    def count_users(self) -> Optional[tuple]:
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def count_reqs(self) -> Optional[tuple]:
        return self.execute("SELECT COUNT(*) FROM REQUESTS;", fetchone=True)

    def add_request(self, req_text: str, req_user_id: int, req_resp: str) -> None:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = (
                "INSERT INTO REQUESTS(req_time, req_text, req_user_id, req_resp) "
                "VALUES(?, ?, ?, ?);"
            )
            self.execute(sql, (now, req_text, req_user_id, req_resp), commit=True)
        except Exception as e:
            logger.exception(f"Failed to save request: {e}")

    # Chat management

    def add_chat(self, chat_id: int, title: str, is_allowed: bool = False) -> None:
        if self.chat_exists(chat_id):
            logger.info(f"Чат {chat_id} уже существует в БД")
            return
        sql = "INSERT INTO Chats(chat_id, title, is_allowed) VALUES(?, ?, ?);"
        self.execute(sql, (chat_id, title, int(is_allowed)), commit=True)

    def chat_exists(self, chat_id: int) -> bool:
        sql = "SELECT 1 FROM Chats WHERE chat_id = ? LIMIT 1;"
        return self.execute(sql, (chat_id,), fetchone=True) is not None

    def has_chat_access(self, chat_id: int) -> bool:
        sql = "SELECT is_allowed FROM Chats WHERE chat_id = ? LIMIT 1;"
        row = self.execute(sql, (chat_id,), fetchone=True)
        return bool(row and row[0])

    def set_chat_access(self, chat_id: int, allowed: bool) -> None:
        if self.chat_exists(chat_id):
            sql = "UPDATE Chats SET is_allowed = ? WHERE chat_id = ?;"
            self.execute(sql, (int(allowed), chat_id), commit=True)
        else:
            self.add_chat(chat_id, "", allowed)

    def set_chat_timezone(self, chat_id: int, timezone: str) -> None:
        if self.chat_exists(chat_id):
            sql = "UPDATE Chats SET timezone = ? WHERE chat_id = ?;"
            self.execute(sql, (timezone, chat_id), commit=True)
        else:
            self.add_chat(chat_id, "", False)
            self.set_chat_timezone(chat_id, timezone)

    def get_chat_timezone(self, chat_id: int) -> str:
        sql = "SELECT timezone FROM Chats WHERE chat_id = ? LIMIT 1;"
        row = self.execute(sql, (chat_id,), fetchone=True)
        return row[0] if row and row[0] else "+3"

    def set_timezone(self, telegram_id: int, timezone: str) -> None:
        if self.user_exists(telegram_id):
            sql = "UPDATE Users SET timezone = ? WHERE telegram_id = ?;"
            self.execute(sql, (timezone, telegram_id), commit=True)
        else:
            self.add_user(telegram_id, "", False)
            self.set_timezone(telegram_id, timezone)

    def get_timezone(self, telegram_id: int) -> str:
        sql = "SELECT timezone FROM Users WHERE telegram_id = ? LIMIT 1;"
        row = self.execute(sql, (telegram_id,), fetchone=True)
        return row[0] if row and row[0] else "+3"
