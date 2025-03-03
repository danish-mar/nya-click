from functools import wraps
from flask import request, jsonify
from app.services.auth_manager import AuthManager


def login_required(f):
    """Decorator to ensure the user is logged in."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = request.headers.get('Authorization')

        if not session_token or not AuthManager.get_user(session_token):
            return jsonify({'error': 'Unauthorized access'}), 401  # Return 401 if not logged in

        return f(*args, **kwargs)  # Call the original function

    return decorated_function
