from aiogram import types


def create_back_to_menu() -> types.InlineKeyboardMarkup:
    """
    Creates a keyboard to return to the start menu.
    """
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.InlineKeyboardButton(
            text="⬅️ Повернутися до вибору локацій", callback_data="back_to_locations"
        )
    )
    return keyboard
