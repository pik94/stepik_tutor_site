from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, StringField, SubmitField
from wtforms.validators import InputRequired

from tutor_site import config as cfg


class RequestForm(FlaskForm):
    goal = RadioField('goal',
                      choices=[(goal_key, goal)
                               for goal_key, goal in cfg.GOALS.items()],
                      default='travel')
    time = RadioField('time', choices=[(time, time) for time in cfg.TIMES],
                      default='3-5')
    name = StringField('Вас зовут',
                       [InputRequired(message='Введите Ваше имя')])
    phone = StringField('Ваш телефон',
                        [InputRequired(message='Введите Ваш номер')])
    submit = SubmitField('Найдите мне преподавателя')


class BookingForm(FlaskForm):
    day_ticker = HiddenField('client_weekday')
    time = HiddenField('client_time')
    tutor_id = HiddenField('client_teacher')
    name = StringField('name', [InputRequired()])
    phone = StringField('phone', [InputRequired()])
    submit = SubmitField('Записаться на пробный урок')
