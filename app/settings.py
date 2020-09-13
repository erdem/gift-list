import os

DEBUG = os.getenv('DEBUG', True)
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', f'sqlite:///{os.path.join(PROJECT_ROOT, "db.sqlite3")}')
SQLALCHEMY_TRACK_MODIFICATIONS = True


