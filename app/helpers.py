from datetime import datetime, date
from config import EXERCISE_TYPE_FIELDS,TRAINING_TYPE_FIELDS

def save_training_draft(session, training_type, form, fields_map):
    """
    Save temporary training info in session before adding exercises.
    """

    draft = session.get('training_draft', {})
    draft['training_type'] = training_type

    for field in ['date', 'difficulty', 'notes']:
        if field in form:
            draft[field] = form.get(field)

    for field in fields_map.get(training_type, []):
        if field in form:
            draft[field] = form.get(field)

    session['training_draft'] = draft
    session.modified = True


def save_exercise_draft(session, training_type, form, fields_map):
    """
    Save temporary exercise info in session before submitting training
    """
    exercises = session.get('exercise_draft', [])
    exercise = {
        'ex_name': form.get('ex_name')
    }

    for field in fields_map.get(training_type, []):
        value = form.get(field)
        if value not in (None, ''):
            exercise[field] = value

    exercises.append(exercise)
    session['exercise_draft'] = exercises
    session.modified = True



def parse_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def validate_training_date(date_str):
    """Make sure date is not in the future"""
    try:
        training_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if training_date > date.today():
            return False
        return True
    except ValueError:
        return False


def exercise_to_dict(exercise, training_type):
    """Convert Exercise to dict for UI"""
    data = {
        'id': exercise.id,
        'ex_name': exercise.ex_name,
        'notes': exercise.notes,
    }

    for field in EXERCISE_TYPE_FIELDS.get(training_type, []):
        value = getattr(exercise, field, None)
        if value is not None:
            data[field] = value

    return data


def training_to_dict(training):
    """Convert training to dict for UI"""
    data = {
        'id': training.id,
        'date': training.date,
        'difficulty': training.difficulty,
        'notes': training.notes,
        **{
            field: getattr(training, field)
            for field in TRAINING_TYPE_FIELDS.get(training.training_type, [])
        }
    }
    return data