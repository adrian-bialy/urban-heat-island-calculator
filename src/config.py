import os

class Config:
    SEND_TO_EXTERNAL_API = os.getenv('SEND_TO_EXTERNAL_API', 'False') == 'True'
    EXTERNAL_BACKEND_URL = os.getenv('EXTERNAL_BACKEND_URL', 'http://156.17.72.94/api/places')
