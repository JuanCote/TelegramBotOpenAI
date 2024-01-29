import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import start_handler, location_handler, checklist_handler

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


if __name__ == "__main__":
    start_handler.setup(dp)
    location_handler.setup(dp)
    checklist_handler.setup(dp)

    executor.start_polling(dp, skip_updates=True)
