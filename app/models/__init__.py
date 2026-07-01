# Make sure Role is at the very top of imports!
from app.models.user import Role, User  
from app.models.restaurant import Restaurant
from app.models.food import FoodItem, Category
from app.models.order import Order, OrderItem
from .address import Address
from .cart import Cart, CartItem
from .payment import Payment
from .delivery import Delivery