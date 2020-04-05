import random

from flask import abort, redirect, render_template, request, url_for
from flask.views import View

from tutor_site import config as cfg
from tutor_site.data import data_storage


class BasePage(View):
    def __init__(self, template_name: str):
        self._template_name = template_name


class Index(BasePage):
    def dispatch_request(self) -> str:
        profile_ids = random.sample(list(data_storage.data), 6)
        data = {profile_id: data_storage.data[profile_id]
                for profile_id in profile_ids}

        return render_template(self._template_name, data=dict(data),
                               goals=cfg.GOALS)


class Goal(BasePage):
    def dispatch_request(self, goal: str) -> str:
        if goal is None or goal not in cfg.GOALS:
            return redirect(url_for('goal', goal='travel'), code=301)

        data = {id_: tutor
                for id_, tutor in data_storage.data.items()
                if goal in tutor['goals']}
        data = sorted(data.items(),
                      key=lambda item: item[1]['rating'],
                      reverse=True)

        return render_template(self._template_name, data=dict(data),
                               goal=cfg.GOALS[goal])


class Profile(BasePage):
    def dispatch_request(self, profile_id: str) -> str:
        profile_id = str(profile_id)

        if profile_id is None or profile_id not in data_storage.data:
            return redirect(url_for('profile', profile_id='1'))

        return render_template(self._template_name,
                               tutor=data_storage.data[profile_id],
                               days=cfg.DAY_MAPPING)


class Request(BasePage):
    def dispatch_request(self) -> str:
        return render_template(self._template_name, goals=cfg.GOALS)


class RequestDone(BasePage):
    methods = ['POST']

    def dispatch_request(self) -> str:
        goal = request.form.get('goal', '')
        time = request.form.get('time', '')
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')

        data = {
            'name':     name,
            'phone':    phone,
            'time':     time,
            'goal':     goal,
        }

        data_storage.put_request_data(data)

        goal = cfg.GOALS.get(goal, '')

        return render_template('request_done.html',
                               goal=goal,
                               time=time,
                               name=name,
                               phone=phone)


class Booking(BasePage):
    def dispatch_request(self, profile_id: int, day: str, time: str) -> str:
        tutor = data_storage.data.get(str(profile_id), {})
        if not tutor:
            abort(404)

        return render_template(self._template_name,
                               tutor=tutor,
                               day_ticker=day,
                               day=cfg.DAY_MAPPING[day],
                               time=time)


class BookingDone(BasePage):
    methods = ['POST']

    def dispatch_request(self) -> str:
        day_ticker = request.form.get('clientWeekday', '')
        time = request.form.get('clientTime', '')
        profile_id = request.form.get('clientTeacher', '')
        client_name = request.form.get('clientName', '')
        client_phone = request.form.get('clientPhone', '')

        data = {
            'profile_id':   profile_id,
            'time':         time,
            'day_ticker':   day_ticker,
            'client_name':  client_name,
            'client_phone': client_phone,
        }

        data_storage.put_booking_data(data)

        return render_template(self._template_name,
                               day=cfg.DAY_MAPPING[day_ticker],
                               time=time,
                               client_name=client_name,
                               client_phone=client_phone)
