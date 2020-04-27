from tutor_site.database.database import db


tutors_goals_association = db.Table('tutors_goals',
    db.Column('tutor_id', db.Integer, db.ForeignKey('tutors.id')),
    db.Column('goal_id', db.Integer, db.ForeignKey('goals.id'))
)


class Tutor(db.Model):
    __tablename__ = 'tutors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture_url = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    free = db.Column(db.JSON, nullable=False)

    goals = db.relationship('Goal', secondary=tutors_goals_association,
                            back_populates='tutors')
    booking = db.relationship('Booking', back_populates='tutor')


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.Text, nullable=False, unique=True)

    tutors = db.relationship('Tutor', secondary=tutors_goals_association,
                             back_populates='goals')


class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=False)
    day_ticker = db.Column(db.String(3), nullable=False)
    client_name = db.Column(db.Text, nullable=False)
    client_phone = db.Column(db.Text, nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    tutor = db.relationship('Tutor', back_populates='booking')


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)
    goal = db.Column(db.Text, nullable=False)
