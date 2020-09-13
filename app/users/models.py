from datetime import datetime

from app.database import db
from app.users.utils import generate_token


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    tokens = db.relationship(
        'Token',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    __mapper_args__ = {
        'order_by': created_at
    }
    __tablename__ = 'users'

    def __str__(self):
        return (
            '<{class_name}('
            'user_id={self.id}, '
            'email="{self.email}")>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class Token(db.Model):
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), default=generate_token, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __mapper_args__ = {
        'order_by': created_at
    }
    __tablename__ = 'user_tokens'

    def __str__(self):
        return (
            '<{class_name}('
            'token={self.key}, '
            'username="{self.user.email}")">'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
