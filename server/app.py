from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ma,
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        db.session.rollback()
    db.session.remove()


# ---- Workout Endpoints ----

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.jsonify(workouts), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return workout_schema.jsonify(workout), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    errors = workout_schema.validate(data)
    if errors:
        return jsonify(errors), 422
    workout = workout_schema.load(data)
    db.session.add(workout)
    db.session.commit()
    return workout_schema.jsonify(workout), 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {id} deleted successfully"}), 200


# ---- Exercise Endpoints ----

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.jsonify(exercises), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return exercise_schema.jsonify(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    errors = exercise_schema.validate(data)
    if errors:
        return jsonify(errors), 422
    exercise = exercise_schema.load(data)
    db.session.add(exercise)
    db.session.commit()
    return exercise_schema.jsonify(exercise), 201


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {id} deleted successfully"}), 200


# ---- WorkoutExercise Endpoints ----

@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    data = request.get_json()
    errors = workout_exercise_schema.validate(data)
    if errors:
        return jsonify(errors), 422

    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds")
    )
    db.session.add(workout_exercise)
    db.session.commit()
    return workout_exercise_schema.jsonify(workout_exercise), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)