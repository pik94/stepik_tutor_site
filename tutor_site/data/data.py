import json
from typing import Dict, NoReturn, Union

from tutor_site import config as cfg


class Data:
    def __init__(self):
        self._data = None

        cfg.REQUEST_FOLDER.mkdir(exist_ok=True)
        self._request_file = cfg.REQUEST_FOLDER / 'request.json'
        if not self._request_file.exists():
            with open(self._request_file, 'w') as file:
                json.dump({}, file)

        cfg.BOOKING_FOLDER.mkdir(exist_ok=True)
        self._booking_file = cfg.BOOKING_FOLDER / 'booking.json'
        if not self._booking_file.exists():
            with open(self._booking_file, 'w') as file:
                json.dump({}, file)

    @property
    def data(self) -> Dict[str, Dict[str, Union[int, str]]]:
        if self._data is None:
            if not cfg.DB_PATH.exists():
                raise ValueError('Database has not been initialized.')

            with open(cfg.DB_PATH, 'r') as file:
                self._data = json.load(file)

        return self._data

    def put_request_data(self, data: Dict[str, str]) -> NoReturn:
        with open(self._request_file, 'r') as file:
            request_data = json.load(file)
            if request_data:
                request_id = max(map(int, request_data)) + 1
            else:
                request_id = 1

        request_data[request_id] = data

        # TODO: do backup before writing

        with open(self._request_file, 'w') as file:
            json.dump(request_data, file, indent=4)

    def put_booking_data(self, data: Dict[str, Union[int, str]]) -> None:
        with open(self._booking_file, 'r') as file:
            booking_data = json.load(file)

            if booking_data:
                booking_id = max(map(int, booking_data)) + 1
            else:
                booking_id = 1

        booking_data[booking_id] = data

        # TODO: do backup before writing

        with open(self._booking_file, 'w') as file:
            json.dump(booking_data, file, indent=4)
