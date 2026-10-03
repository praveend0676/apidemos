# 👨‍💼 Employee Management API — FastAPI + API Key Authentication

A beginner-friendly **Employee Management REST API** built using **Python, FastAPI, Pydantic, SQLAlchemy, and SQLite**.

This project demonstrates how to build CRUD APIs and protect selected endpoints using an **API key passed through the HTTP request header**.

---

## 📌 Problem Statement

Build a small Employee Management API that allows users to:

* Create employees
* View employees
* Update employee information
* Delete employees

Some APIs must be protected using an API key.

The client should send the API key using the following HTTP header:

```text
X-API-Key: super30-secret-key
```

If the API key is missing or incorrect, the API should reject the request with an appropriate HTTP authentication error.

The application should also use **Pydantic validation** to validate employee information before it is stored in the database.

---

# 🎯 Project Objectives

This project demonstrates:

* Python and FastAPI integration
* REST API development
* CRUD operations
* HTTP methods
* HTTP status codes
* Pydantic validation
* SQLAlchemy ORM
* SQLite database
* API-key authentication
* FastAPI dependency injection
* Error handling
* Swagger UI
* Database sessions
* Separation of application responsibilities

---

# 🏗️ Application Architecture

```text
                         Client
                           │
                           │ HTTP Request
                           ↓
                    ┌─────────────┐
                    │   FastAPI   │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ↓                         ↓
       Pydantic Validation        API Key Validation
              │                         │
              │                   X-API-Key
              │                         │
              │                  ┌──────┴──────┐
              │                  │             │
              │                Invalid       Valid
              │                  │             │
              │                 401           ↓
              │                            Continue
              │                               │
              └──────────────┬────────────────┘
                             ↓
                       SQLAlchemy ORM
                             ↓
                          SQLite
                             ↓
                     JSON Response
```

---

# 📁 Project Structure

```text
employee-management-api/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── security.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## File Responsibilities

### `main.py`

Contains:

* FastAPI application
* API endpoints
* CRUD logic
* Error handling
* Dependency injection

### `models.py`

Contains SQLAlchemy database models.

### `schemas.py`

Contains Pydantic request and response models.

### `database.py`

Contains:

* Database URL
* SQLAlchemy engine
* Session factory
* Database dependency

### `security.py`

Contains API-key validation logic.

### `requirements.txt`

Contains project dependencies.

### `.env`

Contains environment-specific configuration such as secrets.

### `.gitignore`

Prevents files such as `.env`, virtual environments, and database files from being committed.

---

# 🧰 Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Programming language      |
| FastAPI    | REST API framework        |
| Pydantic   | Data validation           |
| SQLAlchemy | ORM/database interaction  |
| SQLite     | Database                  |
| Uvicorn    | ASGI application server   |
| Swagger UI | API testing/documentation |

---

# 🔐 API Authentication

This project uses a simple API-key authentication mechanism.

The client sends:

```text
X-API-Key: super30-secret-key
```

Example:

```text
GET /employees
X-API-Key: super30-secret-key
```

The protected endpoints verify this key before executing the API logic.

---

# 🔑 API Key Flow

```text
Client
  │
  │ X-API-Key
  ↓
FastAPI
  │
  ↓
verify_api_key()
  │
  ├── Missing → 401 Unauthorized
  │
  ├── Invalid → 401 Unauthorized
  │
  └── Valid → Continue
                   │
                   ↓
              API Endpoint
```

---

# ⚠️ Security Note

For this learning project, the API key can be demonstrated as:

```text
super30-secret-key
```

In a real production application, secrets should **not** be hard-coded or committed to GitHub.

Instead, use:

```text
.env
```

or a proper secret-management solution.

Example:

```text
API_KEY=super30-secret-key
```

Also, production APIs should use HTTPS to protect credentials while they are transmitted.

---

# ⚙️ Environment Variables

Configuration is loaded from `.env` using `python-dotenv`.

| Variable       | Purpose                                    | Default                    |
| -------------- | ------------------------------------------ | -------------------------- |
| `API_KEY`      | Key expected in the `X-API-Key` header      | `super30-secret-key`       |
| `DATABASE_URL` | SQLAlchemy database connection string       | `sqlite:///./employees.db` |

Example `.env`:

```text
API_KEY=super30-secret-key
DATABASE_URL=sqlite:///./employees.db
```

How they are used:

```text
.env
  │
  ├── API_KEY      ──► security.py  ──► verify_api_key()
  │
  └── DATABASE_URL ──► database.py  ──► create_engine()
```

Notes:

* `.env` is ignored by Git, so it is never committed.
* If `.env` is missing, the defaults above are used and the project still runs.
* Real environment variables always take priority over the values in `.env`.
* `check_same_thread=False` is applied only for SQLite connections.

---

# 🗄️ Database Model

The application uses an `employees` table.

```text
employees
│
├── id
├── name
├── email
├── age
├── department
└── salary
```

Example employee:

```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 30,
  "department": "IT",
  "salary": 75000
}
```

---

# 🧩 Pydantic Validation

Employee data is validated using Pydantic.

Example:

```python
class EmployeeCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    age: int = Field(
        gt=18,
        lt=100
    )

    department: str = Field(
        min_length=2,
        max_length=100
    )

    salary: float = Field(
        gt=0
    )
```

This provides validation such as:

```text
Name
 ├── Minimum 2 characters
 └── Maximum 100 characters

Email
 └── Must be a valid email format

Age
 ├── Greater than 18
 └── Less than 100

Salary
 └── Must be greater than 0
```

---

# 🌐 API Endpoints

## 1. Get All Employees

```text
GET /employees
```

### Authentication

Public endpoint.

No API key required.

### Example

```text
GET http://127.0.0.1:8000/employees
```

### Response

```json
[
  {
    "id": 1,
    "name": "Rahul",
    "email": "rahul@gmail.com",
    "age": 30,
    "department": "IT",
    "salary": 75000
  }
]
```

### Status Code

```text
200 OK
```

---

# 2. Create Employee

```text
POST /employees
```

### Authentication

Protected.

Requires:

```text
X-API-Key: super30-secret-key
```

### Request Body

```json
{
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 30,
  "department": "IT",
  "salary": 75000
}
```

### Successful Response

```text
201 Created
```

Example:

```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 30,
  "department": "IT",
  "salary": 75000
}
```

---

# 3. Update Employee

```text
PUT /employees/{employee_id}
```

### Authentication

Protected.

Requires:

```text
X-API-Key: super30-secret-key
```

Example:

```text
PUT /employees/1
```

### Request Body

```json
{
  "name": "Rahul Kumar",
  "email": "rahul.kumar@gmail.com",
  "age": 31,
  "department": "Engineering",
  "salary": 90000
}
```

### Successful Response

```text
200 OK
```

---

# 4. Delete Employee

```text
DELETE /employees/{employee_id}
```

### Authentication

Protected.

Requires:

```text
X-API-Key: super30-secret-key
```

Example:

```text
DELETE /employees/1
```

### Successful Response

```text
204 No Content
```

---

# 📊 API Summary

| Method | Endpoint                   | Authentication | Purpose           |
| ------ | -------------------------- | -------------- | ----------------- |
| GET    | `/employees`               | ❌ No           | Get all employees |
| POST   | `/employees`               | ✅ API Key      | Create employee   |
| PUT    | `/employees/{employee_id}` | ✅ API Key      | Update employee   |
| DELETE | `/employees/{employee_id}` | ✅ API Key      | Delete employee   |

---

# 🚨 Error Handling

## Missing API Key

Request:

```text
POST /employees
```

without:

```text
X-API-Key
```

Expected:

```text
401 Unauthorized
```

Example response:

```json
{
  "detail": "API key is missing"
}
```

---

# ❌ Invalid API Key

Send:

```text
X-API-Key: wrong-key
```

Expected:

```text
401 Unauthorized
```

Example:

```json
{
  "detail": "Invalid API key"
}
```

---

# ❌ Employee Not Found

For example:

```text
PUT /employees/999
```

if employee `999` does not exist.

Expected:

```text
404 Not Found
```

Response:

```json
{
  "detail": "Employee not found"
}
```

---

# ❌ Duplicate Email

If an employee already exists with:

```text
rahul@gmail.com
```

and another employee is created using the same email, the API should return:

```text
409 Conflict
```

Example:

```json
{
  "detail": "Employee with this email already exists"
}
```

---

# ❌ Invalid Employee Data

Example:

```json
{
  "name": "R",
  "email": "wrong-email",
  "age": 10,
  "department": "",
  "salary": -500
}
```

Pydantic validation rejects the request.

FastAPI returns:

```text
422 Unprocessable Entity
```

---

# 📡 HTTP Status Codes Used

| Status | Meaning                       |
| ------ | ----------------------------- |
| 200    | Successful request            |
| 201    | Resource successfully created |
| 204    | Resource successfully deleted |
| 401    | Authentication failed/missing |
| 404    | Resource not found            |
| 409    | Conflict                      |
| 422    | Validation error              |

---

# ⚙️ Installation

## Step 1 — Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Example:

```bash
git clone https://github.com/praveend0676/employee-management-api.git
```

---

# Step 2 — Open the Project

```bash
cd employee-management-api
```

---

# Step 3 — Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

---

# Step 4 — Activate Virtual Environment

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If activation is successful, the terminal should display:

```text
(.venv)
```

---

# Step 5 — Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Step 6 — Run the Application

```powershell
uvicorn main:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# 📚 Swagger UI

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

* View endpoints
* Enter request data
* Add API headers
* Execute APIs
* View responses
* Test error scenarios

---

# 🧪 Swagger Testing Flow

Follow this sequence when demonstrating the project.

## Test 1 — GET Employees

```text
GET /employees
```

Execute without API key.

Expected:

```text
200 OK
```

---

## Test 2 — POST Without API Key

```text
POST /employees
```

Do not provide the API key.

Expected:

```text
401 Unauthorized
```

---

## Test 3 — POST With Incorrect API Key

Use:

```text
X-API-Key: wrong-key
```

Expected:

```text
401 Unauthorized
```

---

## Test 4 — POST With Correct API Key

Use:

```text
X-API-Key: super30-secret-key
```

Request:

```json
{
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 30,
  "department": "IT",
  "salary": 75000
}
```

Expected:

```text
201 Created
```

---

## Test 5 — GET Employees Again

```text
GET /employees
```

Expected:

```text
200 OK
```

The newly created employee should be displayed.

---

## Test 6 — PUT Employee

```text
PUT /employees/1
```

Use the correct API key.

Expected:

```text
200 OK
```

---

## Test 7 — DELETE Employee

```text
DELETE /employees/1
```

Use the correct API key.

Expected:

```text
204 No Content
```

---

# 🔄 Complete Request Flow

For a protected POST request:

```text
Client
  │
  │ POST /employees
  │ X-API-Key
  │ JSON Body
  ↓
FastAPI
  │
  ├───────────────┐
  ↓               ↓
Pydantic       API Key
Validation     Validation
  │               │
  │          ┌────┴────┐
  │          ↓         ↓
  │       Invalid     Valid
  │          ↓         ↓
  │         401      Continue
  │                    │
  └─────────┬──────────┘
            ↓
       Business Logic
            ↓
        SQLAlchemy
            ↓
          SQLite
            ↓
       JSON Response
```

---

# 🧠 Important Concepts

## 1. FastAPI

FastAPI is used to build the REST API.

```python
app = FastAPI()
```

---

## 2. Pydantic

Pydantic validates incoming request data.

```python
class EmployeeCreate(BaseModel):
```

---

## 3. SQLAlchemy

SQLAlchemy provides ORM-based database interaction.

```python
class Employee(Base):
```

---

## 4. Dependency Injection

FastAPI dependencies provide reusable functionality.

Database:

```python
Depends(get_db)
```

API authentication:

```python
Depends(verify_api_key)
```

---

## 5. API Key Authentication

The API key is sent in:

```text
X-API-Key
```

Example:

```text
X-API-Key: super30-secret-key
```

---

# 🔐 Public vs Protected APIs

```text
                 Employee API
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
       PUBLIC                 PROTECTED
          │                       │
    GET /employees          POST /employees
                            PUT /employees/{id}
                            DELETE /employees/{id}
                                  │
                                  ↓
                              X-API-Key
                                  │
                         ┌────────┴────────┐
                         ↓                 ↓
                       Invalid           Valid
                         ↓                 ↓
                       401              Continue
```

---

# 📈 Learning Flow

This project builds on the following concepts:

```text
Python
   ↓
FastAPI
   ↓
REST API
   ↓
HTTP Methods
   ↓
CRUD
   ↓
Pydantic Validation
   ↓
SQLAlchemy
   ↓
SQLite
   ↓
Dependency Injection
   ↓
API Key Authentication
   ↓
Error Handling
   ↓
Swagger UI
```

---

# 🎥 YouTube Video Demonstration

The video should explain the project in the following order:

### 1. Introduction

Explain what an API is and why authentication is required.

### 2. Problem Statement

Explain the Employee Management API.

### 3. Project Structure

Explain:

```text
main.py
models.py
schemas.py
database.py
security.py
```

### 4. Database

Explain SQLAlchemy and SQLite.

### 5. Pydantic

Explain employee validation.

### 6. API Key Authentication

Explain:

```text
X-API-Key
```

and:

```text
super30-secret-key
```

### 7. API Endpoints

Explain:

```text
GET
POST
PUT
DELETE
```

### 8. Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

### 9. Demonstrate Authentication

Show:

```text
Missing key → 401
Wrong key   → 401
Correct key → API executes
```

### 10. Demonstrate CRUD

Show:

```text
Create
  ↓
Read
  ↓
Update
  ↓
Delete
```

### 11. Demonstrate Validation

Send invalid employee data and show the validation response.

### 12. Explain Complete Flow

```text
Client
 ↓
FastAPI
 ↓
Authentication
 ↓
Pydantic
 ↓
Business Logic
 ↓
SQLAlchemy
 ↓
SQLite
 ↓
Response
```

---

# 🧪 Example Employee Data

You can use the following employees during the demonstration.

### Employee 1

```json
{
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "age": 30,
  "department": "IT",
  "salary": 75000
}
```

### Employee 2

```json
{
  "name": "Priya",
  "email": "priya@gmail.com",
  "age": 28,
  "department": "HR",
  "salary": 65000
}
```

### Employee 3

```json
{
  "name": "Arun",
  "email": "arun@gmail.com",
  "age": 35,
  "department": "Finance",
  "salary": 85000
}
```

---

# 📦 Requirements

Example `requirements.txt`:

```text
fastapi
uvicorn
sqlalchemy
pydantic[email]
python-dotenv
```

Install:

```powershell
pip install -r requirements.txt
```

---

# 🚀 Possible Future Enhancements

This project can be extended with:

* JWT authentication
* OAuth2 authentication
* Role-based access control
* Admin and employee roles
* Password authentication
* Pagination
* Search employees
* Department filtering
* Salary filtering
* PostgreSQL
* MySQL
* Docker
* Automated tests
* CI/CD
* Environment-based configuration
* Secret management

---

# 🎓 Learning Outcomes

After completing this project, you should be able to:

* Create FastAPI applications
* Build REST APIs
* Understand HTTP methods
* Create CRUD operations
* Use Pydantic models
* Validate API request data
* Create SQLAlchemy models
* Connect FastAPI to SQLite
* Manage database sessions
* Use FastAPI dependency injection
* Implement API-key authentication
* Handle HTTP errors
* Use HTTP status codes
* Test APIs using Swagger UI
* Understand public and protected endpoints
* Explain the complete API request lifecycle

---

# ⭐ Key Takeaway

The most important concept in this project is understanding how authentication fits into an API.

```text
                    API Request
                         │
                         ↓
                    FastAPI
                         │
                  API Key Check
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
           Invalid                 Valid
              ↓                     ↓
        401 Unauthorized       Pydantic
                                   │
                                   ↓
                              SQLAlchemy
                                   │
                                   ↓
                                SQLite
                                   │
                                   ↓
                              API Response
```

> **FastAPI handles the API, Pydantic validates the data, API-key authentication protects the endpoints, SQLAlchemy manages database interaction, and SQLite stores the employee information.**

---

# 👨‍💻 Project Summary

This project is a practical introduction to building a **secured CRUD REST API using Python and FastAPI**.

It combines:

```text
Python
+
FastAPI
+
Pydantic
+
SQLAlchemy
+
SQLite
+
API Key Authentication
+
Swagger UI
```

into one small real-world application.

---