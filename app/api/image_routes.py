from flask import Blueprint, jsonify, request
from app.services.image_manager import ImageManager
from datetime import datetime

image_bp = Blueprint('image_bp', __name__)

@image_bp.route('/images', methods=['GET'])
def get_images():
    """Fetch all images"""
    images = ImageManager.get_all_images()

    return jsonify([{
        'image_id': img.image_id,
        'title': img.title,
        'desc': img.desc,
        'date': img.date.strftime('%Y-%m-%d') if isinstance(img.date, datetime) else None,  # ✅ Ensure it's datetime
        'location': img.location,
        'like_count': img.like_count
    } for img in images])
