import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import settings
import assistant
from handlers import start_handler, text_handler, voice_handler

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

dp.include_router(start_handler.router)
dp.include_router(voice_handler.router)
dp.include_router(text_handler.router)

async def main():
    await assistant.create_assistant()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
