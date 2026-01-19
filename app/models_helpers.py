from app import db
from app.models import Training, Exercise
from config import EXERCISE_TYPE_FIELDS, TRAINING_TYPE_FIELDS
from flask import session
from app.helpers import parse_date
from datetime import datetime


def filter_by_training_type(query, training_type):
    """Filters trainings by type"""

    if training_type:
        query = query.filter(Training.training_type == training_type)
    return query.distinct()

def filter_by_date(query, date_str):
    """Filters trainings by date"""

    if not date_str:
        return query

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        return query.filter(Training.date == date_obj)
    except ValueError:
        return query


def apply_filters(training_type='', date_str=None):
    query = Training.query
    query = filter_by_training_type(Training.query, training_type)
    query = filter_by_date(query, date_str)
    return query.distinct()



def build_training(training_type, training_draft):
    training = Training(
        training_type=training_type,
        date=parse_date(training_draft.get('date')),
        difficulty=training_draft.get('difficulty'),
        notes=training_draft.get('notes')
    )

    for field in TRAINING_TYPE_FIELDS.get(training_type, []):
        if field in training_draft:
            setattr(training, field, training_draft[field])

    db.session.add(training)
    db.session.flush()

    return training

def build_exercise(training_id, training_type, exercise_draft):
    exercise = Exercise(
        training_id=training_id,
        ex_name=exercise_draft.get('ex_name')
    )

    for field in EXERCISE_TYPE_FIELDS.get(training_type, []):
        if field in exercise_draft:
            setattr(exercise, field, exercise_draft[field])

    db.session.add(exercise)

def create_training_from_draft(training_type):
    training_draft = session.get('training_draft')
    exercise_draft = session.get('exercise_draft', [])

    training = build_training(training_type, training_draft)

    for ex in exercise_draft:
        build_exercise(training.id, training_type, ex)

    db.session.commit()

    session.pop('training_draft', None)
    session.pop('exercise_draft', None)

    return training