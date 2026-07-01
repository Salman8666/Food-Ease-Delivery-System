from flask_mail import Message
from app import create_app
# Simply acts as a skeleton connector for asynchronous notification hooks
def send_order_update_email(user_email, order_id, status):
    pass