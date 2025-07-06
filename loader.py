import httpx
from aiogram import Bot, Dispatcher, Router
from openai import AsyncOpenAI

from ai.service import OpenAIService
from config import config
from config.config import AI_API_MODEL, AI_SCHEMA, AI_SYSTEM_PROMPT, AI_USER_PROMPT
from ics.creator import ICSCreator
from storage.sqlite import Database

# Bot
ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN

router = Router()
bot = Bot(TOKEN)
db = Database(path_to_db="storage/main.db")
dp = Dispatcher()
ics_creator = ICSCreator()

# Ai
AI_API_KEY = config.AI_API_KEY
AI_API_URL = config.AI_API_URL
PROXY_URL = config.AI_PROXY_URL

if not AI_API_URL:
    AI_API_URL = None
else:
    AI_API_URL = AI_API_URL.rstrip("/")
    if not AI_API_URL.endswith("/v1"):
        AI_API_URL += "/v1"

if PROXY_URL:
    http_client = httpx.AsyncClient(proxy=PROXY_URL)
    ai_client = AsyncOpenAI(
        api_key=AI_API_KEY,
        base_url=AI_API_URL,
        http_client=http_client
        )
else:
    ai_client = AsyncOpenAI(
        api_key=AI_API_KEY,
        base_url=AI_API_URL)

# Инициализация сервиса OpenAI
openai_service = OpenAIService(
    api_client=ai_client,
    model=AI_API_MODEL,
    schema=AI_SCHEMA,
    system_prompt=AI_SYSTEM_PROMPT,
    user_prompt=AI_USER_PROMPT,
    )
