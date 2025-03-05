from flask import Blueprint

from app.api.image_routes import image_bp
from app.api.comment_route import comment_bp
from app.api.like_routes import like_bp
from app.api.like_routes import like_bp
from app.api.auth_routes import auth_bp
from app.api.admin_routes import admin_bp


api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(image_bp, url_prefix='/api')
api_bp.register_blueprint(comment_bp, url_prefix='/api')
api_bp.register_blueprint(like_bp, url_prefix='/api')
api_bp.register_blueprint(admin_bp, url_prefix='/admin')
