from aiogram import types


def create_reuse_image_keyboard() -> types.InlineKeyboardMarkup:
    """
    Creates a keyboard to use the old image.
    """
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        keyboard.add(
            types.InlineKeyboardButton(text=button[0], callback_data=button[1])
        )
    return keyboard


buttons = (
    ("👌 Використати старе фото", "reuse_image"),
    ("🚫 Не завантажувати фото", "refuse_load_image"),
)
