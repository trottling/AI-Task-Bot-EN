from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔢 User stats"), KeyboardButton(text="🔢 Requests stats")],
        [KeyboardButton(text="🟢 Grant user access"), KeyboardButton(text="🔴 Remove user access")],
        [KeyboardButton(text="🟢 Grant chat access"), KeyboardButton(text="🔴 Remove chat access")],
        [KeyboardButton(text="◀️ Back")],
        ],
    resize_keyboard=True,
    )
