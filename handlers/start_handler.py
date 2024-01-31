from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from helpers.photo_saver import load_data
from openai_services.openai_client import send_report_to_ai

from keyboards.locations_keyboard import create_locations_keyboard
from state import UserState


GREETINGS = "👋 Привіт! Почнімо працювати!\n➡️ Обери локацію"


async def send_welcome(message: types.Message, state: FSMContext):
    """
    Sends a welcome message and a keyboard with locations on /start command.
    """
    await state.finish()
    await UserState.choosing_location.set()
    await message.answer(text=GREETINGS, reply_markup=create_locations_keyboard())


async def send_welcome_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Sends a welcome message and a keyboard with locations on back_to_locations callback.
    """
    bot = callback_query.bot
    await state.finish()
    await UserState.choosing_location.set()
    await bot.edit_message_text(
        text=GREETINGS,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=create_locations_keyboard(),
    )


def setup(dp: Dispatcher):
    dp.register_message_handler(
        send_welcome,
        commands=["start"],
        state="*",
    )
    dp.register_callback_query_handler(
        send_welcome_callback, lambda c: c.data == "back_to_locations", state="*"
    )
