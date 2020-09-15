from http import HTTPStatus

from flask import abort, request

from app.users.models import Token


def login(view):
    def authenticate(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(HTTPStatus.UNAUTHORIZED)
        header_auth_data = request.headers.get('Authorization', '')
        token_key = header_auth_data.replace('Bearer ', '')
        token_obj = Token.query.filter_by(key=token_key).one()
        if not token_obj:
            abort(HTTPStatus.UNAUTHORIZED)
        return view(auth_user=token_obj.user, *args, **kwargs)
    return authenticate
