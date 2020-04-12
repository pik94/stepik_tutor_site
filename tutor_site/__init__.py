from flask import Flask
from flask_migrate import Migrate

from tutor_site.views import (
    BookingPage, BookingDonePage, GoalPage, IndexPage, ProfilePage,
    RequestPage, RequestDonePage
    )
from tutor_site.database import db_model

app = Flask(__name__, template_folder='templates')
app.url_map.strict_slashes = False
app.jinja_env.filters['any'] = any
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://pik:123@localhost:5432/tutordb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tutordb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db_model.init_app(app)

migrate = Migrate(app, db_model)


# index page
app.add_url_rule('/', view_func=IndexPage.as_view(
    'index', template_name='index.html'))

# goal page
_goal_view = GoalPage.as_view('goal', template_name='goal.html')
app.add_url_rule('/goals', view_func=_goal_view, defaults={'goal': None})
app.add_url_rule('/goals/<string:goal>', view_func=_goal_view)

# profile page
_profile_view = ProfilePage.as_view('profile', template_name='profile.html')
app.add_url_rule('/profiles', view_func=_profile_view,
                 defaults={'profile_id': None})
app.add_url_rule('/profiles/<int:profile_id>', view_func=_profile_view)

# request page
_request_view = RequestPage.as_view('request', template_name='request.html')
app.add_url_rule('/request', view_func=_request_view)

# request done page
_request_done_view = RequestDonePage.as_view('request_done',
                                             template_name='request_done.html')
app.add_url_rule('/request_done', view_func=_request_done_view)

# booking page
_booking_view = BookingPage.as_view('booking', template_name='booking.html')
app.add_url_rule('/booking/<int:profile_id>/<string:day>/<string:time>',
                 view_func=_booking_view)

# booking done page
_booking_done_view = BookingDonePage.as_view('booking_done',
                                             template_name='booking_done.html')
app.add_url_rule('/booking_done', view_func=_booking_done_view)
