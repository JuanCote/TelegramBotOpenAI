from aiogram import Bot, types
from aiogram.dispatcher.storage import FSMContextProxy

from keyboards.back_to_menu import create_back_to_menu
from openai_services.openai_client import send_report_to_ai


async def reply_with_report_via_editing(
    bot: Bot, callback_query: types.CallbackQuery, data: FSMContextProxy
):
    """
    Receives a response from OpenAI and sends it to the user via message editing.
    """
    await bot.edit_message_text(
        text="😊 Дякую за заповнення чек-листа\n🔄 Відповідь від OpenAI буде незабаром",
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )
    openai_response = await send_report_to_ai(data)
    await bot.send_message(
        text=f"Відповідь OpenAI:\n{openai_response}",
        chat_id=callback_query.from_user.id,
        reply_markup=create_back_to_menu(),
    )
