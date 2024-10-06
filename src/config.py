import os

class Config:
    EXTERNAL_BACKEND_URL = os.environ.get('EXTERNAL_BACKEND_URL', 'http://156.17.72.94/api/places')
    SEND_TO_EXTERNAL_API = os.environ.get('SEND_TO_EXTERNAL_API', 'False').lower() == 'true'
