from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import create_tables, get_db
from models import Employee
from schemas import EmployeeCreate, EmployeeResponse
from security import verify_api_key


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    create_tables()
    yield


app = FastAPI(
    title="Employee Management API",
    description="Employee CRUD API with API Key Authentication",
    version="1.0.0",
    lifespan=lifespan
)

UNAUTHORIZED_RESPONSE = {
    401: {"description": "API key is missing or invalid"}
}

NOT_FOUND_RESPONSE = {
    404: {"description": "Employee not found"}
}

CONFLICT_RESPONSE = {
    409: {"description": "Employee with this email already exists"}
}


@app.get(
    "/employees",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):
    employees = db.scalars(
        select(Employee).order_by(Employee.id)
    ).all()

    return employees

@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    responses={**UNAUTHORIZED_RESPONSE, **CONFLICT_RESPONSE}
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    existing_employee = db.scalar(
        select(Employee).where(
            Employee.email == employee.email
        )
    )

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this email already exists"
        )

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        age=employee.age,
        department=employee.department,
        salary=employee.salary
    )

    db.add(new_employee)

    try:
        db.commit()
        db.refresh(new_employee)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this email already exists"
        )

    return new_employee

@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    responses={
        **UNAUTHORIZED_RESPONSE,
        **NOT_FOUND_RESPONSE,
        **CONFLICT_RESPONSE
    }
)
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):

    existing_employee = db.get(
        Employee,
        employee_id
    )

    if existing_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.age = employee.age
    existing_employee.department = employee.department
    existing_employee.salary = employee.salary

    try:
        db.commit()
        db.refresh(existing_employee)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this email already exists"
        )

    return existing_employee

@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**UNAUTHORIZED_RESPONSE, **NOT_FOUND_RESPONSE}
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):

    employee = db.get(
        Employee,
        employee_id
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()