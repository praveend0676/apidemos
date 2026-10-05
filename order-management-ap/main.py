from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import ALLOWED_TRANSITIONS, Order, OrderItem, OrderStatus, Product
from schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
    ProductCreate,
    ProductResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Order Management API",
    description="FastAPI application for managing products and orders",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================
# PRODUCT APIs
# ============================================================

@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products(
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .order_by(Product.id)
        .all()
    )

    return products


# ============================================================
# ORDER APIs
# ============================================================

@app.post(
    "/orders",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    # ------------------------------------------
    # Merge duplicate products
    # ------------------------------------------
    # A client may send the same product_id more than once.
    # Quantities are summed first so the stock check below
    # sees the real demand and stock can never go negative.

    requested: dict[int, int] = {}

    for item in order.items:
        requested[item.product_id] = (
            requested.get(item.product_id, 0) + item.quantity
        )

    # ------------------------------------------
    # Validate every product BEFORE writing
    # ------------------------------------------

    order_items: list[OrderItem] = []
    total_amount = 0.0

    for product_id, quantity in requested.items():

        product = db.get(Product, product_id)

        # Product does not exist
        if product is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found"
            )

        # Validate stock
        if quantity > product.stock:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Insufficient stock for "
                    f"product {product.id}. "
                    f"Available stock: {product.stock}"
                )
            )

        # Calculate item amount
        item_amount = round(product.price * quantity, 2)

        total_amount += item_amount

        # Create order item
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price
            )
        )

        # Reserve stock
        product.stock -= quantity

    # ------------------------------------------
    # Create Order
    # ------------------------------------------

    new_order = Order(
        customer=order.customer,
        total_amount=round(total_amount, 2),
        status=OrderStatus.PLACED
    )

    new_order.items = order_items

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@app.get(
    "/orders",
    response_model=list[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db)
):

    orders = (
        db.query(Order)
        .order_by(Order.id)
        .all()
    )

    return orders


@app.get(
    "/orders/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.get(Order, order_id)

    if order is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )

    return order


# ============================================================
# ORDER STATUS API
# ============================================================

@app.put(
    "/orders/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):

    order = db.get(Order, order_id)

    if order is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )

    current_status = OrderStatus(order.status)
    new_status = status_update.status

    expected_status = ALLOWED_TRANSITIONS.get(current_status)

    if expected_status is None:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order is already in {current_status.value} status"
        )

    if new_status != expected_status:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid status transition. "
                f"{current_status.value} can only move to "
                f"{expected_status.value}"
            )
        )

    order.status = expected_status

    db.commit()
    db.refresh(order)

    return order