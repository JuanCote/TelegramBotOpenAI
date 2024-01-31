from aiogram import types


def create_locations_keyboard():
    """
    Creates a keyboard with locations.
    """
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for location in locations:
        keyboard.add(
            types.InlineKeyboardButton(
                text=location, callback_data=f"location_{location}"
            )
        )
    return keyboard


locations = ["Локація 1", "Локація 2", "Локація 3", "Локація 4", "Локація 5"]
