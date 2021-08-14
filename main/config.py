import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_PATH = Path(__file__).parent.parent

TEMPLATES_PATH = BASE_PATH / "main" / "templates"
TEMPLATE_FILE = "message.html"

# Telegram bot token generated from BotFather.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HURMA_HOST = os.getenv("HURMA_HOST")
HURMA_EMAIL = os.getenv("HURMA_EMAIL")
HURMA_PASSWORD = os.getenv("HURMA_PASSWORD")
