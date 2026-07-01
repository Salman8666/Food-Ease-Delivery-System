from app import db


# ==========================
# Category Model
# ==========================

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    foods = db.relationship(
        "FoodItem",
        back_populates="category",
        lazy=True
    )


# ==========================
# Food Item Model
# ==========================

class FoodItem(db.Model):
    __tablename__ = "food_items"

    id = db.Column(db.Integer, primary_key=True)

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(db.Text)

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    is_available = db.Column(
        db.Boolean,
        default=True
    )

    is_veg = db.Column(
        db.Boolean,
        default=False
    )

    image_url = db.Column(
        db.String(255)
    )

    restaurant = db.relationship(
        "Restaurant",
        back_populates="foods"
    )

    category = db.relationship(
        "Category",
        back_populates="foods"
    )