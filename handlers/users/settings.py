import logging
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.user import user_kb
from loader import db
from services.settings_service import SettingsService

logger = logging.getLogger(__name__)

settings_service = SettingsService(db)
router = Router()


@router.message(lambda msg: msg.text == "⚙️ Settings")
async def settings_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Available settings:\n\n"
                         "/timezone - set the time zone for tasks, for example timezone +3. By default +3.",
                         reply_markup=user_kb)


@router.message(Command("timezone"))
async def set_timezone_command(message: Message) -> None:
    args = message.text.split()
    if message.chat.type == "private":
        if len(args) == 2:
            tz = args[1]
            if tz.startswith("+") or tz.startswith("-"):
                try:
                    int(tz)
                    settings_service.set_timezone(message.from_user.id, tz)
                    await message.answer(f"Your time zone is set to UTC{tz}")
                    return
                except ValueError:
                    pass
            await message.answer("Incorrect format. Example: /timezone +3")
        else:
            await message.answer("Specify zone: /timezone +3")
    else:
        if len(args) == 2:
            tz = args[1]
            if tz.startswith("+") or tz.startswith("-"):
                try:
                    int(tz)
                    settings_service.set_chat_timezone(message.chat.id, tz)
                    await message.answer(f"Chat timezone is set to UTC{tz}")
                    return
                except ValueError:
                    pass
            await message.answer("Incorrect format. Example: /timezone +3")
        else:
            await message.answer("Specify zone: /timezone +3")
