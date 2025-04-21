# services/recommendation.py
# Treatment recommendation generation

from utils.api_client import call_grok_api
import logging

logger = logging.getLogger(__name__)

def get_recommendations(disease: str, api_key: str, api_url: str) -> str:
    system_prompt = """Ты — доктор с медицинским образованием, говорящий на русском языке. 
    Твоя задача — по диагнозу вывести рекомендации по лечению. 
    Выведи пронумерованный список рекомендаций.
    Формат:
    1. Рекомендация 1
    2. Рекомендация 2
    3. Рекомендация 3
    ...
    Пиши только рекомендации, без дополнительных комментариев."""
    
    user_prompt = f"Диагноз: {disease}"
    
    return call_grok_api(api_key, api_url, system_prompt, user_prompt, temperature=0.14, max_tokens=300)