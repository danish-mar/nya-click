import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///photos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
