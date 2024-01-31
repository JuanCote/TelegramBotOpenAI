from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from helpers.reply_via_editing import reply_with_report_via_editing
from keyboards.checklist_keyboard import create_checklist_keyboard

from state import UserState


async def handle_checklist(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Handles the user's choices on the question.
    """
    callback_response = callback_query.data.split("_")[1]
    bot = callback_query.bot

    if callback_response == "clean":
        async with state.proxy() as data:
            checklist_order = len(data)
            data[f"checklist_{checklist_order}"] = {
                "comment": "Все чисто",
                "file_path": None,
            }
        # Check for question order. If more than 5 then the checklist is over
        if checklist_order < 5:
            await bot.edit_message_text(
                text=f"🧐 Запитання {checklist_order + 1}",
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                reply_markup=create_checklist_keyboard(),
            )
        else:
            await reply_with_report_via_editing(
                bot=bot, callback_query=callback_query, data=data
            )
    # Option when the user chose to write a comment
    else:
        await UserState.comment.set()

        await bot.edit_message_text(
            f"✍️ Напишіть коментар",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        handle_checklist,
        lambda c: c.data and c.data.startswith("checklist_"),
        state=UserState.checklist,
    )
