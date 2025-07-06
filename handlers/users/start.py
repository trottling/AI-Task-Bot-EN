import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.user import user_kb
from loader import ADMINS, db
from utils.escape import escape
from .settings import settings_command

logger = logging.getLogger(__name__)


async def start_command(message: Message) -> None:
    if message.chat.type != "private":
        chat_id = message.chat.id
        try:
            db.add_chat(chat_id=chat_id, title=message.chat.title or "")
        except Exception as e:
            logger.exception(f"Failed to add chat to DB: {e}")

        if not db.has_chat_access(chat_id):
            await message.answer(f"🚫 The chat does not have access to the bot. Contact the administrator. Chat ID:\n```{escape(str(chat_id))}```", parse_mode="MarkdownV2")
            return

        await message.answer("✅ Bot activated in chat")
        return

    full_name = message.from_user.full_name
    telegram_id = message.from_user.id

    try:
        db.add_user(full_name=full_name, telegram_id=telegram_id)
    except Exception as e:
        logger.exception(f"Failed to add user to DB: {e}")

    if telegram_id not in ADMINS and not db.has_access(telegram_id):
        await message.answer(f"🚫 You do not have access to the bot. Contact the administrator.\nℹ️ Your ID: {telegram_id}")
        return

    await message.answer(text=f'👋 Hi {full_name}, click "Help" to understand how the bot works', reply_markup=user_kb)


async def help_command(message: Message) -> None:
    await message.answer(
        "ℹ️ The bot creates tasks for the calendar from a message\n\n"
        "1) Send the bot a message with a task, for example:\n"
        "January 20, driving at 10 o'clock, take your passport with you\n\n"
        "* To create tasks in the chat, use the /create command\n\n"
        "2) Open the files that the bot sent and add events to any calendar - on Android, iPhone or PC\n\n"
        "Detailed instructions for working with answers to frequently asked questions:\nhttps://telegra.ph/111-07-01-32",
        reply_markup=user_kb
        )


async def settings_menu_command(message: Message, state: FSMContext):
    await settings_command(message, state)


async def create_command(message: Message, state: FSMContext):
    from .ics import start_ics_creation
    await start_ics_creation(message, state)
