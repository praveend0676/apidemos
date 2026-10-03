# 🎓 Student Management API Using Python & FastAPI

A beginner-friendly **Student Management REST API** built using **Python, FastAPI, Pydantic, SQLAlchemy, and SQLite**.

This project demonstrates how to build a complete CRUD-based REST API with database persistence, request validation, error handling, and HTTP status codes.

---

## 📌 Problem Statement

Create a FastAPI application for managing student information.

The application should allow users to:

* Create a new student
* Retrieve all students
* Retrieve a student by ID
* Update student information
* Delete a student
* Validate incoming student data
* Return meaningful HTTP status codes
* Handle cases where a student does not exist
* Prevent duplicate student email addresses

Each student contains:

```text
Student
│
├── ID
├── Name
├── Email
├── Age
└── Course
```

---

# 🎯 Project Objective

The objective of this project is to understand how a real-world Python backend application can be developed using:

* Python
* FastAPI
* REST APIs
* HTTP methods
* Pydantic
* SQLAlchemy ORM
* SQLite database
* Dependency Injection
* CRUD operations
* HTTP status codes
* API validation
* Exception handling
* Swagger UI

---

# 🧩 Technologies Used

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Programming language        |
| FastAPI    | Web API framework           |
| Uvicorn    | ASGI application server     |
| Pydantic   | Request/response validation |
| SQLAlchemy | ORM / database interaction  |
| SQLite     | Database                    |
| Swagger UI | API testing/documentation   |
| Git        | Version control             |
| GitHub     | Source code repository      |

---

# 🏗️ Application Architecture

```text
                    Client
              Swagger UI / Postman
                       │
                       ↓
                  ┌─────────┐
                  │ main.py │
                  │ FastAPI │
                  └────┬────┘
                       │
                       ↓
                ┌─────────────┐
                │ schemas.py  │
                │  Pydantic   │
                │ Validation  │
                └──────┬──────┘
                       │
                       ↓
                ┌─────────────┐
                │ database.py │
                │  SQLAlchemy │
                │   Session   │
                └──────┬──────┘
                       │
                       ↓
                ┌─────────────┐
                │  models.py  │
                │ SQLAlchemy  │
                │    Model    │
                └──────┬──────┘
                       │
                       ↓
                ┌─────────────┐
                │ students.db │
                │   SQLite    │
                └─────────────┘
```

---

# 📁 Project Structure

```text
student-management-api/
│
├── .venv/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── requirements.txt
├── README.md
│
└── students.db
```

### File Responsibilities

### `main.py`

Contains:

* FastAPI application
* API endpoints
* Business logic
* HTTP exceptions
* CRUD operations

### `models.py`

Contains:

* SQLAlchemy database models
* Database table definition
* Columns
* Primary key
* Unique constraints

### `schemas.py`

Contains:

* Pydantic request models
* Pydantic response models
* Input validation

### `database.py`

Contains:

* Database URL
* SQLAlchemy engine
* Session factory
* Database dependency
* Base class

### `students.db`

SQLite database file created automatically when the application starts.

---

# 🔄 CRUD Operations

This project implements complete CRUD functionality.

```text
                 CRUD
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
    CREATE       READ       UPDATE
       │          │          │
      POST        GET        PUT
                              │
                              ↓
                           DELETE
```

API mapping:

```text
CREATE
POST /students

READ
GET /students
GET /students/{student_id}

UPDATE
PUT /students/{student_id}

DELETE
DELETE /students/{student_id}
```

---

# 🌐 API Endpoints

| Method | Endpoint                 | Description       |
| ------ | ------------------------ | ----------------- |
| POST   | `/students`              | Create student    |
| GET    | `/students`              | Get all students  |
| GET    | `/students/{student_id}` | Get student by ID |
| PUT    | `/students/{student_id}` | Update student    |
| DELETE | `/students/{student_id}` | Delete student    |

---

# 📋 Student Fields

A student contains:

```text
id
name
email
age
course
```

Example:

```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 21,
  "course": "Python"
}
```

---

# ⚙️ Prerequisites

Install the following:

* Python 3.x
* pip
* Git
* VS Code or another Python IDE

Check Python:

```powershell
python --version
```

Check pip:

```powershell
pip --version
```

---

# 🚀 Step 1 — Create the Project

Create a project directory:

```powershell
mkdir student-management-api
```

Navigate into it:

```powershell
cd student-management-api
```

---

# 🚀 Step 2 — Create Virtual Environment

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, you can use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

# 📦 Step 3 — Install Dependencies

Install FastAPI:

```powershell
pip install fastapi
```

Install Uvicorn:

```powershell
pip install uvicorn
```

Install SQLAlchemy:

```powershell
pip install sqlalchemy
```

Install email validation:

```powershell
pip install email-validator
```

Or install everything together:

```powershell
pip install fastapi uvicorn sqlalchemy email-validator
```

---

# 📄 Step 4 — Create `requirements.txt`

Create:

```text
requirements.txt
```

Add:

```text
fastapi
uvicorn
sqlalchemy
email-validator
```

Install later using:

```powershell
pip install -r requirements.txt
```

---

# 🗄️ Step 5 — Create `database.py`

The database module creates the SQLAlchemy database connection and provides database sessions to the FastAPI endpoints.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./students.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
```

---

# 🧱 Step 6 — Create `models.py`

The SQLAlchemy model represents the database table.

```python
from sqlalchemy import Column, Integer, String

from database import Base


class Student(Base):

    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(50),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    age = Column(
        Integer,
        nullable=False
    )

    course = Column(
        String(100),
        nullable=False
    )
```

The model creates the following table structure:

```text
students
--------------------------------
id
name
email
age
course
```

---

# 📝 Step 7 — Create `schemas.py`

Pydantic schemas validate incoming API data and define the response structure.

```python
from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50
    )

    email: EmailStr

    age: int = Field(
        gt=0,
        lt=100
    )

    course: str = Field(
        min_length=2,
        max_length=100
    )


class StudentResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    age: int

    course: str

    class Config:
        from_attributes = True
```

---

# 🚀 Step 8 — Create `main.py`

```python
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Student
from schemas import StudentCreate, StudentResponse


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Management API",
    description="CRUD API for managing students",
    version="1.0.0"
)


# ==================================================
# CREATE STUDENT
# ==================================================

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    existing_student = (
        db.query(Student)
        .filter(Student.email == student.email)
        .first()
    )

    if existing_student:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with this email already exists"
        )

    new_student = Student(
        name=student.name,
        email=student.email,
        age=student.age,
        course=student.course
    )

    db.add(new_student)

    db.commit()

    db.refresh(new_student)

    return new_student


# ==================================================
# GET ALL STUDENTS
# ==================================================

@app.get(
    "/students",
    response_model=list[StudentResponse],
    status_code=status.HTTP_200_OK
)
def get_students(
    db: Session = Depends(get_db)
):

    students = db.query(Student).all()

    return students


# ==================================================
# GET STUDENT BY ID
# ==================================================

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


# ==================================================
# UPDATE STUDENT
# ==================================================

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK
)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    student.name = student_data.name
    student.email = student_data.email
    student.age = student_data.age
    student.course = student_data.course

    db.commit()

    db.refresh(student)

    return student


# ==================================================
# DELETE STUDENT
# ==================================================

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    db.delete(student)

    db.commit()

    return
```

---

# ▶️ Step 9 — Run the Application

Run:

```powershell
uvicorn main:app --reload
```

Expected output:

```text
INFO:     Uvicorn running on
http://127.0.0.1:8000
```

---

# 📚 Step 10 — Open Swagger UI

Open your browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI will display:

```text
Student Management API

POST    /students
GET     /students
GET     /students/{student_id}
PUT     /students/{student_id}
DELETE  /students/{student_id}
```

---

# 🧪 API Testing

## 1. POST `/students`

Create a student.

Request:

```json
{
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 21,
  "course": "Python"
}
```

Expected response:

```text
201 Created
```

Example:

```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 21,
  "course": "Python"
}
```

---

# 2. Create Another Student

```json
{
  "name": "Priya",
  "email": "priya@gmail.com",
  "age": 22,
  "course": "FastAPI"
}
```

---

# 3. GET `/students`

Request:

```text
GET /students
```

Expected:

```json
[
  {
    "id": 1,
    "name": "Rahul",
    "email": "rahul@gmail.com",
    "age": 21,
    "course": "Python"
  },
  {
    "id": 2,
    "name": "Priya",
    "email": "priya@gmail.com",
    "age": 22,
    "course": "FastAPI"
  }
]
```

Status:

```text
200 OK
```

---

# 4. GET `/students/{student_id}`

Request:

```text
GET /students/1
```

Response:

```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 21,
  "course": "Python"
}
```

Status:

```text
200 OK
```

---

# 5. GET Non-Existing Student

Try:

```text
GET /students/999
```

Response:

```json
{
  "detail": "Student not found"
}
```

Status:

```text
404 Not Found
```

---

# 6. PUT `/students/{student_id}`

Update student 1.

```text
PUT /students/1
```

Request:

```json
{
  "name": "Rahul Kumar",
  "email": "rahul.kumar@gmail.com",
  "age": 22,
  "course": "Advanced Python"
}
```

Expected:

```text
200 OK
```

---

# 7. DELETE `/students/{student_id}`

Request:

```text
DELETE /students/2
```

Expected:

```text
204 No Content
```

The student is removed from the database.

---

# ❌ Error Handling

The application handles common errors.

## 404 — Student Not Found

Example:

```text
GET /students/999
```

Response:

```json
{
  "detail": "Student not found"
}
```

---

## 409 — Duplicate Email

Try creating another student with:

```json
{
  "name": "Another Rahul",
  "email": "rahul@gmail.com",
  "age": 25,
  "course": "Java"
}
```

Response:

```json
{
  "detail": "Student with this email already exists"
}
```

Status:

```text
409 Conflict
```

---

# 🔍 Pydantic Validation

The API validates incoming data.

For example:

```python
email: EmailStr
```

requires a valid email address.

This is invalid:

```json
{
  "name": "Rahul",
  "email": "wrong-email",
  "age": 21,
  "course": "Python"
}
```

The request will be rejected by validation.

---

## Age Validation

The schema contains:

```python
age: int = Field(
    gt=0,
    lt=100
)
```

Therefore:

```text
age = -5
```

is invalid.

Also:

```text
age = 150
```

is invalid.

---

## Name Validation

The schema contains:

```python
name: str = Field(
    min_length=2,
    max_length=50
)
```

Therefore, the name must contain between 2 and 50 characters.

---

# 📊 HTTP Status Codes

| Status Code | Meaning              | Example            |
| ----------- | -------------------- | ------------------ |
| 200         | Successful request   | GET / PUT          |
| 201         | Resource created     | POST               |
| 204         | Successfully deleted | DELETE             |
| 404         | Resource not found   | Invalid student ID |
| 409         | Conflict             | Duplicate email    |
| 422         | Validation error     | Invalid input      |

---

# 🔄 Complete Request Flow

## Create Student

```text
Client
  ↓
POST /students
  ↓
JSON Request
  ↓
Pydantic Validation
  ↓
FastAPI Endpoint
  ↓
Check Duplicate Email
  ↓
SQLAlchemy
  ↓
SQLite
  ↓
Student Created
  ↓
201 Created
```

---

# 🔄 GET Student Flow

```text
Client
  ↓
GET /students/1
  ↓
FastAPI
  ↓
SQLAlchemy
  ↓
SQLite
  ↓
Find Student
  ↓
Student Found
  ↓
Pydantic Response
  ↓
200 OK
```

---

# 🔄 DELETE Student Flow

```text
Client
  ↓
DELETE /students/1
  ↓
FastAPI
  ↓
Find Student
  ↓
Student Found?
  │
  ├── NO → 404
  │
  └── YES
       ↓
     Delete
       ↓
     Commit
       ↓
     204
```

---

# 🧠 Why Do We Need Separate Files?

## `database.py`

Responsible for:

```text
Database connection
Database engine
Database session
```

---

## `models.py`

Responsible for:

```text
Database structure
Database tables
Database columns
```

---

## `schemas.py`

Responsible for:

```text
API request validation
API response structure
Pydantic models
```

---

## `main.py`

Responsible for:

```text
API endpoints
Business logic
CRUD operations
HTTP errors
```

---

# 🏛️ Architecture Summary

```text
                  FastAPI Application
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Routes         Schemas        Database
      main.py        schemas.py     database.py
          │              │              │
          │              ↓              ↓
          │          Pydantic       SQLAlchemy
          │                             │
          │                             ↓
          └────────────────────────→ models.py
                                        │
                                        ↓
                                   SQLite DB
```

---

# 🎓 OOP / Backend Concepts Demonstrated

This project demonstrates:

* Python classes
* SQLAlchemy ORM
* Pydantic models
* FastAPI routes
* Dependency Injection
* REST API design
* CRUD operations
* Request validation
* Response models
* HTTP status codes
* Exception handling
* Database sessions
* SQLite persistence

---

# 📚 What Is Learned From This Project?

After completing this project, you should be able to:

* Create a FastAPI application
* Create REST API endpoints
* Understand HTTP methods
* Use POST, GET, PUT, and DELETE
* Create Pydantic schemas
* Validate API requests
* Create SQLAlchemy models
* Connect FastAPI to SQLite
* Create database sessions
* Perform CRUD operations
* Handle 404 errors
* Handle duplicate data
* Return appropriate HTTP status codes
* Test APIs using Swagger UI
* Understand the separation between API schemas and database models

---

# 🎥 Suggested YouTube Demonstration Flow

For the project video, demonstrate the following sequence:

```text
1. Introduction
        ↓
2. Problem Statement
        ↓
3. Explain CRUD
        ↓
4. Explain Project Structure
        ↓
5. Explain database.py
        ↓
6. Explain models.py
        ↓
7. Explain schemas.py
        ↓
8. Explain main.py
        ↓
9. Start Uvicorn
        ↓
10. Open Swagger UI
        ↓
11. POST Student
        ↓
12. GET All Students
        ↓
13. GET Student by ID
        ↓
14. PUT Student
        ↓
15. DELETE Student
        ↓
16. Demonstrate 404
        ↓
17. Demonstrate validation
        ↓
18. Demonstrate duplicate email
        ↓
19. Explain SQLite persistence
        ↓
20. Final summary
```

---

# 🖥️ Swagger UI

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to:

* View endpoints
* View request models
* Enter request data
* Execute APIs
* View responses
* Test HTTP status codes
* Demonstrate validation errors

---

# 🔧 Useful Commands

Start application:

```powershell
uvicorn main:app --reload
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Check installed packages:

```powershell
pip list
```

Deactivate virtual environment:

```powershell
deactivate
```

---

# 🔄 Restart the Application

Stop Uvicorn:

```text
CTRL + C
```

Start again:

```powershell
uvicorn main:app --reload
```

Because the application uses SQLite, the data remains in:

```text
students.db
```

---

# 🗃️ Database Persistence

The first simple version of this project used:

```python
students = []
```

That stores data only in memory.

The current version uses:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
SQLite
   ↓
students.db
```

Therefore, student records are stored in a database file rather than only in application memory.

---

# 🚀 Future Enhancements

This project can be extended with:

* Student authentication
* Login and registration
* JWT authentication
* Course management
* Student-course relationships
* PostgreSQL
* MySQL
* Database migrations with Alembic
* Pagination
* Searching students
* Filtering students by course
* Sorting
* Docker
* Unit testing
* Integration testing
* CI/CD
* Cloud deployment
* AWS deployment

---

# 📌 Example Future API Design

The application can later be expanded to:

```text
POST   /students
GET    /students
GET    /students/{id}
PUT    /students/{id}
DELETE /students/{id}

POST   /courses
GET    /courses
GET    /courses/{id}

POST   /enroll
GET    /students/{id}/courses
DELETE /enroll/{id}
```

This would allow the application to become a complete **Student and Course Management System**.

---

# 📦 GitHub Submission

Initialize Git:

```powershell
git init
```

Add files:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Create Student Management FastAPI application"
```

Create a GitHub repository and connect the remote:

```powershell
git remote add origin https://github.com/<username>/student-management-api.git
```

Rename the branch:

```powershell
git branch -M main
```

Push:

```powershell
git push -u origin main
```

---

# 🔐 Important: Do Not Commit the Virtual Environment

Create a `.gitignore` file:

```text
.venv/
__pycache__/
*.pyc
.env
```

If you don't want to commit the local SQLite database:

```text
students.db
```

you can also add:

```text
students.db
```

So the complete `.gitignore` can be:

```text
.venv/
__pycache__/
*.pyc
.env
students.db
```

---

# 🎯 Final Project Flow

```text
                 Student Management API
                           │
                           ↓
                       FastAPI
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          Create          Read         Update
           POST            GET           PUT
             │             │             │
             └─────────────┼─────────────┘
                           ↓
                         DELETE
                           │
                           ↓
                      SQLAlchemy
                           │
                           ↓
                         SQLite
                           │
                           ↓
                     students.db
```

---

# ⭐ Final Takeaway

This project demonstrates how to build a basic real-world backend application using Python and FastAPI.

The key architecture is:

```text
FastAPI
   ↓
Pydantic
   ↓
SQLAlchemy
   ↓
SQLite
```

Where:

```text
FastAPI
→ Handles HTTP requests and API routes

Pydantic
→ Validates request and response data

SQLAlchemy
→ Communicates with the database

SQLite
→ Stores persistent student information
```

The complete CRUD API is:

```text
POST   /students
GET    /students
GET    /students/{student_id}
PUT    /students/{student_id}
DELETE /students/{student_id}
```

This project provides the foundation for building larger FastAPI applications with authentication, PostgreSQL, course management, testing, Docker, and cloud deployment.
