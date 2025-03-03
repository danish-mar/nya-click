from flask import Blueprint, jsonify, request

from app.services.like_manager import LikeManager
from app.services.middleware import login_required
from app.services.auth_manager import AuthManager

like_bp = Blueprint('like_bp', __name__)

@like_bp.route('/<int:image_id>/like', methods=['POST'])
@login_required
def like_image(image_id):
    """Like an image"""
    session_token = request.headers.get('Authorization')
    user_id = AuthManager.get_user(session_token)
    new_like = LikeManager.like_image(user_id, image_id)
    if new_like:
        return jsonify({'message': 'Image liked!'}), 201
    return jsonify({'message': 'Already liked'}), 400

@like_bp.route('/<int:image_id>/like', methods=['DELETE'])
@login_required
def unlike_image(image_id):
    session_id = request.headers.get("Authorization")
    user_id = AuthManager.get_user(session_id)
    if LikeManager.unlike_image(user_id, image_id):
        return jsonify({'message': 'Image unliked!'}), 200
    return jsonify({'message': 'Already unliked'}), 400
