from app import db

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    payment_method = db.Column(
        db.Enum(
            "Cash on Delivery",
            "Credit Card",
            name="payment_method_enum"
        )
    )

    payment_status = db.Column(
        db.Enum(
            "Pending",
            "Paid",
            "Failed",
            name="payment_status_enum"
        ),
        default="Pending"
    )

    transaction_id = db.Column(db.String(100))

    paid_at = db.Column(db.DateTime)

    order = db.relationship(
        "Order",
        back_populates="payment"
    )

    customer = db.relationship(
        "User",
        back_populates="payments"
    )

    def __repr__(self):
        return f"<Payment {self.id}>"