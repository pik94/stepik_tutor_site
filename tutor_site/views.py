import datetime as dt

from flask import abort, redirect, render_template, request, url_for
from flask.views import View

from tutor_site import config as cfg
from tutor_site.database import db_model
from tutor_site.database import Booking, Goal, Request, Tutor
from tutor_site.forms import BookingForm, RequestForm


class IndexPage(View):
    def dispatch_request(self) -> str:
        # TODO: handle exceptions
        rows = db_model.session.query(Tutor).order_by(
            Tutor.rating.desc()).limit(6).all()

        # profile_ids = random.sample(list(data_storage.data), 6)
        data = {row.id: row for row in rows}

        return render_template(cfg.TEMPLATES_NAME_MAPPING['index'],
                               data=dict(data),
                               goals=cfg.GOALS)


class GoalPage(View):
    def dispatch_request(self, goal: str) -> str:
        if goal is None or goal not in cfg.GOALS:
            return redirect(url_for('goal', goal='travel'), code=301)

        # TODO: handle exception
        goal_obj = db_model.session.query(Goal).filter(
            Goal.goal == goal).scalar()

        tutors = sorted(goal_obj.tutors, key=lambda tutor: tutor.rating,
                        reverse=True)
        data = {tutor.id: tutor for tutor in tutors}
        return render_template(cfg.TEMPLATES_NAME_MAPPING['goals'],
                               data=dict(data),
                               goal=cfg.GOALS[goal])


class ProfilePage(View):
    def dispatch_request(self, profile_id: int) -> str:
        # TODO: handle exception
        tutor = db_model.session.query(Tutor).filter(
            Tutor.id == profile_id).scalar()
        if not tutor:
            abort(404)

        return render_template(cfg.TEMPLATES_NAME_MAPPING['profile'],
                               tutor=tutor,
                               days=cfg.DAY_MAPPING)


class RequestPage(View):
    methods = ['GET', 'POST']

    def dispatch_request(self) -> str:
        form = RequestForm()
        if request.method == 'GET' or not form.validate_on_submit():
            return render_template(cfg.TEMPLATES_NAME_MAPPING['request'],
                                   form=form)

        elif request.method == 'POST':
            goal = form.goal.data
            time = form.time.data
            name = form.name.data
            phone = form.phone.data

            req = Request(name=name, phone=phone, time=time, goal=goal)
            db_model.session.add(req)
            # TODO: handle exception
            db_model.session.commit()

            goal = cfg.GOALS.get(goal, '')

            return render_template(cfg.TEMPLATES_NAME_MAPPING[
                                       'request_success'],
                                   goal=goal,
                                   time=time,
                                   name=name,
                                   phone=phone)

        else:
            abort(404)


class BookingPage(View):
    methods = ['GET', 'POST']

    def dispatch_request(self, profile_id: int, day: str, time: str) -> str:
        form = BookingForm()
        if request.method == 'GET' or not form.validate_on_submit():
            tutor = db_model.session.query(Tutor).filter(
                Tutor.id == profile_id).scalar()
            if not tutor:
                abort(404)

            return render_template(cfg.TEMPLATES_NAME_MAPPING['booking'],
                                   tutor=tutor,
                                   day_ticker=day,
                                   day=cfg.DAY_MAPPING[day],
                                   time=time,
                                   form=form)

        elif request.method == 'POST':
            day = form.day_ticker.data
            time = form.time.data
            tutor_id = form.tutor_id.data
            client_name = form.name.data
            client_phone = form.phone.data

            booking_info = Booking(
                time=dt.datetime.strptime(time, '%H:%M').time(),
                day_ticker=day,
                client_name=client_name,
                client_phone=client_phone,
                tutor_id=int(tutor_id))

            # TODO: handle exception
            db_model.session.add(booking_info)
            db_model.session.commit()

            return render_template(cfg.TEMPLATES_NAME_MAPPING[
                                       'booking_success'],
                                   day=cfg.DAY_MAPPING[day],
                                   time=time,
                                   client_name=client_name,
                                   client_phone=client_phone)

        else:
            abort(404)
