from aiogram.types import Message


async def help_command(message: Message) -> None:
    await message.answer(
        "ℹ️ The bot creates tasks for the calendar from a message\n\n"
        "1) Send the bot a message with a task, for example:\n"
        "January 20, driving at 10 o'clock, take your passport with you\n\n"
        "To create tasks in the chat, use the /create command\n\n"
        "2) Open the file that the bot sent and add events to any calendar - on Android, iPhone or PC\n\n"
        "Detailed instructions for working with answers to frequently asked questions:\nhttps://telegra.ph/FAQ--CHasto-zadavaemye-voprosy-po-AI-Task-Bot-07-03"
        )
