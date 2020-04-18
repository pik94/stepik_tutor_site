import os
import uuid


GOALS = {'travel': 'Для путешествий', 'study': 'Для учебы',
         'work': 'Для работы', 'relocate': 'Для переезда',
         'development': 'Для программирования',
         }
TIMES = ['1-2', '3-5', '5-7', '7-10']


DAY_MAPPING = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресенье'
}

# Database credentials
DB_TYPE = 'postgresql'
DB_TYPE = os.environ.get('DB_TYPE', DB_TYPE)
DB_HOST = 'localhost'
DB_HOST = os.environ.get('DB_HOST', DB_HOST)
DB_PORT = 5432
DB_PORT = os.environ.get('DB_PORT', DB_PORT)
DB_USER = 'pik'
DB_USER = os.environ.get('DB_USER', DB_USER)
DB_PASSWORD = '123'
DB_PASSWORD = os.environ.get('DB_PASSWORD', DB_PASSWORD)
DB_NAME = 'tutordb'
DB_NAME = os.environ.get('DB_NAME', DB_NAME)

# Server credentials
SERVER_HOST = 'localhost'
SERVER_HOST = os.environ.get('SERVER_HOST', SERVER_HOST)
SERVER_PORT = 5000
SERVER_PORT = os.environ.get('SERVER_PORT', SERVER_PORT)

# Security
CSRF_TOKEN = str(uuid.uuid4())
CSRF_TOKEN = os.environ.get('CRSF_TOKEN', CSRF_TOKEN)
