from app import db
from datetime import datetime


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(db.Text)

    cuisine_type = db.Column(db.String(100))

    is_open = db.Column(
        db.Boolean,
        default=True
    )

    rating = db.Column(
        db.Numeric(3, 2),
        default=5.00
    )

    image_url = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Restaurant → Food Items
    foods = db.relationship(
        "FoodItem",
        back_populates="restaurant",
        cascade="all, delete-orphan",
        lazy=True
    )

    # Restaurant → Orders
    orders = db.relationship(
        "Order",
        backref="restaurant",
        lazy=True
    )