# services/symptom_processor.py
# Symptom extraction and disease prediction

from typing import List, Set
from utils.api_client import call_grok_api
from database import SYMPTOMS_DISEASES
import logging

logger = logging.getLogger(__name__)

def extract_symptoms(text: str, api_key: str, api_url: str) -> List[str]:
    system_prompt = """Ты — доктор с медицинским образованием, говорящий на русском языке. 
    Твоя задача — извлечь симптомы из текста, описывающего состояние пациента. 
    Верни симптомы в виде списка, разделенного запятыми. 
    Если симптомы не найдены, верни "Симптомы не найдены".
    Формат ответа: "Симптомы: симптом1, симптом2, симптом3" или "Симптомы: Симптомы не найдены" """
    
    user_prompt = f"Текст: {text}"
    
    response_text = call_grok_api(api_key, api_url, system_prompt, user_prompt, temperature=0.05, max_tokens=100)
    
    if response_text.startswith("Симптомы: "):
        symptoms_part = response_text.replace("Симптомы: ", "").strip()
        if symptoms_part == "Симптомы не найдены":
            return ["Симптомы не найдены"]
        return [symptom.strip() for symptom in symptoms_part.split(",")]
    else:
        return ["Симптомы не найдены"]

def predict_disease(symptoms: List[str], api_key: str, api_url: str) -> str:
    possible_diseases: Set[str] = set()
    for symptom in symptoms:
        if symptom in SYMPTOMS_DISEASES:
            possible_diseases.update(SYMPTOMS_DISEASES[symptom])
    
    if not possible_diseases:
        return "Диагноз не определен"
    
    system_prompt = """Ты — доктор с медицинским образованием, говорящий на русском языке. 
    Твоя задача — определить наиболее вероятный диагноз на основе списка симптомов и возможных заболеваний. 
    Верни только название диагноза без дополнительных объяснений."""
    
    user_prompt = (
        f"Симптомы: {', '.join(symptoms)}\n"
        f"Возможные заболевания: {', '.join(possible_diseases)}"
    )
    
    predicted_disease = call_grok_api(api_key, api_url, system_prompt, user_prompt, temperature=0.1, max_tokens=50)
    
    return predicted_disease if predicted_disease else list(possible_diseases)[0] if possible_diseases else "Диагноз не определен"

def get_additional_symptoms(symptoms: List[str]) -> List[str]:
    possible_diseases = set()
    for symptom in symptoms:
        if symptom in SYMPTOMS_DISEASES:
            possible_diseases.update(SYMPTOMS_DISEASES[symptom])
    
    all_related_symptoms = set()
    for disease in possible_diseases:
        for symp, diseases in SYMPTOMS_DISEASES.items():
            if disease in diseases:
                all_related_symptoms.add(symp)
    
    additional_symptoms = [s for s in all_related_symptoms if s not in symptoms]
    return additional_symptoms[:3] if len(additional_symptoms) >= 3 else additional_symptoms