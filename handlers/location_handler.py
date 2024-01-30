from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards.checklist_keyboard import create_checklist_keyboard

from state import UserState


async def handle_location(callback_query: types.CallbackQuery, state: FSMContext):
    location = callback_query.data.split("_")[1]
    bot = callback_query.bot

    async with state.proxy() as data:
        data["choosing_location"] = location

    await UserState.checklist.set()

    await bot.edit_message_text(
        f"Ви обрали локацію: {location}\nПункт 1",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=create_checklist_keyboard(),
    )


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        handle_location,
        lambda c: c.data and c.data.startswith("location_"),
        state=UserState.choosing_location,
    )
