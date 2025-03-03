from app.models import Like, Image, db


class LikeManager:
    @staticmethod
    def like_image(user_id, image_id):
        """Allow a user to like an image"""
        existing_like = Like.query.filter_by(user_id=user_id, image_id=image_id).first()
        if existing_like:
            return None  # User already liked this image

        new_like = Like(user_id=user_id, image_id=image_id)
        db.session.add(new_like)

        # Increment like count
        image = Image.query.get(image_id)
        image.like_count += 1

        db.session.commit()
        return new_like

    @staticmethod
    def unlike_image(user_id, image_id):
        """Allow a user to unlike an image"""
        like = Like.query.filter_by(user_id=user_id, image_id=image_id).first()
        if like:
            db.session.delete(like)

            # Decrement like count
            image = Image.query.get(image_id)
            image.like_count -= 1

            db.session.commit()
            return True
        return False
