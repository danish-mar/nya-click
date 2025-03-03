from app.models import Comment, db

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
        """Get all comments for a specific image"""
        return Comment.query.filter_by(image_id=image_id).all()
