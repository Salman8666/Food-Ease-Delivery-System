from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role_id != 1:
        flash('Access Denied. Executive clearance required.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')