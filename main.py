import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import (
    start_handler,
    location_handler,
    checklist_handler,
    сomment_handler,
    image_handler,
)

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

start_handler.setup(dp)
location_handler.setup(dp)
checklist_handler.setup(dp)
сomment_handler.setup(dp)
image_handler.setup(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
