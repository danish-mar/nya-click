import os
from flask import Blueprint, send_from_directory, render_template

from app.services.comment_manager import CommentManager
from app.services.image_manager import ImageManager

static_bp = Blueprint('static_bp', __name__)


@static_bp.route('/', methods=['GET'])
def index():
    """Serve the index.html file"""
    return render_template('index.html')


@static_bp.route('/auth/signin', methods=['GET'])
def sigin_user():
    return render_template('auth/sign_in_user.html')


@static_bp.route('/auth/register', methods=['GET'])
def signup_user():
    return render_template('auth/sign_up_user.html')


@static_bp.route('/auth/admin/login', methods=['GET'])
def login_admin():
    return render_template('auth/admin_signup.html')


@static_bp.route("/image/<int:image_id>", methods=["GET"])
def view_image(image_id):
    """Render the image page dynamically"""
    image = ImageManager.get_image_by_id(image_id)
    if not image:
        return "Image not found", 404

    comments = CommentManager.get_comments_by_image(image_id)  # ✅ Now includes username

    return render_template("image.html", image=image, comments=comments)

