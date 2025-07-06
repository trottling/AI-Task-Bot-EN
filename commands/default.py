from aiogram import Bot
from aiogram.methods.set_my_commands import BotCommand
from aiogram.types import BotCommandScopeDefault


async def set_default_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="🔁 Restart the bot"),
        BotCommand(command="/help", description="❓ Help"),
        BotCommand(command="/create", description="❇️ Create tasks"),
        BotCommand(command="/timezone", description="🌍 Set the time zone (e.g., /timezone +3)")
        ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
