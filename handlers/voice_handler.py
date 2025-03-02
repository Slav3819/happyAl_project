import logging
from aiogram import F, Router, Bot
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender
from config import settings
from openai import AsyncOpenAI
from pydub import AudioSegment
import io


client = AsyncOpenAI(api_key=settings.openai_api_key)

router = Router()

@router.message(F.voice)
async def handle_voice_message(message: Message):
    async with ChatActionSender.record_voice(chat_id=message.chat.id, bot=message.bot):
        try:

            file = await message.bot.get_file(message.voice.file_id)
            file_path = await message.bot.download_file(file.file_path)

            audio = AudioSegment.from_file(file_path, format="ogg")
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav")
            wav_buffer.seek(0)

            transcription = await client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", wav_buffer, "audio/wav")
            )
            user_text = transcription.text

            logging.info(f"Распознанный текст: {user_text}")

            await message.answer(f"Вы сказали: {user_text}")

            response = await get_openai_response(user_text)

            await message.answer(response)

            await send_voice_response(message.chat.id, response, message.bot)

        except Exception as e:
            logging.error(f"Ошибка при обработке голосового сообщения: {e}")
            await message.answer("Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз.")

async def get_openai_response(text: str) -> str:
    """Получаем ответ от OpenAI Assistant API."""

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content

async def send_voice_response(chat_id: int, text: str, bot: Bot):
    """Преобразуем текст в голос с помощью TTS API и отправляем пользователю."""
    try:
        tts_response = await client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        audio_buffer = io.BytesIO(tts_response.read())
        audio_buffer.seek(0)

        voice_file = BufferedInputFile(audio_buffer.read(), filename="response.mp3")

        await bot.send_voice(chat_id, voice=voice_file)

    except Exception as e:
        logging.error(f"Ошибка при озвучке ответа: {e}")
        await bot.send_message(chat_id, "Не удалось озвучить ответ. Вот текстовый ответ:")
        await bot.send_message(chat_id, text)