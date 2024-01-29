from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards.checklist_keyboard import create_checklist_keyboard

from state import UserState


async def handle_checklist(callback_query: types.CallbackQuery, state: FSMContext):
    checklist_order = callback_query.data.split("_")[1]
    bot = callback_query.bot

    async with state.proxy() as data:
        data["checklist_1"] = checklist_order

    await UserState.next()

    await bot.edit_message_text(
        f"checklist",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        handle_checklist,
        lambda c: c.data and c.data.startswith("checklist_"),
        state=UserState.checklist_1,
    )
