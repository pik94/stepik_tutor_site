import datetime as dt

from flask import abort, redirect, render_template, request, url_for
from flask.views import View

from tutor_site import config as cfg
from tutor_site.database import db_model
from tutor_site.database import Booking, Goal, Request, Tutor


class BasePage(View):
    def __init__(self, template_name: str):
        self._template_name = template_name


class IndexPage(BasePage):
    def dispatch_request(self) -> str:
        # TODO: handle exceptions
        rows = db_model.session.query(Tutor).order_by(
            Tutor.rating.desc()).limit(6).all()

        # profile_ids = random.sample(list(data_storage.data), 6)
        data = {row.id: row for row in rows}

        return render_template(self._template_name, data=dict(data),
                               goals=cfg.GOALS)


class GoalPage(BasePage):
    def dispatch_request(self, goal: str) -> str:
        if goal is None or goal not in cfg.GOALS:
            return redirect(url_for('goal', goal='travel'), code=301)

        # TODO: handle exception
        goal_obj = db_model.session.query(Goal).filter(
            Goal.goal == goal).scalar()

        tutors = sorted(goal_obj.tutors, key=lambda tutor: tutor.rating,
                        reverse=True)
        data = {id_: tutor for id_, tutor in tutors}
        return render_template(self._template_name, data=dict(data),
                               goal=cfg.GOALS[goal])


class ProfilePage(BasePage):
    def dispatch_request(self, profile_id: int) -> str:
        # TODO: handle exception
        tutor = db_model.session.query(Tutor).filter(
            Tutor.id == profile_id).scalar()
        if not tutor:
            abort(404)

        return render_template(self._template_name,
                               tutor=tutor,
                               days=cfg.DAY_MAPPING)


class RequestPage(BasePage):
    def dispatch_request(self) -> str:
        return render_template(self._template_name, goals=cfg.GOALS)


class RequestDonePage(BasePage):
    methods = ['POST']

    def dispatch_request(self) -> str:
        goal = request.form.get('goal', '')
        time = request.form.get('time', '')
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')

        req = Request(name=name, phone=phone, time=time, goal=goal)
        db_model.session.add(req)
        # TODO: handle exception
        db_model.session.commit()

        goal = cfg.GOALS.get(goal, '')

        return render_template('request_done.html',
                               goal=goal,
                               time=time,
                               name=name,
                               phone=phone)


class BookingPage(BasePage):
    def dispatch_request(self, profile_id: int, day: str, time: str) -> str:
        tutor = db_model.session.query(Tutor).filter(
            Tutor.id == profile_id).scalar()
        if not tutor:
            abort(404)

        return render_template(self._template_name,
                               tutor=tutor,
                               day_ticker=day,
                               day=cfg.DAY_MAPPING[day],
                               time=time)


class BookingDonePage(BasePage):
    methods = ['POST']

    def dispatch_request(self) -> str:
        day_ticker = request.form.get('clientWeekday', '')
        time = request.form.get('clientTime', '')
        profile_id = request.form.get('clientTeacher', 0)
        client_name = request.form.get('clientName', '')
        client_phone = request.form.get('clientPhone', '')

        booking_info = Booking(time=dt.datetime.strptime(time, '%H:%M').time(),
                               day_ticker=day_ticker,
                               client_name=client_name,
                               client_phone=client_phone,
                               tutor_id=int(profile_id))

        # TODO: handle exception
        db_model.session.add(booking_info)
        db_model.session.commit()

        return render_template(self._template_name,
                               day=cfg.DAY_MAPPING[day_ticker],
                               time=time,
                               client_name=client_name,
                               client_phone=client_phone)
