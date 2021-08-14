import os

from dotenv import load_dotenv

load_dotenv()

# Telegram bot token generated from BotFather.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

HURMA_HOST = os.getenv("HURMA_HOST")
HURMA_EMAIL = os.getenv("HURMA_EMAIL")
HURMA_PASSWORD = os.getenv("HURMA_PASSWORD")
