from app import db


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    customer = db.relationship(
        "User",
        back_populates="cart"
    )

    items = db.relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("cart.id", ondelete="CASCADE"),
        nullable=False
    )

    food_item_id = db.Column(
        db.Integer,
        db.ForeignKey("food_items.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    cart = db.relationship(
        "Cart",
        back_populates="items"
    )

    food_item = db.relationship(
        "FoodItem"
    )