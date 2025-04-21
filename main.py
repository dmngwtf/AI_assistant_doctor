# main.py
# Entry point for the medical bot

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.config import TELEGRAM_BOT_TOKEN
from utils.logging_setup import setup_logging
from handlers.start_handler import register_start_handler
from handlers.voice_handler import register_voice_handler
from handlers.text_handler import register_text_handler

logger = setup_logging()

async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    
    # Register handlers
    register_start_handler(dp)
    register_voice_handler(dp, bot)
    register_text_handler(dp)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())