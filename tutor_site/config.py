from pathlib import Path

ROOT_PATH = Path(__file__).parent

DB_PATH = ROOT_PATH / 'db.json'
REQUEST_FOLDER = ROOT_PATH / 'requests'
BOOKING_FOLDER = ROOT_PATH / 'booking'

GOALS = {"travel": "Для путешествий", "study": "Для учебы",
         "work": "Для работы", "relocate": "Для переезда"}

DAY_MAPPING = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресенье'
}
