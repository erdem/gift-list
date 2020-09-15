from http import HTTPStatus

from flask import Blueprint, request, jsonify

from app.users.models import User
from app.users.schemas import UserSchema, AuthenticateUserSchema

users_api = Blueprint('users_api', __name__)


@users_api.route('/', methods=["POST"])
def register():
    data = request.get_json()
    schema = UserSchema(many=False)

    errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    load_data = schema.load(data)
    user_obj = schema.create(load_data)
    return jsonify(schema.dump(user_obj)), HTTPStatus.CREATED


@users_api.route('/', methods=["GET"])
@users_api.route('/<int:user_id>/', methods=["GET"])
def retrieve_users(user_id=None):
    if user_id:
        user = User.query.filter_by(id=user_id).first_or_404()
        return jsonify(UserSchema().dump(user)), HTTPStatus.OK

    users = User.query.all()
    return jsonify(UserSchema(many=True).dump(users)), HTTPStatus.OK


@users_api.route('/authenticate/', methods=["POST"])
def authenticate_user():
    data = request.get_json()
    auth_schema = AuthenticateUserSchema()
    validation_errors = auth_schema.validate(data)

    if validation_errors:
        return jsonify(validation_errors), HTTPStatus.UNAUTHORIZED

    user = User.query.filter_by(email=data.get('email')).one()
    return jsonify(UserSchema().dump(user)), HTTPStatus.OK
