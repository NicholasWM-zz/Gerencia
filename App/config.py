import os

SECRET_KEY = 'gerencia'
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
SEND_FILE_MAX_AGE_DEFAULT = 0