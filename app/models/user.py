from app import db
from flask_login import UserMixin
from datetime import datetime

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Role
    role = db.relationship("Role", backref="users")

    # Customer Cart
    cart = db.relationship(
        "Cart",
        back_populates="customer",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Customer Orders
    orders = db.relationship(
        "Order",
        foreign_keys="Order.customer_id",
        backref="customer",
        lazy=True
    )

    # Saved Addresses
    addresses = db.relationship(
        "Address",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    # Payments
    payments = db.relationship(
        "Payment",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    # Deliveries (Delivery Staff)
    deliveries = db.relationship(
        "Delivery",
        foreign_keys="Delivery.delivery_staff_id",
        back_populates="delivery_staff"
    )