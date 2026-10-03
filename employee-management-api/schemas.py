from pydantic import BaseModel, ConfigDict, EmailStr, Field


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


class EmployeeResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    age: int
    department: str
    salary: float

    model_config = ConfigDict(
        from_attributes=True
    )