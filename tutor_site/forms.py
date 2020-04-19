from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from tutor_site import config as cfg


class RequestForm(FlaskForm):
    goal = RadioField('goal',
                      choices=[(goal_key, goal)
                               for goal_key, goal in cfg.GOALS.items()],
                      default='travel')
    time = RadioField('time', choices=[(time, time) for time in cfg.TIMES],
                      default='3-5')
    name = StringField('Вас зовут',
                       [InputRequired(message='Вы не ввели свое имя'),
                        Length(message='В имени должно быть минимум 3 символа',
                               min=3)])
    phone = StringField('Ваш телефон',
                        [InputRequired('Вы не ввели свой номер.')])
    submit = SubmitField('Найдите мне преподавателя')


class BookingForm(FlaskForm):
    day_ticker = HiddenField('client_weekday')
    time = HiddenField('client_time')
    tutor_id = HiddenField('client_teacher')
    name = StringField('name',
                       [InputRequired(message='Вы не ввели свое имя.'),
                        Length(message='В имени должно быть минимум 3 символа',
                               min=3)])
    phone = StringField('phone',
                        [InputRequired(message='Вы не ввели свой номер')])
    submit = SubmitField('Записаться на пробный урок')
