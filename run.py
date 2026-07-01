from app import create_app, db
from app.models.user import Role
from flask import redirect, url_for

app = create_app()

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Seed core target system roles if completely empty
        if not Role.query.first():
            admin_role = Role(id=1, name='Admin')
            customer_role = Role(id=2, name='Customer')
            restaurant_role = Role(id=3, name='Restaurant')
            delivery_role = Role(id=4, name='Delivery')
            db.session.add_all([admin_role, customer_role, restaurant_role, delivery_role])
            db.session.commit()
            
    app.run(debug=True)