# services/user_state.py
# User state management

from typing import Dict, List

user_state: Dict[int, Dict] = {}

def set_user_state(user_id: int, symptoms: List[str], additional_symptoms: List[str], voice_mode: bool = False):
    user_state[user_id] = {
        "symptoms": symptoms,
        "additional_symptoms": additional_symptoms,
        "current_index": 0,
        "current_symptom": additional_symptoms[0] if additional_symptoms else None,
        "awaiting_response": True,
        "voice_mode": voice_mode
    }

def clear_user_state(user_id: int):
    if user_id in user_state:
        del user_state[user_id]