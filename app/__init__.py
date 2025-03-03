from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, migrate  # Import migrate
from app.models import User, Image, Comment, Like  # Import models
from app.api import api_bp
from app.views import static_route_bp

def create_app():
    print("Initializing app")
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    # login_manager.init_app(app)
    migrate.init_app(app, db)  # Attach migrate

    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(static_route_bp)

    return app
