from flask import Blueprint, jsonify, request

from app.services.auth_manager import AuthManager
from app.services.comment_manager import CommentManager
from app.services.middleware import login_required

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('/comments/<int:image_id>', methods=['GET'])
def get_comments(image_id):
    """Fetch comments for a specific image"""
    comments = CommentManager.get_comments_by_image(image_id)
    return jsonify([{
        'comment_id': c.comment_id,
        'user_id': c.user_id,
        'comment': c.comment,
        'created_at': c.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for c in comments])


@comment_bp.route('/comments/<int:image_id>/', methods=['POST'])
@login_required
def add_comment(image_id):
    """Add a new comment to an image"""
    session_token = request.headers.get('Authorization')
    user_id = AuthManager.get_user(session_token)
    if not user_id:
        return jsonify({'error': 'Invalid session'}), 401

    data = request.json
    new_comment = CommentManager.add_comment(user_id, image_id, data['comment'])
    if new_comment:
        return jsonify({'message': 'Comment added!', 'comment_id': new_comment.comment_id}), 201
    return jsonify({'message': 'Failed to add comment'}), 400

