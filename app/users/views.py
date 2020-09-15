from http import HTTPStatus

from flask import Blueprint, request, jsonify
from sqlalchemy import desc

from app.core import auth
from app.users.models import User, Token
from app.users.schemas import UserSchema, AuthenticateUserSchema

users_api = Blueprint('users_api', __name__)


@users_api.route('/', methods=['POST'])
def register():
    data = request.get_json()
    schema = UserSchema(many=False)

    errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    load_data = schema.load(data)
    user_obj = schema.create(load_data)
    token = user_obj.tokens.order_by(desc(Token.created_at)).first()
    return jsonify(AuthenticateUserSchema().dump(token)), HTTPStatus.CREATED


@users_api.route('/', methods=['GET'])
@users_api.route('/<int:user_id>/', methods=['GET'])
@auth.login
def retrieve_users(auth_user, user_id=None):
    if user_id:
        user = User.query.filter_by(id=user_id).first_or_404()
        return jsonify(UserSchema().dump(user)), HTTPStatus.OK

    users = User.query.all()
    return jsonify(UserSchema(many=True).dump(users)), HTTPStatus.OK


@users_api.route('/authenticate/', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    auth_schema = AuthenticateUserSchema()
    validation_errors = auth_schema.validate(data)

    if validation_errors:
        return jsonify(validation_errors), HTTPStatus.UNAUTHORIZED

    user_obj = User.query.filter_by(email=data.get('email')).one()
    token_obj = user_obj.tokens.order_by(desc(Token.created_at)).first()
    return jsonify(auth_schema.dump(token_obj)), HTTPStatus.OK
