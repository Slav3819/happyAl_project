import logging
from aiogram import F, Router, Bot
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender
from config import settings
from openai import AsyncOpenAI
import assistant

client = AsyncOpenAI(api_key=settings.openai_api_key)

router = Router()

@router.message(F.voice)
async def handle_voice_message(message: Message):
    async with ChatActionSender.record_voice(chat_id=message.chat.id, bot=message.bot):
        try:

            file = await message.bot.get_file(message.voice.file_id)
            file_path = await message.bot.download_file(file.file_path)

            user_text = await assistant.get_openai_transcription(file_path)

            logging.info(f"Распознанный текст: {user_text}")

            await message.answer(f"Вы сказали: {user_text}")

            response = await assistant.get_openai_response(user_text)

            await message.answer(response)

            await send_voice_response(message.chat.id, response, message.bot)

        except Exception as e:
            logging.error(f"Ошибка при обработке голосового сообщения: {e}")
            await message.answer("Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз.")

async def send_voice_response(chat_id: int, text: str, bot: Bot):
    """Преобразуем текст в голос с помощью TTS API и отправляем пользователю."""
    try:

        audio_buffer = await assistant.get_openai_text(text)

        voice_file = BufferedInputFile(audio_buffer.read(), filename="response.mp3")

        await bot.send_voice(chat_id, voice=voice_file)

    except Exception as e:
        logging.error(f"Ошибка при озвучке ответа: {e}")
        await bot.send_message(chat_id, "Не удалось озвучить ответ. Вот текстовый ответ:")
        await bot.send_message(chat_id, text)