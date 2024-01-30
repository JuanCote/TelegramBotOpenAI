import os
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
import aiohttp
from helpers.photo_saver import download_photo, load_data
from helpers.reply_via_editing import reply_with_report_via_editing
from keyboards.checklist_keyboard import create_checklist_keyboard
from openai_services.openai_client import send_report_to_ai

from state import UserState


PHOTOS_DIR = "images"


async def handle_image(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        location = data["choosing_location"].split(" ")[-1]
        checklist_order = len(data) - 1
        file_path = await download_photo(
            message=message, location=location, checklist_order=str(checklist_order)
        )
        data[f"checklist_{checklist_order}"]["file_path"] = file_path
    if checklist_order >= 5:
        await message.answer(
            text="Дякую за заповнення чек-листа\nВідповідь від OpenAI буде незабаром",
        )
        openai_response = await send_report_to_ai(data)
        await message.answer(
            text=f"Відповідь OpenAI:\n{openai_response}",
        )
    else:
        await UserState.checklist.set()
        await message.answer(
            text=f"Пункт {checklist_order + 1}",
            reply_markup=create_checklist_keyboard(),
        )


async def reuse_image(callback_query: types.CallbackQuery, state: FSMContext):
    bot = callback_query.bot
    json_data = await load_data()
    user_id = str(callback_query.from_user.id)
    async with state.proxy() as data:
        location = data["choosing_location"].split(" ")[-1]
        checklist_order = len(data) - 1
        data[f"checklist_{checklist_order}"]["file_path"] = json_data[user_id][
            location
        ][str(checklist_order)]
    if checklist_order >= 5:
        await reply_with_report_via_editing(
            bot=bot, callback_query=callback_query, data=data
        )
    else:
        await UserState.checklist.set()
        await bot.edit_message_text(
            f"Пункт {checklist_order + 1}",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=create_checklist_keyboard(),
        )


def setup(dp: Dispatcher):
    dp.register_message_handler(
        handle_image, state=UserState.image, content_types=types.ContentType.PHOTO
    )
    dp.register_callback_query_handler(
        reuse_image, lambda c: c.data == "reuse_image", state=UserState.image
    )
