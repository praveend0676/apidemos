from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from database import (
    check_database_connection,
    create_tables,
    engine,
    get_db,
    session_scope,
)
from models import Course, Enrollment, Student
from schemas import (
    CourseCreate,
    CourseResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    MessageResponse,
    StudentCourseResponse,
    StudentCoursesResponse,
    StudentResponse,
)

SAMPLE_STUDENTS = [
    {"name": "Rahul", "age": 25, "city": "Delhi"},
    {"name": "Priya", "age": 24, "city": "Mumbai"},
    {"name": "Arun", "age": 30, "city": "Pune"},
]


def seed_sample_students() -> None:
    with session_scope() as db:
        already_seeded = db.scalar(select(Student).limit(1))

        if already_seeded is None:
            db.add_all([Student(**student) for student in SAMPLE_STUDENTS])


def commit_or_503(db: Session, detail: str) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        ) from None
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database error while saving the changes"
        ) from None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if not check_database_connection():
        raise RuntimeError("Cannot reach the database. Check DATABASE_URL in your .env file.")

    create_tables()
    seed_sample_students()

    yield

    engine.dispose()


app = FastAPI(
    title="Student Course Enrollment API",
    description="FastAPI application for managing courses and student enrollments",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "Student Course Enrollment API"
    }


# -------------------------------------------------
# GET /students
# -------------------------------------------------

@app.get("/students", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db)
):
    return db.scalars(select(Student).order_by(Student.id)).all()


# -------------------------------------------------
# POST /courses
# -------------------------------------------------

@app.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    new_course = Course(
        name=course.name,
        description=course.description
    )

    db.add(new_course)
    commit_or_503(db, "Course could not be created")

    db.refresh(new_course)

    return new_course


# -------------------------------------------------
# GET /courses
# -------------------------------------------------

@app.get("/courses", response_model=list[CourseResponse])
def get_courses(
    db: Session = Depends(get_db)
):
    return db.scalars(select(Course).order_by(Course.id)).all()


# -------------------------------------------------
# GET /courses/{course_id}
# -------------------------------------------------

@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.get(Course, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return course


# -------------------------------------------------
# POST /enroll
# -------------------------------------------------

@app.post(
    "/enroll",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_student(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    student = db.get(Student, enrollment.student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    course = db.get(Course, enrollment.course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    existing = db.scalar(
        select(Enrollment).where(
            Enrollment.student_id == enrollment.student_id,
            Enrollment.course_id == enrollment.course_id
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course"
        )

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )

    db.add(new_enrollment)
    commit_or_503(db, "Student is already enrolled in this course")

    db.refresh(new_enrollment)

    return new_enrollment


# -------------------------------------------------
# GET /students/{student_id}/courses
# -------------------------------------------------

@app.get(
    "/students/{student_id}/courses",
    response_model=StudentCoursesResponse
)
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    enrollments = db.scalars(
        select(Enrollment)
        .options(selectinload(Enrollment.course))
        .where(Enrollment.student_id == student_id)
        .order_by(Enrollment.id)
    ).all()

    return {
        "student_id": student_id,
        "student_name": student.name,
        "courses": [
            StudentCourseResponse(
                enrollment_id=enrollment.id,
                course_id=enrollment.course.id,
                course_name=enrollment.course.name,
                description=enrollment.course.description
            )
            for enrollment in enrollments
        ]
    }


# -------------------------------------------------
# DELETE /enroll/{enrollment_id}
# -------------------------------------------------

@app.delete(
    "/enroll/{enrollment_id}",
    response_model=MessageResponse
)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    enrollment = db.get(Enrollment, enrollment_id)

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    db.delete(enrollment)
    commit_or_503(db, "Enrollment could not be deleted")

    return {
        "message": "Enrollment deleted successfully"
    }
