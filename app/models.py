from app import db
from datetime import date

class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False, default=date.today)
    training_type = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20))
    notes = db.Column(db.Text)

    # ---- Pool only ----
    pool_size = db.Column(db.Integer)

    # ---- Depth only ----
    location = db.Column(db.String(100))
    temperature = db.Column(db.Integer)
    wetsuit = db.Column(db.String(50))
    weights_free = db.Column(db.Integer)

    # ---- Gym only ----
    duration = db.Column(db.String(50))
    kcal = db.Column(db.String(50))
    avg_heartrate = db.Column(db.Integer)
    max_heartrate = db.Column(db.Integer)

    exercises = db.relationship(
        'Exercise',
        backref='training',
        lazy='select',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Training {self.id} {self.training_type}>'


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    training_id = db.Column(
        db.Integer,
        db.ForeignKey('training.id'),
        nullable=False
    )

    ex_name = db.Column(db.String(100))
    reps = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # ---- Pool
    distance = db.Column(db.Integer)
    interval = db.Column(db.String(20))

    # ---- Depth ----
    depth = db.Column(db.Integer)
    dive_time = db.Column(db.String(50))
    rest_time = db.Column(db.String(50))

    # ---- Gym ----
    weight = db.Column(db.String(50))
    sets = db.Column(db.Integer)

    def __repr__(self):
        return f'<Exercise {self.ex_name}>'




