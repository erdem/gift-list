from datetime import datetime

from app.database import db
from app.users.utils import generate_token, hash_md5


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    tokens = db.relationship(
        'Token',
        back_populates='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    lists = db.relationship(
        'List',
        back_populates='owner',
        cascade='all, delete-orphan'
    )

    purchased_list_items = db.relationship(
        'PurchasedListItem',
        back_populates='purchased_by',
        cascade='all, delete-orphan'
    )

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

    def set_password(self, password):
        self.password = hash_md5(password)


class Token(db.Model):
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), default=generate_token, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

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
