from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from db.models import AdminUser
from db.database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'admin_id' in session:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = AdminUser.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['admin_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('admin.dashboard'))
            
        flash('Invalid username or password', 'error')
        
    return render_template('admin/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('username', None)
    return redirect(url_for('auth.login'))
