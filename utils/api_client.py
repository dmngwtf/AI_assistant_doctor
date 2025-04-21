# utils/api_client.py
# Functions for interacting with the Grok API

import requests
import logging

logger = logging.getLogger(__name__)

def call_grok_api(api_key, api_url, system_prompt, user_prompt, model="llama3-70b-8192", temperature=0.1, max_tokens=100):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Error calling API: {e}")
        return f"Error: {e}"