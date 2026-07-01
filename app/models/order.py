from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id"),
        nullable=False
    )

    address_id = db.Column(
        db.Integer,
        db.ForeignKey("addresses.id")
    )

    total_amount = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    status = db.Column(
        db.Enum(
            "Pending",
            "Accepted",
            "Preparing",
            "Out For Delivery",
            "Delivered",
            "Cancelled"
        ),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    items = db.relationship(
        "OrderItem",
        backref="order_rel",
        lazy=True,
        cascade="all, delete-orphan"
    )

    address = db.relationship(
        "Address",
        back_populates="orders"
    )

    payment = db.relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )

    delivery = db.relationship(
        "Delivery",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    food_item_id = db.Column(
        db.Integer,
        db.ForeignKey("food_items.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    food_item = db.relationship(
        "FoodItem",
        backref="order_items"
    )