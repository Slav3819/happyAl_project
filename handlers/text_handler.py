from aiogram import F, Router
from aiogram.types import Message
from config import settings
from openai import AsyncOpenAI
import logging
from handlers import voice_handler

client = AsyncOpenAI(api_key=settings.openai_api_key)

router = Router()

@router.message(F.text)
async def handle_text_message(message: Message):
    try:

        response = await get_openai_response(message.text)

        await message.answer(response)

        await voice_handler.send_voice_response(message.chat.id, response, message.bot)

    except Exception as e:
        logging.error(f"Ошибка при обработке текстового сообщения: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз.")

async def get_openai_response(text: str) -> str:
    """Получаем ответ от OpenAI Assistant API."""
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content