from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError, fields
from models import db, Exercise, Workout, WorkoutExercise

ma = Marshmallow()


class ExerciseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Exercise
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    category = ma.auto_field(required=True)
    equipment_needed = ma.auto_field(required=True)

    VALID_CATEGORIES = ["strength", "cardio", "flexibility", "balance"]

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError("Name cannot be empty.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if value not in self.VALID_CATEGORIES:
            raise ValidationError(f"Category must be one of: {self.VALID_CATEGORIES}")


class WorkoutExerciseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True

    id = ma.auto_field(dump_only=True)
    workout_id = ma.auto_field(dump_only=True)
    exercise_id = ma.auto_field(dump_only=True)
    reps = ma.auto_field()
    sets = ma.auto_field()
    duration_seconds = ma.auto_field()

    @validates("reps")
    def validate_reps(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be a positive integer.")

    @validates("sets")
    def validate_sets(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be a positive integer.")

    @validates("duration_seconds")
    def validate_duration_seconds(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("Duration in seconds cannot be negative.")


class WorkoutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Workout
        load_instance = True

    id = ma.auto_field(dump_only=True)
    date = ma.auto_field(required=True)
    duration_minutes = ma.auto_field(required=True)
    notes = ma.auto_field()

    exercises = ma.Nested(ExerciseSchema, many=True, dump_only=True)
    workout_exercises = ma.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):
        if value is None or value <= 0:
            raise ValidationError("Duration must be a positive integer.")


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)