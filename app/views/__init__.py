from flask import Blueprint

from app.views.static_routes import static_bp

static_route_bp = Blueprint('static_route_bp', __name__)

static_route_bp.register_blueprint(static_bp, url_prefix='/')


