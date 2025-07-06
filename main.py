import asyncio
import logging
import sys

from commands.default import set_default_commands
from handlers import register_handlers
from loader import ADMINS, bot, dp


async def main() -> None:
    await register_handlers(dp, ADMINS)
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    asyncio.run(main())

