from pydantic import BaseModel, ConfigDict, Field


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    city: str


class CourseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None


class EnrollmentCreate(BaseModel):
    student_id: int = Field(gt=0)
    course_id: int = Field(gt=0)


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    course_id: int


class StudentCourseResponse(BaseModel):
    enrollment_id: int
    course_id: int
    course_name: str
    description: str | None = None


class StudentCoursesResponse(BaseModel):
    student_id: int
    student_name: str
    courses: list[StudentCourseResponse]


class MessageResponse(BaseModel):
    message: str
