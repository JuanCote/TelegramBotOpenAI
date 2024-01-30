from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from helpers.photo_saver import load_data
from openai_services.openai_client import send_report_to_ai

from keyboards.locations_keyboard import create_locations_keyboard
from state import UserState


async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await UserState.choosing_location.set()
    await message.answer(
        text="Привіт! Почнімо працювати.", reply_markup=create_locations_keyboard()
    )


def setup(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start"], state="*")
