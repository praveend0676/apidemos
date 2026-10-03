from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    age: Mapped[int] = mapped_column(
        Integer
    )

    department: Mapped[str] = mapped_column(
        String(100)
    )

    salary: Mapped[float] = mapped_column(
        Float
    )