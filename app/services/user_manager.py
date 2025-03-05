from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve user by ID"""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        """Retrieve user by email"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username):
        """Retrieve user by username"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def register_user(username, email, password):
        """Register a new user with hashed password"""

        # Check if username or email already exists
        if UserManager.get_user_by_username(username):
            return {'error': 'Username already exists'}, 400
        if UserManager.get_user_by_email(email):
            return {'error': 'Email already in use'}, 400

        hashed_password = generate_password_hash(password)

        # ✅ Correct way to create a user
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return new_user  # ✅ Return the created user



    @staticmethod
    def verify_password(user, password):
        """Check if the password matches"""
        return check_password_hash(user.password, password)
