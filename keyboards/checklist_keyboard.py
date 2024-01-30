from aiogram import types


def create_checklist_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        keyboard.add(
            types.InlineKeyboardButton(text=button, callback_data=f"checklist_{button}")
        )
    return keyboard


buttons = ["Все чисто", "Залишити коментар"]
