from aiogram import types


def create_refuse_image_keyboard():
    """
    Creates a keyboard with a button to refuse to upload photo.
    """
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🚫 Не завантажувати фото", callback_data="refuse_load_image"
        )
    )
    return keyboard
