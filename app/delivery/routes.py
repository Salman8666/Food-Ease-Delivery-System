from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role_id != 4:
        flash('Unauthorized Access Field.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('delivery/dashboard.html')