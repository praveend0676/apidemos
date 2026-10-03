from pydantic import BaseModel, ConfigDict, EmailStr, Field


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

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    course: str