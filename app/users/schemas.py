from marshmallow import Schema, fields, validates, ValidationError, post_load

from app.database import db
from app.users.models import User, Token


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=False)
    token = fields.Method('get_user_token', dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @validates('email')
    def validate_email(self, email, **kwargs):
        if bool(User.query.filter_by(email=email).first()):
            raise ValidationError(f'"{email}" email address already exists.')

    def get_user_token(self, user):
        try:
            return user.tokens[0].key
        except IndexError:
            return None

    @property
    def instance(self):
        """
        Returns created db entity object after `Schema` loaded.
        """
        try:
            return self._instance
        except AttributeError:
            raise AttributeError(f'"instance" attribute not accessible, you must loaded the schema to access.')

    @post_load
    def create(self, data, **kwargs):
        user = User(**data)
        token = Token()
        user.tokens.append(token)
        db.session.add(user)
        db.session.add(token)
        db.session.commit()
        self._instance = user


class AuthenticateUserSchema(Schema):
    email = fields.Email(required=True)