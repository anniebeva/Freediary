from app import app, db
from datetime import datetime
from app.models import Training, Exercise
from flask import render_template, request, redirect, url_for, session, abort, flash

from app.helpers import save_training_draft, \
    exercise_to_dict, training_to_dict, validate_training_date
from app.models_helpers import create_training_from_draft, apply_filters,build_exercise
from config import TRAINING_TYPE_FIELDS, EXERCISE_TYPE_FIELDS

@app.route('/')
@app.route('/trainings', methods=['GET', 'POST'])
def show_all_trainings():
    """Main page: all trainings/filtered trainings"""

    selected_type = request.args.get('training_type', '')
    date_str = request.args.get('date')

    query = apply_filters(
        training_type=selected_type,
        date_str=date_str
    )

    trainings = query.order_by(Training.date.desc()).all()

    return render_template(
        'all_trainings.html',
        trainings=trainings,
        selected_type=selected_type,
        searched_date=date_str,
        not_found=(date_str is not None and not trainings)
    )


@app.route('/add_training', methods=['GET', 'POST'])
def choose_training_type():
    """
    First step to add new training
    Select training type
    """
    if request.method == 'POST':
        training_type = request.form.get('type')

        # Create/clean drafts for new training
        session['training_draft'] = {'training_type': training_type}
        session['exercise_draft'] = []

        return redirect(url_for('add_training', training_type=training_type))

    return render_template('training_form/choose_training_type.html')


@app.route('/add_training/<training_type>', methods=['GET', 'POST'])
def add_training(training_type):
    """
    Add training based on training type
    """
    # Take draft from session - empty
    training_draft = session.get('training_draft', {})
    exercise_draft = session.get('exercise_draft', [])

    if request.method == 'POST':
        date_str = request.form.get('date')
        if not validate_training_date(date_str):
            flash('Date cannot be in the future', 'danger')
            return redirect(request.url)

        #Save to draft
        save_training_draft(
            session=session,
            training_type=training_type,
            form=request.form,
            fields_map=TRAINING_TYPE_FIELDS
        )

        if 'add_exercise' in request.form:
            return redirect(url_for('add_exercise'))

        if 'submit_training' in request.form:
            training = create_training_from_draft(training_type)
            return redirect(url_for('show_all_trainings'))

    return render_template(
        'training_form/add_training.html',
        training_type=training_type,
        training_draft=training_draft,
        exercise_draft=exercise_draft
    )

@app.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    """
    Add exercise page
    Saves exercise to training DB if training exists
    Else saves exercise as a draft to session
    """
    training_id = request.args.get('training_id', type=int)
    next_url = request.args.get('next')

    if training_id:
        training = Training.query.get_or_404(training_id)
        training_type = training.training_type
    else:
        training = None
        training_type = session.get('training_draft', {}).get('training_type')

    if request.method == 'POST':
        exercise_data = {
            'ex_name': request.form.get('ex_name'),
            'notes': request.form.get('notes')
        }

        for field in EXERCISE_TYPE_FIELDS.get(training_type, []):
            value = request.form.get(field)
            if value not in (None, ''):
                exercise_data[field] = value

        # for DB
        if training:
            build_exercise(
                training_id=training.id,
                training_type=training_type,
                exercise_draft=exercise_data
            )
            db.session.commit()

            return redirect(
                next_url or url_for('show_training', id=training.id)
            )

        # for draft
        exercises = session.get('exercise_draft', [])
        exercises.append(exercise_data)
        session['exercise_draft'] = exercises
        session.modified = True

        return redirect(
            next_url or url_for('add_training', training_type=training_type)
        )

    return render_template(
        'exercise_form/add_exercise.html',
        training_type=training_type,
        training=training
    )

@app.route('/training/<id>')
def show_training(id):
    """Training page"""

    training = Training.query.get_or_404(id)
    return render_template('training_info_templates/training_info.html',
                           training=training,
                           exercises=training.exercises,
                           training_type=training.training_type)


@app.route('/edit_training/<id>', methods=['GET', 'POST'])
def edit_training(id):
    """Edit training page"""

    training = Training.query.get_or_404(id)
    training_dict = training_to_dict(training)
    training_type = training.training_type

    exercises = [
        exercise_to_dict(ex, training.training_type)
        for ex in training.exercises
    ]

    if request.method == 'POST':
        date_str = request.form.get('date')
        training.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        training.difficulty = request.form.get('difficulty')
        training.notes = request.form.get('notes')

        for field in TRAINING_TYPE_FIELDS.get(training_type, []):
            setattr(training, field, request.form.get(field))

        db.session.commit()
        return redirect(url_for('show_training', id=id))

    return render_template('training_form/edit_training.html',
                           training=training_dict,
                           exercises=exercises,
                           training_type=training.training_type,
                           is_edit=True)


@app.route('/edit_draft_exercise/<int:index>/<training_type>', methods=['GET', 'POST'])
def edit_draft_exercise(index, training_type):
    draft_exercises = session.get('exercise_draft', [])
    if index >= len(draft_exercises):
        abort(404)
    ex = draft_exercises[index]

    if request.method == 'POST':
        ex['ex_name'] = request.form.get('ex_name')
        ex['notes'] = request.form.get('notes')

        for field in EXERCISE_TYPE_FIELDS.get(training_type, []):
            ex[field] = request.form.get(field)

        session['exercise_draft'] = draft_exercises
        next_url = request.form.get('next') or url_for('add_training', training_type=training_type)
        return redirect(next_url)

    return render_template(
        'exercise_form/edit_exercise.html',
        exercise=ex,
        draft=ex,
        training_type=training_type,
        next=request.args.get('next')
    )


@app.route('/edit_exercise/<int:exercise_id>', methods=['GET', 'POST'])
def edit_exercise(exercise_id):
    """Edit existing exercise in DB"""
    exercise = Exercise.query.get_or_404(exercise_id)
    training_type = exercise.training.training_type

    if request.method == 'POST':
        exercise.ex_name = request.form.get('ex_name')
        exercise.notes = request.form.get('notes')

        for field in EXERCISE_TYPE_FIELDS.get(training_type, []):
            setattr(exercise, field, request.form.get(field))

        db.session.commit()
        next_url = request.form.get('next') or url_for('show_training', id=exercise.training_id)
        return redirect(next_url)

    return render_template(
        'exercise_form/edit_exercise.html',
        exercise=exercise,
        draft=None,
        training_type=training_type,
        next=request.args.get('next')
    )

@app.route('/delete_draft_exercise/<int:index>')
def delete_draft_exercise(index):
    exercise_draft = session.get('exercise_draft', [])
    training_draft = session.get('training_draft', {})

    if index < 0 or index >= len(exercise_draft):
        abort(404)

    exercise_draft.pop(index)
    session['exercise_draft'] = exercise_draft
    session.modified = True

    training_type = training_draft.get('training_type')
    next_url = request.args.get('next') or url_for('add_training', training_type=training_type)
    return redirect(next_url)

@app.route('/delete_training/<id>')
def delete_training(id):
    """Delete training from db"""

    training = Training.query.get_or_404(id)

    db.session.delete(training)
    db.session.commit()

    return redirect(url_for('show_all_trainings'))


@app.route('/delete_exercise/<int:exercise_id>')
def delete_exercise(exercise_id):
    """delete exercise from db"""
    exercise = Exercise.query.get_or_404(exercise_id)

    db.session.delete(exercise)
    db.session.commit()

    next_url = request.args.get('next')
    if next_url:
        return redirect(next_url)

    return redirect(url_for('show_training', id=exercise.training_id))