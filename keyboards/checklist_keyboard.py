from aiogram import types


def create_checklist_keyboard(checklist_order: int) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        keyboard.add(
            types.InlineKeyboardButton(
                text=button, callback_data=f"checklist_{checklist_order}_{button}"
            )
        )
    return keyboard


buttons = ["Все чисто", "Залишити коментар"]
