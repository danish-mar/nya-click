from datetime import datetime
from flask_login import UserMixin
from app.extensions import db  # Importing db from extensions.py

# 🔹 User Model (Regular Users)
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# 🔹 Image Model (Uploaded by Admin Only)
class Image(db.Model):
    __tablename__ = 'images'

    image_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # ✅ Store as `datetime`
    location = db.Column(db.String(255), nullable=True)
    like_count = db.Column(db.Integer, default=0)

    # Relationships
    comments = db.relationship('Comment', backref='image', lazy=True)
    likes = db.relationship('Like', backref='image', lazy=True)

    def __repr__(self):
        return f'<Image {self.title}>'

# 🔹 Comment Model (Users Comment on Images)
class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.comment[:20]}>'

# 🔹 Like Model (Users Like Images)
class Like(db.Model):
    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), nullable=False)

    def __repr__(self):
        return f'<Like User:{self.user_id} Image:{self.image_id}>'
