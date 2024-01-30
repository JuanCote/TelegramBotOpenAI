from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from helpers.photo_saver import load_data
from keyboards.reuse_image_keyboard import create_reuse_image_keyboard

from state import UserState


async def handle_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        location = data["choosing_location"].split(" ")[-1]
        checklist_order = len(data)
        data[f"checklist_{checklist_order}"] = {"comment": message.text}

    json_data = await load_data()
    user_id = str(message.from_user.id)
    await UserState.image.set()
    try:
        image_url = json_data[user_id][location][str(checklist_order)]
        try:
            with open(image_url, "rb") as photo:
                await message.bot.send_photo(message.chat.id, photo)
            await message.answer(
                f"Коментар збережно\nВи вже раніше завантажували фото до цього пункту цієї локації\nЧи бажаєте ви його використати\nЯкщо ні - завантажте нове фото",
                reply_markup=create_reuse_image_keyboard(),
            )
        except FileNotFoundError:
            raise KeyError
    except KeyError:
        await message.answer(
            f"Коментар збережно\nТепер надішліть фото",
        )


def setup(dp: Dispatcher):
    dp.register_message_handler(
        handle_comment,
        state=UserState.comment,
    )
