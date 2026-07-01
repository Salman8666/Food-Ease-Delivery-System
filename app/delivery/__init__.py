from flask import Blueprint

delivery_bp = Blueprint('delivery', __name__)

from app.delivery import routes