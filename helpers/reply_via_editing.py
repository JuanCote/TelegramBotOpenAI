import asyncio
import time
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
    openai_task = asyncio.create_task(send_report_to_ai(data))
    asyncio.create_task(
        update_interface(
            bot=bot,
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            openai_task=openai_task,
        )
    )
    openai_response = await openai_task
    await bot.send_message(
        text=f"Відповідь OpenAI:\n{openai_response}",
        chat_id=callback_query.from_user.id,
        reply_markup=create_back_to_menu(),
    )


async def update_interface(
    bot: Bot,
    chat_id: int,
    message_id: int,
    openai_task: asyncio.Task,
):
    """
    Updates the user interface with the specified message while waiting for the OpenAI task to complete.
    """
    flag = True
    sec_counter = 0
    while not openai_task.done():
        if flag:
            flag = False
            text = "⏳"
        else:
            flag = True
            text = "⌛️"
        await asyncio.sleep(1)  # Update every second
        await bot.edit_message_text(
            text=f"😊 Дякую за заповнення чек-листа\n🔄 Відповідь від OpenAI буде незабаром\n🕒 Процес обробки триває {text} {sec_counter} сек",
            chat_id=chat_id,
            message_id=message_id,
        )
        sec_counter += 1
