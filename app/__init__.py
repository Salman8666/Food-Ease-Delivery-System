from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_migrate import Migrate
from app.config import Config

# Initialize Extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
sess = Session()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind Extensions to App Context
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    sess.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    # -------------------------------------------------------------
    # THE FIX: Tell Flask-Login how to load a user from the database
    # -------------------------------------------------------------
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # -------------------------------------------------------------

    # Register Blueprints
    from app.auth import auth_bp
    from app.customer.routes import customer_bp
    from app.restaurant.routes import restaurant_bp
    from app.delivery.routes import delivery_bp
    from app.admin.routes import admin_bp
    from app.api.endpoints import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(restaurant_bp, url_prefix='/restaurant')
    app.register_blueprint(delivery_bp, url_prefix='/delivery')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app