# handlers/voice_handler.py
# Handler for voice messages

import os
import tempfile
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from utils.audio_processing import text_to_speech, transcribe_audio_with_sr
from services.symptom_processor import extract_symptoms, predict_disease, get_additional_symptoms
from services.recommendation import get_recommendations
from services.user_state import set_user_state
from config.config import VOSK_MODEL_PATH, API_KEY1, API_KEY2, API_URL

logger = logging.getLogger(__name__)

def register_voice_handler(dp: Dispatcher, bot: Bot):
    @dp.message(lambda message: message.voice is not None)
    async def handle_voice(message: Message):
        voice_file_path = None
        try:
            file_id = message.voice.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file:
                voice_file_path = temp_file.name
            
            await bot.download_file(file_path, voice_file_path)
            await message.reply("Обрабатываю ваше голосовое сообщение...")
            
            text = await transcribe_audio_with_sr(voice_file_path)
            
            if os.path.exists(voice_file_path):
                os.unlink(voice_file_path)
            
            if text:
                await message.reply(f"Вы сказали: {text}")
                
                symptoms = extract_symptoms(text, API_KEY1, API_URL)
                
                if "Симптомы не найдены" in symptoms:
                    response = "Не удалось найти симптомы в вашем сообщении. Пожалуйста, опишите их подробнее."
                    await message.reply(response)
                    voice_file = await text_to_speech(response)
                    if voice_file:
                        await message.answer_voice(voice=FSInputFile(voice_file))
                        os.unlink(voice_file)
                    return
                
                additional_symptoms = get_additional_symptoms(symptoms)
                user_id = message.from_user.id
                
                if additional_symptoms:
                    set_user_state(user_id, symptoms, additional_symptoms, voice_mode=True)
                    markup = ReplyKeyboardMarkup(
                        keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
                        resize_keyboard=True,
                        one_time_keyboard=True
                    )
                    response = f"Есть ли у вас {additional_symptoms[0]}?"
                    await message.reply(response, reply_markup=markup)
                    voice_file = await text_to_speech(response)
                    if voice_file:
                        await message.answer_voice(voice=FSInputFile(voice_file))
                        os.unlink(voice_file)
                else:
                    disease = predict_disease(symptoms, API_KEY1, API_URL)
                    recommendations = get_recommendations(disease, API_KEY2, API_URL)
                    response = (
                        f"Симптомы: {', '.join(symptoms)}\n"
                        f"Диагноз: {disease}\n"
                        f"Рекомендации:\n{recommendations}"
                    )
                    await message.reply(response)
                    voice_file = await text_to_speech(response)
                    if voice_file:
                        await message.answer_voice(voice=FSInputFile(voice_file))
                        os.unlink(voice_file)
            else:
                response = "Извините, я не смог распознать ваше голосовое сообщение. Пожалуйста, попробуйте еще раз."
                await message.reply(response)
                voice_file = await text_to_speech(response)
                if voice_file:
                    await message.answer_voice(voice=FSInputFile(voice_file))
                    os.unlink(voice_file)
                
        except Exception as e:
            logger.error(f"Error processing voice message: {e}")
            await message.reply("Произошла ошибка при обработке голосового сообщения.")
        finally:
            if voice_file_path and os.path.exists(voice_file_path):
                os.unlink(voice_file_path)