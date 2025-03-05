import os
from dotenv import load_dotenv
from flask import session

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def is_admin_logged_in():
    """Check if admin is logged in"""
    return session.get("admin_logged_in", False)


def login_admin(username, password):
    """Verify admin credentials and log in"""
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        return True
    return False


def logout_admin():
    """Log out admin"""
    session.pop("admin_logged_in", None)
