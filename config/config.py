from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = list(map(int, env.list("ADMINS")))
AI_API_KEY = env.str("AI_API_KEY")
AI_API_MODEL = env.str("AI_API_MODEL")
AI_API_URL = env.str("AI_API_URL")
AI_PROXY_URL = env.str("AI_PROXY_URL")

with open("./config/schema.json", "r", encoding="utf-8") as f:
    AI_SCHEMA = f.read()

with open("./config/system_prompt.txt", "r", encoding="utf-8") as f:
    AI_SYSTEM_PROMPT = f.read()

with open("./config/user_prompt.txt", "r", encoding="utf-8") as f:
    AI_USER_PROMPT = f.read()

