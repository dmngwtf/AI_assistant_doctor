# handlers/text_handler.py
# Handler for text messages

import logging
from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from services.symptom_processor import extract_symptoms, predict_disease, get_additional_symptoms
from services.recommendation import get_recommendations
from services.user_state import user_state, set_user_state, clear_user_state
from utils.audio_processing import text_to_speech
from aiogram.types import FSInputFile
from config.config import API_KEY1, API_KEY2, API_URL

logger = logging.getLogger(__name__)

def register_text_handler(dp: Dispatcher):
    @dp.message()
    async def handle_text(message: Message):
        user_id = message.from_user.id
        text = message.text.lower()
    
        try:
            if user_id in user_state:
                state = user_state[user_id]
                voice_mode = state.get("voice_mode", False)
                
                if "awaiting_response" in state:
                    symptom = state["current_symptom"]
                    if text in ["да", "нет"]:
                        if text == "да":
                            state["symptoms"].append(symptom)
                        state["current_index"] += 1
                        
                        if state["current_index"] < len(state["additional_symptoms"]):
                            next_symptom = state["additional_symptoms"][state["current_index"]]
                            state["current_symptom"] = next_symptom
                            markup = ReplyKeyboardMarkup(
                                keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
                                resize_keyboard=True,
                                one_time_keyboard=True
                            )
                            response = f"Есть ли у вас {next_symptom}?"
                            await message.reply(response, reply_markup=markup)
                            if voice_mode:
                                voice_file = await text_to_speech(response)
                                if voice_file:
                                    await message.answer_voice(voice=FSInputFile(voice_file))
                                    os.unlink(voice_file)
                        else:
                            disease = predict_disease(state["symptoms"], API_KEY1, API_URL)
                            recommendations = get_recommendations(disease, API_KEY2, API_URL)
                            response = (
                                f"Симптомы: {', '.join(state['symptoms'])}\n"
                                f"Диагноз: {disease}\n"
                                f"Рекомендации:\n{recommendations}"
                            )
                            await message.reply(response)
                            if voice_mode:
                                voice_file = await text_to_speech(response)
                                if voice_file:
                                    await message.answer_voice(voice=FSInputFile(voice_file))
                                    os.unlink(voice_file)
                            clear_user_state(user_id)
                    else:
                        response = "Пожалуйста, ответьте 'Да' или 'Нет'."
                        await message.reply(response)
                        if voice_mode:
                            voice_file = await text_to_speech(response)
                            if voice_file:
                                await message.answer_voice(voice=FSInputFile(voice_file))
                                os.unlink(voice_file)
                    return
    
            symptoms = extract_symptoms(text, API_KEY1, API_URL)
            if "Симптомы не найдены" in symptoms:
                response = "Не удалось найти симптомы в вашем сообщении. Пожалуйста, опишите их подробнее."
                await message.reply(response)
                return
    
            additional_symptoms = get_additional_symptoms(symptoms)
            if additional_symptoms:
                set_user_state(user_id, symptoms, additional_symptoms, voice_mode=False)
                markup = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
                await message.reply(f"Есть ли у вас {additional_symptoms[0]}?", reply_markup=markup)
            else:
                disease = predict_disease(symptoms, API_KEY1, API_URL)
                recommendations = get_recommendations(disease, API_KEY2, API_URL)
                response = (
                    f"Симптомы: {', '.join(symptoms)}\n"
                    f"Диагноз: {disease}\n"
                    f"Рекомендации:\n{recommendations}"
                )
                await message.reply(response)
    
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await message.reply("Произошла ошибка. Пожалуйста, попробуйте еще раз.")