from openai import AsyncOpenAI
from config import settings
from pydub import AudioSegment
import io

client = AsyncOpenAI(api_key=settings.openai_api_key)

async def create_assistant():
    """Создает нового ассистента и возвращает его ID."""
    assistant = await client.beta.assistants.create(
        name="Telegram Bot Assistant",
        instructions="Полезный помощник, который отвечает на вопросы пользователей.",
        model="gpt-4-1106-preview"
    )
    settings.openai_assistant_id = assistant.id
    print(f"New id assistant {settings.openai_assistant_id}")
    return assistant.id

async def get_openai_response(text: str) -> str:
    """Получаем ответ от OpenAI Assistant API."""

    thread = await client.beta.threads.create()

    await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=settings.openai_assistant_id,
        poll_interval_ms=2000
    )

    while run.status != "completed":
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    messages = await client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value
    print(settings.openai_assistant_id)
    return response

async def get_openai_transcription(file_path):
    """Преобразование голосового в текст."""

    audio = AudioSegment.from_file(file_path, format="ogg")
    wav_buffer = io.BytesIO()
    audio.export(wav_buffer, format="wav")
    wav_buffer.seek(0)

    transcription = await client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", wav_buffer, "audio/wav")
    )
    await client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", wav_buffer, "audio/wav")
            )

    return transcription.text

async def get_openai_text(text):
    """Преобразование  текста в голосовое."""

    tts_response = await client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    audio_buffer = io.BytesIO(tts_response.read())
    audio_buffer.seek(0)

    return audio_buffer