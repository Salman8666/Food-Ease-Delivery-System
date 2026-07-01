from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for
)

from flask_login import login_required, current_user

from app import db

from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.food import FoodItem
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.address import Address
from app.models.delivery import Delivery

customer_bp = Blueprint("customer", __name__)


# ======================================================
# CUSTOMER DASHBOARD
# ======================================================



# ======================================================
# BROWSE RESTAURANTS
# ======================================================



# ======================================================
# ADD TO CART
# ======================================================

@customer_bp.route("/cart/add/<int:food_id>", methods=["POST"])
@login_required
def add_to_cart(food_id):

    food = FoodItem.query.get_or_404(food_id)

    if not food.is_available:
        flash(
            "This food item is currently unavailable.",
            "warning"
        )
        return redirect(request.referrer)

    cart = Cart.query.filter_by(
        customer_id=current_user.id
    ).first()

    if not cart:
        cart = Cart(customer_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    item = CartItem.query.filter_by(
        cart_id=cart.id,
        food_item_id=food.id
    ).first()

    if item:
        item.quantity += 1

    else:
        item = CartItem(
            cart_id=cart.id,
            food_item_id=food.id,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()

    flash("Item added to cart successfully.", "success")

    return redirect(request.referrer)


# ======================================================
# VIEW CART
# ======================================================

@customer_bp.route("/cart")
@login_required
def view_cart():

    cart = Cart.query.filter_by(
        customer_id=current_user.id
    ).first()

    total = 0

    if cart:
        for item in cart.items:
            total += item.food_item.price * item.quantity

    return render_template(
        "customer/cart.html",
        cart=cart,
        total=total
    )


# ======================================================
# UPDATE CART
# ======================================================

@customer_bp.route("/cart/update/<int:item_id>", methods=["POST"])
@login_required
def update_cart(item_id):

    item = CartItem.query.get_or_404(item_id)

    cart = Cart.query.filter_by(
        customer_id=current_user.id
    ).first()

    if not cart or item.cart_id != cart.id:

        flash("Unauthorized access.", "danger")

        return redirect(
            url_for("customer.view_cart")
        )

    try:
        quantity = int(
            request.form.get("quantity", 1)
        )

    except ValueError:

        flash("Invalid quantity.", "danger")

        return redirect(
            url_for("customer.view_cart")
        )

    if quantity <= 0:

        db.session.delete(item)

    else:

        item.quantity = quantity

    db.session.commit()

    flash(
        "Cart updated successfully.",
        "success"
    )

    return redirect(
        url_for("customer.view_cart")
    )


# ======================================================
# REMOVE FROM CART
# ======================================================

@customer_bp.route("/cart/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):

    item = CartItem.query.get_or_404(item_id)

    cart = Cart.query.filter_by(
        customer_id=current_user.id
    ).first()

    if not cart or item.cart_id != cart.id:

        flash("Unauthorized access.", "danger")

        return redirect(
            url_for("customer.view_cart")
        )

    db.session.delete(item)

    db.session.commit()

    flash(
        "Item removed from cart.",
        "success"
    )

    return redirect(
        url_for("customer.view_cart")
    )
    
@customer_bp.route("/checkout")
@login_required
def checkout():

    cart = Cart.query.filter_by(
        customer_id=current_user.id
    ).first()

    if not cart or not cart.items:

        flash("Your cart is empty.", "warning")

        return redirect(url_for("customer.view_cart"))

    # Get customer's saved addresses
    addresses = Address.query.filter_by(
        customer_id=current_user.id
    ).all()

    # Calculate subtotal
    total = sum(
        float(item.food_item.price) * item.quantity
        for item in cart.items
    )

    delivery_fee = 150
    tax = total * 0.05
    grand_total = total + delivery_fee + tax

    return render_template(
        "customer/checkout.html",
        cart=cart,
        addresses=addresses,
        total=total,
        delivery_fee=delivery_fee,
        tax=tax,
        grand_total=grand_total
    )
    
@customer_bp.route("/place-order", methods=["POST"])
@login_required
def place_order():

    cart = Cart.query.filter_by(
        customer_id=current_user.id
    ).first()

    if not cart or not cart.items:

        flash("Your cart is empty.", "warning")

        return redirect(
            url_for("customer.view_cart")
        )

    address_id = request.form.get("address_id")

    payment_method = request.form.get(
        "payment_method",
        "Cash on Delivery"
    )

    address = Address.query.filter_by(
        id=address_id,
        customer_id=current_user.id
    ).first()

    if not address:

        flash(
            "Please select a valid delivery address.",
            "danger"
        )

        return redirect(
            url_for("customer.checkout")
        )

    subtotal = sum(
        item.food_item.price * item.quantity
        for item in cart.items
    )

    delivery_fee = 150

    tax = subtotal * 0.05

    grand_total = subtotal + delivery_fee + tax

    restaurant_id = cart.items[0].food_item.restaurant_id

    try:

        order = Order(
            customer_id=current_user.id,
            restaurant_id=restaurant_id,
            address_id=address.id,
            total_amount=grand_total,
            status="Pending"
        )

        db.session.add(order)

        db.session.flush()

        for item in cart.items:

            order_item = OrderItem(

                order_id=order.id,

                food_item_id=item.food_item_id,

                quantity=item.quantity,

                price=item.food_item.price

            )

            db.session.add(order_item)

        payment = Payment(

            order_id=order.id,

            customer_id=current_user.id,

            payment_method=payment_method,

            payment_status="Pending"

        )

        db.session.add(payment)

        for item in cart.items:

            db.session.delete(item)

        db.session.commit()

        flash(
            "Order placed successfully.",
            "success"
        )

        return redirect(
            url_for(
                "customer.payment",
                order_id=order.id
            )
        )

    except Exception as e:

        db.session.rollback()

        print(e)

        flash(
            "Something went wrong while placing the order.",
            "danger"
        )

        return redirect(
            url_for("customer.checkout")
        )
@customer_bp.route("/address/add")
@login_required
def add_address():
    return render_template("customer/add_address.html")
@customer_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role_id == 1:
        return redirect(url_for("admin.dashboard"))

    elif current_user.role_id == 3:
        return redirect(url_for("restaurant.dashboard"))

    restaurants = Restaurant.query.filter_by(is_open=True).all()

    foods = FoodItem.query.filter_by(is_available=True).all()

    cart = Cart.query.filter_by(
        customer_id=current_user.id
    ).first()

    cart_count = 0

    if cart:
        cart_count = sum(item.quantity for item in cart.items)

    return render_template(
        "customer/dashboard.html",
        restaurants=restaurants,
        foods=foods,
        cart_count=cart_count
    )