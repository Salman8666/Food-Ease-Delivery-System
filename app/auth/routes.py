from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.models.user import User
from app import db, bcrypt

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('customer.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            # Route logic based on system access role
            if user.role_id == 1:
                return redirect(url_for('admin.dashboard'))
            elif user.role_id == 3:
                return redirect(url_for('restaurant.dashboard'))
            elif user.role_id == 4:
                return redirect(url_for('delivery.dashboard'))
            return redirect(url_for('customer.dashboard'))
        else:
            flash('Invalid login credentials. Please try again.', 'error')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer.dashboard'))
        
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role_id = int(request.form.get('role_id', 2))
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('That email address is already registered.', 'error')
            return render_template('auth/register.html')
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            role_id=role_id
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been successfully created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during creation. Please check database data inputs.', 'error')
            
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))