import os

class Config:
    SECRET_KEY = 'votre-cle-secrete-changez-moi'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/iaounde_conferences'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'logos')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB