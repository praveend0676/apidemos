from pydantic import BaseModel, ConfigDict, Field, field_validator

from models import OrderStatus


# -------------------------
# Product Schemas
# -------------------------

class ProductCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    price: float = Field(
        gt=0
    )

    stock: int = Field(
        ge=0
    )


class ProductResponse(ProductCreate):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------
# Order Item Schemas
# -------------------------

class OrderItemCreate(BaseModel):

    product_id: int = Field(
        gt=0
    )

    quantity: int = Field(
        gt=0
    )


class OrderItemResponse(BaseModel):

    id: int
    product_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------
# Order Schemas
# -------------------------

class OrderCreate(BaseModel):

    customer: str = Field(
        min_length=2,
        max_length=100
    )

    items: list[OrderItemCreate] = Field(
        min_length=1
    )


class OrderResponse(BaseModel):

    id: int
    customer: str
    total_amount: float
    status: OrderStatus
    items: list[OrderItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------
# Status Update
# -------------------------

class OrderStatusUpdate(BaseModel):

    status: OrderStatus

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value):
        if isinstance(value, str):
            return value.strip().upper()

        return value