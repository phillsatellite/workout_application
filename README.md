# Workout Application API

A RESTful API backend for managing workouts and exercises, built with Flask, SQLAlchemy, and Marshmallow. The API allows users to create and manage workouts, create and manage exercises, and add exercises to workouts with tracking data like reps, sets, and duration.

---

## Installation

### Prerequisites
- Python 3.11+
- Pipenv

### Steps

**1. Clone the repository and navigate into the project:**
```bash
git clone https://github.com/phillsatellite/workout_application.git
cd workout_application
```

**2. Install dependencies:**
```bash
pipenv install
pipenv shell
```

**3. Navigate to the server directory:**
```bash
cd server
```

**4. Set the Flask app environment variable:**
```bash
export FLASK_APP=app.py
```

**5. Initialize and run database migrations:**
```bash
flask db init
flask db migrate -m "create exercises, workouts, and workout_exercises tables"
flask db upgrade
```

**6. Seed the database:**
```bash
python seed.py
```

---

## Running the Application

```bash
python app.py
```

The server will start at `http://127.0.0.1:5555`.

---

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | Returns a list of all workouts, each including their associated exercises and workout exercise details (reps, sets, duration) |
| GET | `/workouts/<id>` | Returns a single workout by ID, including its associated exercises and workout exercise details |
| POST | `/workouts` | Creates a new workout. Requires `date` and `duration_minutes`. Optionally accepts `notes` |
| DELETE | `/workouts/<id>` | Deletes a workout by ID. Also deletes all associated workout exercises |

**POST `/workouts` request body:**
```json
{
  "date": "2024-03-01",
  "duration_minutes": 45,
  "notes": "Optional notes here"
}
```

---

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | Returns a list of all exercises |
| GET | `/exercises/<id>` | Returns a single exercise by ID |
| POST | `/exercises` | Creates a new exercise. Requires `name`, `category`, and `equipment_needed` |
| DELETE | `/exercises/<id>` | Deletes an exercise by ID. Also deletes all associated workout exercises |

**POST `/exercises` request body:**
```json
{
  "name": "Pull Up",
  "category": "strength",
  "equipment_needed": false
}
```

Valid categories: `strength`, `cardio`, `flexibility`, `balance`

---

### Workout Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Adds an exercise to a workout. Optionally accepts `reps`, `sets`, and `duration_seconds` |

**POST request body:**
```json
{
  "sets": 3,
  "reps": 10,
  "duration_seconds": null
}
```

---

## Validations

### Table Constraints
- Exercise `name` must be unique and non-null
- Exercise `category` must be one of the four valid values
- Workout `duration_minutes` must be greater than 0
- Workout `date` cannot be null
- WorkoutExercise `reps` and `sets` must be positive if provided
- WorkoutExercise `duration_seconds` must be non-negative if provided

### Model Validations
- Exercise name cannot be blank or whitespace
- Exercise category must be `strength`, `cardio`, `flexibility`, or `balance`
- Workout duration must be a positive integer
- Workout date cannot be None

### Schema Validations
- All required fields are validated on incoming requests before hitting the database
- Invalid data returns a `422 Unprocessable Entity` response with error details

---

## Pipfile Dependencies

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
flask-sqlalchemy = "*"
flask-migrate = "*"
flask-marshmallow = "*"
marshmallow-sqlalchemy = "*"
python-dotenv = "*"

[dev-packages]

[requires]
python_version = "3.11"
```

---

## Project Structure

```
workout_application/
└── server/
    ├── app.py          
    ├── models.py       
    ├── schemas.py      
    ├── seed.py         
    ├── migrations/     
    └── instance/
        └── workout.db  
```
