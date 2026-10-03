from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Student
from schemas import StudentCreate, StudentResponse


app = FastAPI(
    title="Student Management API",
    description="CRUD API for managing students",
    version="1.0.0"
)

# Create the students table when the application starts
Base.metadata.create_all(bind=engine)


# -----------------------------
# ROOT
# -----------------------------

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {
        "message": "Student Management API",
        "docs": "/docs"
    }


# -----------------------------
# CREATE STUDENT
# -----------------------------

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    email = student.email.lower()

    # Prevent duplicate email addresses
    existing = db.query(Student).filter(Student.email == email).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with this email already exists"
        )

    new_student = Student(
        name=student.name,
        email=email,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# -----------------------------
# GET ALL STUDENTS
# -----------------------------

@app.get(
    "/students",
    response_model=list[StudentResponse],
    status_code=status.HTTP_200_OK
)
def get_students(db: Session = Depends(get_db)):

    return db.query(Student).order_by(Student.id).all()


# -----------------------------
# GET STUDENT BY ID
# -----------------------------

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK
)
def get_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


# -----------------------------
# UPDATE STUDENT
# -----------------------------

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK
)
def update_student(
    student_id: int,
    updated_student: StudentCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    email = updated_student.email.lower()

    # The new email must not belong to another student
    clash = db.query(Student).filter(
        Student.email == email,
        Student.id != student_id
    ).first()

    if clash:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with this email already exists"
        )

    student.name = updated_student.name
    student.email = email
    student.age = updated_student.age
    student.course = updated_student.course

    db.commit()
    db.refresh(student)

    return student


# -----------------------------
# DELETE STUDENT
# -----------------------------

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()