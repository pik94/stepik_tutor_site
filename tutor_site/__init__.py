from flask import Flask
from flask_migrate import Migrate

from tutor_site import config as cfg
from tutor_site.views import (
    BookingPage, GoalPage, IndexPage, ProfilePage, RequestPage
    )
from tutor_site.database import db_model
from tutor_site.database.database import get_connection_string

app = Flask(__name__, template_folder='templates')
app.url_map.strict_slashes = False
app.jinja_env.filters['any'] = any
app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = cfg.CSRF_TOKEN

db_model.init_app(app)
app.app_context().push()

migrate = Migrate(app, db_model)


# index page
app.add_url_rule('/', view_func=IndexPage.as_view('index'))

# goal page
_goal_view = GoalPage.as_view('goal')
app.add_url_rule('/goals', view_func=_goal_view, defaults={'goal': None})
app.add_url_rule('/goals/<string:goal>', view_func=_goal_view)

# profile page
_profile_view = ProfilePage.as_view('profile')
app.add_url_rule('/profiles', view_func=_profile_view,
                 defaults={'profile_id': None})
app.add_url_rule('/profiles/<int:profile_id>', view_func=_profile_view)

# request page
_request_view = RequestPage.as_view('request')
app.add_url_rule('/request', view_func=_request_view)

# booking page
_booking_view = BookingPage.as_view('booking')
app.add_url_rule('/booking/<int:profile_id>/<string:day>/<string:time>',
                 view_func=_booking_view)
