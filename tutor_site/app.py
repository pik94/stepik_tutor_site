import json
import random
from typing import Dict, List, Optional, Union

from flask import Flask, abort, render_template, redirect, request

from tutor_site import config as cfg


class TutorSiteApp:
    def __init__(self):
        self._app = Flask(__name__, template_folder='templates')
        self._app.url_map.strict_slashes = False
        self._app.jinja_env.filters['any'] = any

        self.set_pages()

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
    def server(self) -> Flask:
        return self._app

    @property
    def data(self) -> Dict[str, Dict[str, Union[int, str]]]:
        if self._data is None:
            if not cfg.DB_PATH.exists():
                raise ValueError('Cannot initialize database.')

            with open(cfg.DB_PATH, 'r') as file:
                self._data = json.load(file)

        return self._data

    def set_pages(self) -> None:
        # index page
        self._app.add_url_rule('/', 'index', self._get_index)

        # goal page
        self._app.add_url_rule('/goals', 'goal',
                               self._get_goal, defaults={'goal': None})
        self._app.add_url_rule('/goals/<string:goal>', 'goal',
                               self._get_goal)

        # profile page
        self._app.add_url_rule('/profiles', 'profile', self._get_profile,
                               defaults={'profile': None})
        self._app.add_url_rule('/profiles/<int:profile_id>', 'profile',
                               self._get_profile)

        # request page
        self._app.add_url_rule('/request', 'request', self._get_request)

        # request done page
        self._app.add_url_rule('/request_done', 'request_done',
                               self._get_request_done, methods=['POST'])

        # booking page
        booking_url = '/booking/<int:profile_id>/<string:day>/<string:time>'
        self._app.add_url_rule(booking_url, 'booking', self._get_booking)

        # booking done page
        self._app.add_url_rule('/booking_done', 'booking_done',
                               self._get_booking_done, methods=['POST'])

    def _get_index(self) -> str:
        profile_ids = random.sample(list(self.data), 6)
        data = {profile_id: self.data[profile_id]
                for profile_id in profile_ids}

        return render_template('index.html', data=dict(data), goals=cfg.GOALS)

    def _get_goal(self, goal: str) -> str:
        if goal is None or goal not in cfg.GOALS:
            return redirect('/goals/travel', code=301)

        data = {id_: tutor
                for id_, tutor in self.data.items()
                if goal in tutor['goals']}
        data = sorted(data.items(),
                      key=lambda item: item[1]['rating'],
                      reverse=True)

        return render_template('goal.html', data=dict(data),
                               goal=cfg.GOALS[goal])

    def _get_profile(self, profile_id: str) -> str:
        profile_id = str(profile_id)

        if profile_id is None or profile_id not in self.data:
            return redirect('/profiles/1')

        return render_template('profile.html',
                               tutor=self.data[profile_id],
                               days=cfg.DAY_MAPPING)

    def _get_request(self) -> str:
        return render_template('request.html', goals=cfg.GOALS)

    def _get_request_done(self) -> str:
        goal = request.form.get('goal', '')
        time = request.form.get('time', '')
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')

        with open(self._request_file, 'r') as file:
            request_data = json.load(file)
            if request_data:
                request_id = max(map(int, request_data)) + 1
            else:
                request_id = 1

            request_data[request_id] = {
                'name':     name,
                'phone':    phone,
                'time':     time,
                'goal':     goal,
            }

        # TODO: do backup before writing

        with open(self._request_file, 'w') as file:
            json.dump(request_data, file, indent=4)

        goal = cfg.GOALS.get(goal, '')

        return render_template('request_done.html',
                               goal=goal,
                               time=time,
                               name=name,
                               phone=phone)

    def _get_booking(self, profile_id: int, day: str, time: str) -> str:
        tutor = self.data.get(str(profile_id), {})
        if not tutor:
            abort(404)

        return render_template('booking.html',
                               tutor=tutor,
                               day_ticker=day,
                               day=cfg.DAY_MAPPING[day],
                               time=time)

    def _get_booking_done(self) -> str:
        day_ticker = request.form.get('clientWeekday', '')
        time = request.form.get('clientTime', '')
        profile_id = request.form.get('clientTeacher', '')
        client_name = request.form.get('clientName', '')
        client_phone = request.form.get('clientPhone', '')

        with open(self._booking_file, 'r') as file:
            booking_data = json.load(file)

            if booking_data:
                booking_id = max(map(int, booking_data)) + 1
            else:
                booking_id = 1

            booking_data[booking_id] = {
                'profile_id':   profile_id,
                'time':         time,
                'day_ticker':   day_ticker,
                'client_name':  client_name,
                'client_phone': client_phone,
            }

        # TODO: do backup before writing

        with open(self._booking_file, 'w') as file:
            json.dump(booking_data, file, indent=4)

        return render_template('booking_done.html',
                               day=cfg.DAY_MAPPING[day_ticker],
                               time=time,
                               client_name=client_name,
                               client_phone=client_phone)

    def run(self,
            debug: Optional[bool] = False,
            host: Optional[str] = 'localhost',
            port: Optional[int] = 8080):
        self.set_pages()

        self._app.run(debug=debug, host=host, port=port)
