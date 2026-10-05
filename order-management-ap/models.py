import enum

from sqlalchemy import CheckConstraint, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class OrderStatus(str, enum.Enum):
    """Allowed order states and the only valid forward path through the workflow."""

    PLACED = "PLACED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


ALLOWED_TRANSITIONS: dict[OrderStatus, OrderStatus] = {
    OrderStatus.PLACED: OrderStatus.PROCESSING,
    OrderStatus.PROCESSING: OrderStatus.SHIPPED,
    OrderStatus.SHIPPED: OrderStatus.DELIVERED,
}


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price > 0", name="ck_products_price_positive"),
        CheckConstraint("stock >= 0", name="ck_products_stock_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    order_items = relationship(
        "OrderItem",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r} stock={self.stock}>"


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_orders_total_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String(100), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(
        Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.PLACED,
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderItem.id",
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} customer={self.customer!r} status={self.status}>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    @property
    def line_total(self) -> float:
        return round(self.unit_price * self.quantity, 2)

    def __repr__(self) -> str:
        return f"<OrderItem order_id={self.order_id} product_id={self.product_id} qty={self.quantity}>"