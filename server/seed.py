from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():

    print("Clearing tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    bench_press = Exercise(name="Bench Press", category="strength", equipment_needed=True)
    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    yoga_stretch = Exercise(name="Yoga Stretch", category="flexibility", equipment_needed=False)
    plank = Exercise(name="Plank", category="strength", equipment_needed=False)

    db.session.add_all([bench_press, squat, running, yoga_stretch, plank])
    db.session.commit()

    print("Seeding workouts...")
    workout1 = Workout(date=date(2024, 1, 15), duration_minutes=60, notes="Morning strength session")
    workout2 = Workout(date=date(2024, 1, 17), duration_minutes=45, notes="Cardio and flexibility day")
    workout3 = Workout(date=date(2024, 1, 19), duration_minutes=30, notes="Quick lunch workout")

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()

    print("Seeding workout exercises...")
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=bench_press.id, sets=4, reps=10)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=squat.id, sets=3, reps=12)
    we3 = WorkoutExercise(workout_id=workout1.id, exercise_id=plank.id, sets=3, duration_seconds=60)
    we4 = WorkoutExercise(workout_id=workout2.id, exercise_id=running.id, duration_seconds=1800)
    we5 = WorkoutExercise(workout_id=workout2.id, exercise_id=yoga_stretch.id, sets=2, duration_seconds=120)
    we6 = WorkoutExercise(workout_id=workout3.id, exercise_id=squat.id, sets=3, reps=15)

    db.session.add_all([we1, we2, we3, we4, we5, we6])
    db.session.commit()

    print("Done seeding!")