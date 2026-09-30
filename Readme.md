# Student Course Enrollment API

## Problem Statement

Build a FastAPI application where students can enroll in courses.

## Technologies

- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL (Neon)
- Pydantic v2
- Uvicorn

SQLite is also supported - set `DATABASE_URL=sqlite:///enrollment.db` in `.env`
and the app will create the file and its tables automatically.

## Features

- Create courses
- List courses
- Fetch a single course
- List students
- Enroll students
- Prevent duplicate enrollment (checked in the app *and* enforced by a
  unique database constraint)
- View a student's courses
- Delete an enrollment
- Meaningful 400 / 404 / 422 errors
- Tables are created and sample students are seeded once, on startup

## Project structure

```
apidemo/
├── main.py          # FastAPI app, routes, startup/shutdown
├── database.py      # Engine, session factory, Base, connection check
├── models.py        # SQLAlchemy models: Student, Course, Enrollment
├── schemas.py       # Pydantic request/response models
├── .env.example     # Template for your own credentials
└── requirement.txt  # Dependencies
```

## API Endpoints

| Method | Path                          | Success | Notes                          |
| ------ | ----------------------------- | ------- | ------------------------------ |
| GET    | `/`                           | 200     | Service message                |
| GET    | `/students`                   | 200     | List students                  |
| POST   | `/courses`                    | 201     | Create a course                |
| GET    | `/courses`                    | 200     | List courses                   |
| GET    | `/courses/{course_id}`        | 200     | Fetch one course               |
| POST   | `/enroll`                     | 201     | Enroll a student               |
| GET    | `/students/{student_id}/courses` | 200  | A student's courses            |
| DELETE | `/enroll/{enrollment_id}`     | 200     | Delete an enrollment           |

### Errors

| Status | When                                                   |
| ------ | ------------------------------------------------------ |
| 400    | Student is already enrolled in that course             |
| 404    | Student / course / enrollment not found                |
| 422    | Request body fails validation                          |

## Installation

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirement.txt
```

## Configuration

Copy the template and put your own credentials in `.env` (this file is
git-ignored):

```
copy .env.example .env
```

`.env` must contain:

```
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require
```

The app exits at startup with a clear error if the database is unreachable.

## Run

```
uvicorn main:app --reload
```

## Swagger

http://127.0.0.1:8000/docs

## Notes

- No migrations are used; `create_all()` runs on startup and skips tables that
  already exist. It never drops or alters anything.
- Tables: `students`, `courses`, `enrollments`.
