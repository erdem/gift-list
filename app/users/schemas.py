from marshmallow import Schema, fields, validates, ValidationError, validates_schema

from app.database import db
from app.users.models import User, Token
from app.users.utils import hash_md5


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=False)
    created_at = fields.DateTime(dump_only=True)

    @validates('email')
    def validate_email(self, email, **kwargs):
        if bool(User.query.filter_by(email=email).first()):
            raise ValidationError(f'"{email}" email address already exists.')

    @classmethod
    def create(cls, data, **kwargs):
        user = User(**data)
        user.set_password(data['password'])
        token = Token()
        user.tokens.append(token)
        db.session.add(user)
        db.session.add(token)
        db.session.commit()
        return user


class AuthenticateUserSchema(Schema):
    email = fields.Email(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)
    key = fields.String(dump_only=True)

    @validates_schema()
    def validate_password(self, data, **kwargs):
        is_password_valid = bool(
            User.query.filter_by(
                email=data['email'],
                password=hash_md5(data['password'])
            ).first()
        )

        if not is_password_valid:
            raise ValidationError('Wrong password!', field_name='password')
