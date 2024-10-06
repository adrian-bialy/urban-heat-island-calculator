# src/services/external_api.py

import requests
from flask import current_app

def send_to_external_backend(url, data):
    try:
        response = requests.post(url, json=data, timeout=10000)
        response.raise_for_status()
        return True, response.text
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Failed to send data to external backend: {e}")
        return False, str(e)
