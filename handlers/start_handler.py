from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def handle_start(message: types.Message):
    welcome_text = (
        "Привет! 👋\n"
        "Я — голосовой AI-бот. Вот что я умею:\n"
        "1. Принимать голосовые сообщения и преобразовывать их в текст.\n"
        "2. Отвечать на ваши вопросы с помощью AI.\n"
        "3. Озвучивать ответы голосом.\n\n"
        "Просто отправьте мне голосовое сообщение или текст, и я постараюсь помочь!"
    )
    await message.answer(welcome_text)
