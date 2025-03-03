import uuid


class AuthManager:
    """A simple in-memory session store (acts like Redis)"""

    sessions = {}  # Dictionary to store user_id mapped to session_token
    admins = {}  # Dictionary to store admin sessions separately

    @staticmethod
    def create_session(user_id, is_admin=False):
        """Create a new session and store it in memory"""
        session_token = str(uuid.uuid4())  # Generate a unique session token
        if is_admin:
            AuthManager.admins[session_token] = user_id
        else:
            AuthManager.sessions[session_token] = user_id
        return session_token

    @staticmethod
    def get_user(session_token):
        """Retrieve user_id from session token"""
        return AuthManager.sessions.get(session_token, None)

    @staticmethod
    def get_admin(session_token):
        """Retrieve admin_id from session token"""
        return AuthManager.admins.get(session_token, None)

    @staticmethod
    def remove_session(session_token):
        """Logout user by removing session"""
        AuthManager.sessions.pop(session_token, None)
        AuthManager.admins.pop(session_token, None)
