from app.models import Comment, db, User


class CommentManager:
    @staticmethod
    def add_comment(user_id, image_id, comment_text):
        """Add a new comment to an image"""
        new_comment = Comment(user_id=user_id, image_id=image_id, comment=comment_text)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    @staticmethod
    def get_comments_by_image(image_id):
        """Get all comments for a specific image with usernames"""
        return (
            db.session.query(Comment.comment_id, Comment.comment, Comment.created_at, User.username)
            .join(User, Comment.user_id == User.user_id)  # ✅ Join with User table
            .filter(Comment.image_id == image_id)
            .all()
        )
