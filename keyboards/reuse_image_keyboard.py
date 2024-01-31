from aiogram import types


def create_reuse_image_keyboard() -> types.InlineKeyboardMarkup:
    """
    Creates a keyboard to use the old image.
    """
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.InlineKeyboardButton(
            text="Використати старе фото", callback_data="reuse_image"
        )
    )
    return keyboard
