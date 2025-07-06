import logging
import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.user import collect_kb, user_kb
from loader import bot, db, ics_creator
from services.task_service import TaskService

logger = logging.getLogger(__name__)

task_service = TaskService(db=db, ics_creator=ics_creator)

router = Router()


class TaskCreation(StatesGroup):
    collecting_tasks = State()
    generating = State()


async def start_ics_creation(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == TaskCreation.collecting_tasks.state:
        await message.answer('⛔️ You have already started composing tasks. Submit all tasks and click "**Continue**".', reply_markup=collect_kb, parse_mode="MarkdownV2")
        return

    await state.clear()
    await state.set_state(TaskCreation.collecting_tasks)
    await state.update_data(tasks=[])
    await message.answer('✍️ Send or forward messages with tasks.\nWhen you are finished, click "Continue"".\n\nℹ️ The bot understands the essence, time, place and Eisenhower square', reply_markup=collect_kb)


@router.message(TaskCreation.collecting_tasks, lambda m: m.text and m.text.strip() not in ["➡️ Continue", "❌ Отмена"])
async def collect_task_message(message: Message, state: FSMContext):
    data = await state.get_data()
    tasks = data.get("tasks", [])
    tasks.append(message.text.strip())
    await state.update_data(tasks=tasks)
    await message.answer("✅ Added!\nYou can send another task or click 'Continue''.", reply_markup=collect_kb)


@router.message(TaskCreation.collecting_tasks, lambda m: m.text == "❌ Cancel")
async def cancel_task_collection(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Task creation cancelled.", reply_markup=user_kb)


@router.message(TaskCreation.collecting_tasks, lambda m: m.text == "➡️ Continue")
async def finish_task_collection(message: Message, state: FSMContext):
    data = await state.get_data()
    tasks = data.get("tasks", [])
    if not tasks:
        await message.answer("❌ You have not submitted any tasks. Please submit at least one task..", reply_markup=collect_kb)
        return

    await state.set_state(TaskCreation.generating)
    await message.answer("🔄 Task generation...", reply_markup=user_kb)
    await state.clear()

    # We combine all tasks into one text using line breaks
    all_text = "\n".join(tasks)
    result = await task_service.process_task_text(text=all_text, user_id=message.from_user.id, chat_id=message.chat.id, message_chat_type=message.chat.type)

    if not result.get("success"):
        await message.answer(result["message"], reply_markup=user_kb, parse_mode="MarkdownV2")
        return

    await message.answer(result["message"], reply_markup=user_kb, parse_mode="MarkdownV2")

    event_tasks = result.get("event_tasks")
    if not event_tasks:
        return

    ics_filename = task_service.generate_ics(event_tasks)
    if not ics_filename:
        logger.error("Failed to create ICS file")
        await message.answer("❌ Failed to generate ICS file for transferred events", reply_markup=user_kb, parse_mode="MarkdownV2")
        return

    try:
        await send_ics_file(message.chat.id, ics_filename)
    finally:
        try:
            os.unlink(ics_filename)
        except OSError as e:
            logger.exception(f"Failed to delete temporary file {ics_filename}: {e}")


async def send_ics_file(chat_id: int, ics_filename: str) -> None:
    """Send ICS file to user."""
    if not os.path.exists(ics_filename):
        logger.error(f"File {ics_filename} not found")
        return

    try:
        await bot.send_document(chat_id, FSInputFile(ics_filename))
    except Exception as e:
        logger.exception(f"Error sending ICS: {e}")


@router.message(Command("create"))
async def create_from_reply(message: Message):
    if message.chat.type == "private":
        await message.answer("ℹ️ Use **/create** in group chats in response to a message", parse_mode="MarkdownV2")
        return

    if not message.reply_to_message or not message.reply_to_message.text:
        await message.answer("ℹ️ Use **\/create** in response to a task message\.", parse_mode="MarkdownV2")
        return

    await message.answer("🔄 Task generation...")

    result = await task_service.process_task_text(text=message.reply_to_message.text.strip(), user_id=message.from_user.id, chat_id=message.chat.id, message_chat_type=message.chat.type)
    if not result.get("success"):
        await message.answer(result["message"])
        return

    await message.answer(result["message"])

    event_tasks = result.get("event_tasks")
    if not event_tasks:
        return

    ics_filename = task_service.generate_ics(event_tasks)
    if not ics_filename:
        logger.error("Failed to create ICS file")
        await message.answer("❌ Failed to generate ICS file for transferred events")
        return

    try:
        await send_ics_file(message.chat.id, ics_filename)
    finally:
        try:
            os.unlink(ics_filename)
        except OSError as e:
            logger.exception(f"Failed to delete temporary file {ics_filename}: {e}")
