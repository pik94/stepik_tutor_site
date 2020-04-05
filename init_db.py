import json

from tutor_site.config import DB_PATH
from tutor_site.data.raw_data import teachers


def main() -> None:
    data = {
        teacher['id']: {
            'id':       teacher['id'],
            'name':     teacher['name'],
            'about':    teacher['about'],
            'rating':   teacher['rating'],
            'picture':  teacher['picture'],
            'price':    teacher['price'],
            'goals':    teacher['goals'],
            'free':     teacher['free'],
        }
        for teacher in teachers
    }

    with open(DB_PATH, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    main()
