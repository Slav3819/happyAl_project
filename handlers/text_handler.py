from aiogram import F, Router
from aiogram.types import Message
import logging
from handlers import voice_handler
import assistant

router = Router()

@router.message(F.text)
async def handle_text_message(message: Message):
    try:

        response = await assistant.get_openai_response(message.text)

        await message.answer(response)

        await voice_handler.send_voice_response(message.chat.id, response, message.bot)

    except Exception as e:
        logging.error(f"Ошибка при обработке текстового сообщения: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз.")

