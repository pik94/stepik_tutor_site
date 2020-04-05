from flask import Flask

from tutor_site.views import (
    Booking, BookingDone, Goal, Index, Profile, Request, RequestDone
    )

app = Flask(__name__, template_folder='templates')
app.url_map.strict_slashes = False
app.jinja_env.filters['any'] = any

# index page
app.add_url_rule('/', view_func=Index.as_view(
    'index', template_name='index.html'))

# goal page
_goal_view = Goal.as_view('goal', template_name='goal.html')
app.add_url_rule('/goals', view_func=_goal_view, defaults={'goal': None})
app.add_url_rule('/goals/<string:goal>', view_func=_goal_view)

# profile page
_profile_view = Profile.as_view('profile', template_name='profile.html')
app.add_url_rule('/profiles', view_func=_profile_view,
                 defaults={'profile_id': None})
app.add_url_rule('/profiles/<int:profile_id>', view_func=_profile_view)

# request page
_request_view = Request.as_view('request', template_name='request.html')
app.add_url_rule('/request', view_func=_request_view)

# request done page
_request_done_view = RequestDone.as_view('request_done',
                                         template_name='request_done.html')
app.add_url_rule('/request_done', view_func=_request_done_view)

# booking page
_booking_view = Booking.as_view('booking', template_name='booking.html')
app.add_url_rule('/booking/<int:profile_id>/<string:day>/<string:time>',
                 view_func=_booking_view)

# booking done page
_booking_done_view = BookingDone.as_view('booking_done',
                                         template_name='booking_done.html')
app.add_url_rule('/booking_done', view_func=_booking_done_view)
