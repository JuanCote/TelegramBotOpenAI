from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from helpers.photo_saver import load_data
from helpers.reply_via_editing import reply_with_report_via_editing
from keyboards.checklist_keyboard import create_checklist_keyboard
from keyboards.refuse_from_image import create_refuse_image_keyboard
from keyboards.reuse_image_keyboard import create_reuse_image_keyboard

from state import UserState


async def handle_comment(message: types.Message, state: FSMContext):
    """
    Handles the user's comment message during checklist completion.
    """
    # Saving user's comment in state
    async with state.proxy() as data:
        location = data["choosing_location"].split(" ")[-1]
        checklist_order = len(data)
        data[f"checklist_{checklist_order}"] = {"comment": message.text}

    json_data = await load_data()
    user_id = str(message.from_user.id)
    await UserState.image.set()
    # Trying to get a photo added earlier to this question of this location
    try:
        image_url = json_data[user_id][location][str(checklist_order)]
        try:
            with open(image_url, "rb") as photo:
                await message.bot.send_photo(message.chat.id, photo)
            await message.answer(
                f"📂 Коментар збережно\nВи вже раніше завантажували фото до цього пункту цієї локації\nЧи бажаєте ви його використати\nЯкщо ні - завантажте нове фото",
                reply_markup=create_reuse_image_keyboard(),
            )
        except FileNotFoundError:
            raise KeyError
    except KeyError:
        await message.answer(
            f"📂 Коментар збережно\nТепер надішліть фото",
            reply_markup=create_refuse_image_keyboard(),
        )


async def handle_refusal_to_load_image(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """
    Handles the user's refucal from load image.
    """
    bot = callback_query.bot
    async with state.proxy() as data:
        checklist_order = len(data)
        data[f"checklist_{checklist_order - 1}"]["file_path"] = None
    if checklist_order <= 5:
        await UserState.checklist.set()
        await bot.edit_message_text(
            text=f"🧐 Запитання {checklist_order}",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=create_checklist_keyboard(),
        )
    else:
        await reply_with_report_via_editing(
            bot=bot, callback_query=callback_query, data=data
        )


def setup(dp: Dispatcher):
    dp.register_message_handler(
        handle_comment,
        state=UserState.comment,
    )
    dp.register_callback_query_handler(
        handle_refusal_to_load_image,
        lambda c: c.data == "refuse_load_image",
        state=UserState.image,
    )
