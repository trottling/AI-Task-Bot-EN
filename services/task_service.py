import json
import logging
from typing import Any, Optional

from ics.creator import ICSCreator
from loader import openai_service
from storage.sqlite import Database
from services.settings_service import SettingsService

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, db: Database, ics_creator: ICSCreator):
        self.db = db
        self.ics_creator = ics_creator
        self.settings_service = SettingsService(db)

    async def process_task_text(self, text: str, user_id: int, chat_id: int = None, message_chat_type: str = "private") -> dict[str, Any]:
        """
        Checks text, calls AI, saves request, returns result.
        Returns dict with keys: success, message, ai_response, ics_filename (if any).
        """
        if len(text) < 15:
            return { "success": False, "message": "```⛔️ Слишком маленькое сообщение```" }
        if len(text) > 750:
            return { "success": False, "message": "```⛔️ Слишком большое сообщение```" }

        # We get a time zone: priority is chat, then user, then +3
        tz = "+3"
        if message_chat_type != "private" and chat_id is not None:
            tz = self.settings_service.get_chat_timezone(chat_id)
        else:
            tz = self.settings_service.get_timezone(user_id)
        try:
            from datetime import datetime, timedelta, timezone
            offset = int(tz)
            now = datetime.now(timezone.utc) + timedelta(hours=offset)
            now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            now_str = None

        try:
            ai_response = await openai_service.ask(text, now_str)
            self.db.add_request(text, user_id, json.dumps(ai_response, ensure_ascii=False))
        except Exception as e:
            logger.exception(f"AI error: {e}")
            return { "success": False, "message": "❌ Failed to create task list:\n```No response```" }

        if not ai_response:
            return { "success": False, "message": "❌ Failed to create task list:\n```Empty response```" }
        if ai_response.get("error"):
            extra = f" {ai_response['response']}" if ai_response.get('response') else ""
            return { "success": False, "message": f"❌ Failed to create task list:\n```{ai_response['error']}{extra}```" }
        if "events_tasks" not in ai_response:
            return { "success": False, "message": "❌ Не failed to create task list:\n```JSON is missing field 'events_tasks```'" }

        event_tasks = [
            t for t in ai_response["events_tasks"]
            if t.get("type", "").strip().lower() in ["event", "task"]
            ]
        if not event_tasks:
            return { "success": True, "message": ai_response.get("response", "") }

        return {
            "success": True,
            "message": ai_response.get("response", ""),
            "ai_response": ai_response,
            "event_tasks": event_tasks,
            }

    def generate_ics(self, event_tasks: list[dict[str, Any]], tz: str = "+3") -> Optional[str]:
        ics_filename = self.ics_creator.create_ics({ "events_tasks": event_tasks }, tz=tz)
        return ics_filename
