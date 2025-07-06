# AI Task Bot

AI Task Bot is a Telegram bot that converts text messages into regular tasks and calendar events. The bot extracts structured data from text via the OpenAI API (or a compatible service) and can generate `.ics` files for import into any calendar.

## Key features

- Automatic extraction of events and tasks from written requests;
- Generation of imported `.ics` files;
- Minimalistic logs in Russian;
- Support for launching in Docker.

The bot can be added to group chats. To call commands in a group, use the
format `/command@BotName`.

## Requirements

- Python 3.11+
- Dependencies from `requirements.txt`

## Quickstart

1. Clone the repository and create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and fill in the variables:
- `BOT_TOKEN` — your bot token
- `ADMINS` — admin IDs
- `AI_API_KEY` — AI access key
- `AI_API_MODEL` — model to process
- `AI_API_URL` — service address
- `AI_PROXY_URL` — proxy if needed, for example `socks5://user:pass@1.1.1.1:1234`
4. Run the bot:
```bash
python main.py
```

After launching, you can use the `/start`, `/help` and `/create` commands in the chat.

## Launching in Docker

For simplified deployment, you can use Docker:

```bash
docker-compose up -d
```

The `storage` folder is mounted to store the database.

## Access control

By default, the bot is inaccessible to all users except for the IDs specified in the `ADMINS` variable. Administrators can grant and revoke access directly from the
admin menu. Similarly, you can allow or prohibit the use of the bot in group chats. The access state is saved in the `storage/main.db` SQLite database.

## Setup and update

- The `config/system_prompt.txt`, `config/user_prompt.txt` and `config/schema.json` files allow you to change the bot logic for your tasks;

## Example .env

```env
BOT_TOKEN=your-telegram-bot-token
ADMINS=123456789,987654321
AI_API_KEY=your-openai-key
AI_API_MODEL=gpt-3.5-turbo
AI_API_URL=https://api.openai.com/v1
AI_PROXY_URL=
```

## Project structure

- `ai/` — working with the AI ​​model;
- `handlers/` — telegram commands and response formats;
- `ics/` — generating `.ics` files;
- `storage/` — a simple SQLite database for storing queries.

## License

The project is distributed under the BSD-3-Clause license.