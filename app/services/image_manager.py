from app.models import Image, db

class ImageManager:
    @staticmethod
    def get_all_images():
        """Retrieve all images from the database"""
        return Image.query.all()

    @staticmethod
    def get_image_by_id(image_id):
        """Retrieve a single image by its ID"""
        return Image.query.get(image_id)

    @staticmethod
    def add_image(title, desc, location):
        """Only Admins can add images"""
        new_image = Image(title=title, desc=desc, location=location)
        db.session.add(new_image)
        db.session.commit()
        return new_image

    @staticmethod
    def delete_image(image_id):
        """Delete an image"""
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()
            return True
        return False
