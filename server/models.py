from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        CheckConstraint("name != ''", name="exercise_name_not_empty"),
        CheckConstraint(
            "category IN ('strength', 'cardio', 'flexibility', 'balance')",
            name="valid_category",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )
    # Has many Workouts through WorkoutExercises
    workouts = db.relationship("Workout", secondary="workout_exercises", viewonly=True)

    VALID_CATEGORIES = ["strength", "cardio", "flexibility", "balance"]

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if value not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {self.VALID_CATEGORIES}")
        return value

    def __repr__(self):
        return f"<Exercise id={self.id} name={self.name} category={self.category}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="positive_duration"),
        CheckConstraint("date IS NOT NULL", name="date_required"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )
    # Has many Exercises through WorkoutExercises
    exercises = db.relationship("Exercise", secondary="workout_exercises", viewonly=True)

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Duration must be a positive integer.")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("Date is required.")
        return value

    def __repr__(self):
        return f"<Workout id={self.id} date={self.date} duration={self.duration_minutes}min>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (
        CheckConstraint("reps > 0", name="positive_reps"),
        CheckConstraint("sets > 0", name="positive_sets"),
        CheckConstraint("duration_seconds >= 0", name="non_negative_duration_seconds"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Belongs to Workout and Exercise
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be a positive integer.")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be a positive integer.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and value < 0:
            raise ValueError("Duration in seconds cannot be negative.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise workout_id={self.workout_id} exercise_id={self.exercise_id}>"