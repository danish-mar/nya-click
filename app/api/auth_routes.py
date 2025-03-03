from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models import User
from app.services.auth_manager import AuthManager
from app.extensions import db
from app.services.middleware import login_required

auth_bp = Blueprint('auth_bp', __name__)

# 🔹 User Login API
@auth_bp.route('/login', methods=['POST'])
def login():
    """User login API"""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    session_token = AuthManager.create_session(user.user_id)
    return jsonify({'message': 'Login successful', 'session_token': session_token}), 200

# 🔹 Admin Login API
@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login API"""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    admin = User.query.filter_by(email=email, username='admin').first()  # Admin must be named "admin"
    if not admin or not check_password_hash(admin.password, password):
        return jsonify({'error': 'Invalid admin credentials'}), 401

    session_token = AuthManager.create_session(admin.user_id, is_admin=True)
    return jsonify({'message': 'Admin login successful', 'session_token': session_token}), 200

# 🔹 User Logout API
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout API"""
    session_token = request.headers.get('Authorization')
    if not session_token or not AuthManager.get_user(session_token):
        return jsonify({'error': 'Invalid session'}), 401

    AuthManager.remove_session(session_token)
    return jsonify({'message': 'Logout successful'}), 200

# 🔹 Admin Logout API
@auth_bp.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout API"""
    session_token = request.headers.get('Authorization')
    if not session_token or not AuthManager.get_admin(session_token):
        return jsonify({'error': 'Invalid admin session'}), 401

    AuthManager.remove_session(session_token)
    return jsonify({'message': 'Admin logout successful'}), 200

# 🔹 Get Logged-in User API
@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Retrieve logged-in user details"""
    session_token = request.headers.get('Authorization')
    user_id = AuthManager.get_user(session_token)
    if not user_id:
        return jsonify({'error': 'Invalid session'}), 401

    user = User.query.get(user_id)
    return jsonify({'user_id': user.user_id, 'username': user.username, 'email': user.email}), 200
