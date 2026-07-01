from app import db

class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )

    delivery_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.Enum(
            "Assigned",
            "Picked",
            "Delivered",
            name="delivery_status_enum"
        ),
        default="Assigned"
    )

    assigned_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    delivered_at = db.Column(db.DateTime)

    order = db.relationship(
        "Order",
        back_populates="delivery"
    )

    delivery_staff = db.relationship(
        "User",
        back_populates="deliveries"
    )

    def __repr__(self):
        return f"<Delivery {self.id}>"