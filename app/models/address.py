from app import db

class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    customer = db.relationship(
        "User",
        back_populates="addresses"
    )

    orders = db.relationship(
        "Order",
        back_populates="address"
    )

    def __repr__(self):
        return f"<Address {self.id}>"