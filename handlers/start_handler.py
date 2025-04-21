# handlers/start_handler.py
# Handler for /start command

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

def register_start_handler(dp: Dispatcher):
    @dp.message(Command("start"))
    async def start_command(message: Message):
        welcome_message = (
            "Добро пожаловать! Я бот, который помогает определить возможный диагноз по симптомам.\n"
            "Просто напишите или опишите голосом свои симптомы (например, 'кашель, температура'), и я постараюсь помочь.\n"
            "Обратите внимание: это не заменяет консультацию врача!"
        )
        await message.reply(welcome_message)