from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

user_kb = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="❓ Help"),
        KeyboardButton(text="❇️ Create Task"),
        KeyboardButton(text="⚙️ Settings"),
        ]],
    resize_keyboard=True,
    )

collect_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➡️ Continue")],
        [KeyboardButton(text="❌ Cancel")],
        ],
    resize_keyboard=True,
    )
