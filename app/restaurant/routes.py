from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

restaurant_bp = Blueprint('restaurant', __name__)

@restaurant_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role_id != 3:
        flash('Unauthorized Access Field.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('restaurant/dashboard.html')