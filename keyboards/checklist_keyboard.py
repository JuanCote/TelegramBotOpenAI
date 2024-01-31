from aiogram import types


def create_checklist_keyboard() -> types.InlineKeyboardMarkup:
    """
    Creates a keyboard to answer a question.
    """
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        keyboard.add(
            types.InlineKeyboardButton(
                text=button[0], callback_data=f"checklist_{button[1]}"
            )
        )
    return keyboard


buttons = (("👌 Все чисто", "clean"), ("💬 Залишити коментар", "comment"))
