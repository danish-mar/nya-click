import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.services.image_manager import ImageManager
from app.services.admin_auth import is_admin_logged_in, login_admin, logout_admin
from app.models import User, Image, Comment, Like
from app.extensions import db

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

import os

# Get the absolute path to the project's root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Points to "app/api/"
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Moves up to "app/"

# Correctly set the UPLOAD_FOLDER
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "static", "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# 🔹 Make `is_admin_logged_in()` available in all templates
@admin_bp.context_processor
def inject_admin_status():
    return dict(is_admin_logged_in=is_admin_logged_in)


# 🔹 Admin Login
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if is_admin_logged_in():
        return redirect(url_for("api.admin_bp.dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if login_admin(username, password):
            flash("Logged in successfully!", "success")
            return redirect(url_for("api.admin_bp.dashboard"))
        else:
            flash("Invalid credentials!", "error")

    return render_template("admin/admin_login.html")


# 🔹 Admin Logout
@admin_bp.route("/logout")
def admin_logout():
    logout_admin()
    flash("Logged out!", "success")
    return redirect(url_for("api.admin_bp.admin_login"))


@admin_bp.route("/")
def dashboard():
    if not is_admin_logged_in():
        return redirect(url_for("api.admin_bp.admin_login"))

    total_users = User.query.count()
    total_images = Image.query.count()
    total_comments = Comment.query.count()
    total_likes = Like.query.count()

    # ✅ Fetch recent images and pass them to the template
    recent_images = Image.query.order_by(Image.date.desc()).limit(10).all()

    return render_template("admin/admin_dashboard.html",
                           users=total_users, images=total_images,
                           comments=total_comments, likes=total_likes,
                           recent_images=recent_images)  # ✅ Pass images


# 🔹 Upload Image
@admin_bp.route("/upload", methods=["GET", "POST"])
def upload_image():
    if not is_admin_logged_in():
        return redirect(url_for("api.admin_bp.admin_login"))

    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        file = request.files["file"]

        if not title or not file:
            flash("Title and image are required!", "error")
            return redirect(url_for("api.admin_bp.upload_image"))

        if not allowed_file(file.filename):
            flash("Invalid file type!", "error")
            return redirect(url_for("api.admin_bp.upload_image"))

        filename = secure_filename(file.filename)

        # ✅ Absolute path to save the file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # ✅ Relative path to store in the database
        relative_path = f"/static/images/{filename}"

        ImageManager.add_image(title, desc, relative_path)

        flash("Image uploaded successfully!", "success")
        return redirect(url_for("api.admin_bp.dashboard"))

    return render_template("admin/admin_upload.html")


# 🔹 Edit Image
@admin_bp.route("/edit/<int:image_id>", methods=["GET", "POST"])
def edit_image(image_id):
    if not is_admin_logged_in():
        return redirect(url_for("api.admin_bp.admin_login"))

    image = Image.query.get_or_404(image_id)

    if request.method == "POST":
        image.title = request.form["title"]
        image.desc = request.form["desc"]

        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image.location = filepath  # Update image path

        db.session.commit()
        flash("Image updated successfully!", "success")
        return redirect(url_for("api.admin_bp.dashboard"))

    return render_template("admin/admin_edit.html", image=image)


# 🔹 Image Details (Likes, Comments)
@admin_bp.route("/image/<int:image_id>")
def image_details(image_id):
    if not is_admin_logged_in():
        return redirect(url_for("api.admin_bp.admin_login"))

    image = Image.query.get_or_404(image_id)
    comments = Comment.query.filter_by(image_id=image_id).order_by(Comment.created_at.desc()).limit(5).all()
    likes = Like.query.filter_by(image_id=image_id).count()

    return render_template("admin/admin_image_details.html", image=image, comments=comments, likes=likes)


# 🔹 Userbase Page
@admin_bp.route("/users")
def userbase():
    if not is_admin_logged_in():
        return redirect(url_for("api.admin_bp.admin_login"))

    users = User.query.all()
    return render_template("admin/admin_users.html", users=users)


# 🔹 Delete Image (Along with Comments & Likes)
@admin_bp.route("/delete/<int:image_id>", methods=["POST"])
def delete_image(image_id):
    if not is_admin_logged_in():
        return redirect(url_for("api.admin_bp.admin_login"))

    image = Image.query.get_or_404(image_id)

    # ✅ Remove the image file from the static folder
    if image.location:
        image_path = os.path.join(UPLOAD_FOLDER, os.path.basename(image.location))
        if os.path.exists(image_path):
            os.remove(image_path)

    # ✅ Delete all related comments
    Comment.query.filter_by(image_id=image_id).delete()

    # ✅ Delete all related likes
    Like.query.filter_by(image_id=image_id).delete()

    # ✅ Delete the image itself
    db.session.delete(image)
    db.session.commit()

    flash("Image and all related data deleted successfully!", "success")
    return redirect(url_for("admin_bp.dashboard"))

