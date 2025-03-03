from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Import Flask-Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Initialize Migrate
