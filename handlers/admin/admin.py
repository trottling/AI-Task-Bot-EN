import logging
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from keyboards.admin import admin_kb
from loader import db
from services.admin_service import AdminService
from utils.escape import escape

logger = logging.getLogger(__name__)

admin_service = AdminService(db)

class GrantAccess(StatesGroup):
    waiting_for_id = State()
    waiting_for_chat_id = State()

class RevokeAccess(StatesGroup):
    waiting_for_id = State()
    waiting_for_chat_id = State()

async def is_admin(message: Message) -> None:
    await message.answer(text="✅ Admin panel", reply_markup=admin_kb)

async def users_count(message: Message) -> None:
    count = admin_service.get_users_count()
    await message.answer(f"✅ In the db ```{count}``` users", reply_markup=admin_kb, parse_mode="MarkdownV2")

async def reqs_count(message: Message) -> None:
    count = admin_service.get_reqs_count()
    await message.answer(f"✅ There are ```{count}``` requests in the db", reply_markup=admin_kb, parse_mode="MarkdownV2")

async def allow_access_prompt(message: Message, state: FSMContext) -> None:
    await state.set_state(GrantAccess.waiting_for_id)
    await message.answer("✏️ Enter user ID to grant access:", reply_markup=admin_kb)

async def allow_chat_prompt(message: Message, state: FSMContext) -> None:
    await state.set_state(GrantAccess.waiting_for_chat_id)
    await message.answer("✏️ Enter the chat ID to grant access:", reply_markup=admin_kb)

async def allow_access(message: Message, state: FSMContext) -> None:
    await state.clear()
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Incorrect ID", reply_markup=admin_kb)
        return
    result = admin_service.set_user_access(user_id, True)
    if result["success"]:
        await message.answer(f"✅ User @{message.from_user.username} has been granted access\n```{escape(str(user_id))}```", reply_markup=admin_kb, parse_mode="MarkdownV2")
    else:
        await message.answer(f"❌ Access Grant Error: {result.get('error', '')}", reply_markup=admin_kb)

async def allow_chat(message: Message, state: FSMContext) -> None:
    await state.clear()
    try:
        chat_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Incorrect ID", reply_markup=admin_kb)
        return
    result = admin_service.set_chat_access(chat_id, True)
    if result["success"]:
        await message.answer(f"✅ Chat access granted\n```{escape(str(chat_id))}```", reply_markup=admin_kb, parse_mode="MarkdownV2")
    else:
        await message.answer(f"❌ Error granting access to chat: {result.get('error', '')}", reply_markup=admin_kb)

async def deny_access_prompt(message: Message, state: FSMContext) -> None:
    await state.set_state(RevokeAccess.waiting_for_id)
    await message.answer("✏️ Enter user ID to deny access:", reply_markup=admin_kb)

async def deny_chat_prompt(message: Message, state: FSMContext) -> None:
    await state.set_state(RevokeAccess.waiting_for_chat_id)
    await message.answer("✏️ Enter chat ID to deny access:", reply_markup=admin_kb)

async def deny_access(message: Message, state: FSMContext) -> None:
    await state.clear()
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Incorrect ID", reply_markup=admin_kb)
        return
    result = admin_service.set_user_access(user_id, False)
    if result["success"]:
        await message.answer(f"✅ User @{message.from_user.username} has been denied access\n```{escape(str(user_id))}```", reply_markup=admin_kb, parse_mode="MarkdownV2")
    else:
        await message.answer(f"❌ Access Denied Error: {result.get('error', '')}", reply_markup=admin_kb)

async def deny_chat(message: Message, state: FSMContext) -> None:
    await state.clear()
    try:
        chat_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Incorrect ID", reply_markup=admin_kb)
        return
    result = admin_service.set_chat_access(chat_id, False)
    if result["success"]:
        await message.answer(f"✅ Chat access denied\n```{escape(str(chat_id))}```", reply_markup=admin_kb, parse_mode="MarkdownV2")
    else:
        await message.answer(f"❌ Chat access denied error: {result.get('error', '')}", reply_markup=admin_kb)
