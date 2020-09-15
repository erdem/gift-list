import json

from app.users.models import Token, User


def test_user_registration_view_validations(test_client, guest_user_data_1):
    # when ... attempt to register an user with empty payload
    response = test_client.post(
        '/api/users/',
        data=json.dumps({}),
        content_type='application/json'
    )

    # then ... API endpoint should return 400 along with validation errors
    assert response.status_code == 400
    errors = response.get_json()
    assert len(errors.keys()) == 3

    # when ... attempt to register an user without password
    response = test_client.post(
        '/api/users/',
        data=json.dumps(guest_user_data_1),
        content_type='application/json'
    )

    # then ... API endpoint should return 400 along with password validation error
    errors = response.get_json()
    assert response.status_code == 400
    assert len(errors.keys()) == 1
    assert 'password' in errors
    assert errors['password'] == ['Missing data for required field.']


def test_new_user_registration(test_client, guest_user_data_1):
    # given ... a password for test user
    guest_user_data_1['password'] = '123123'

    # when ... attempt to register an user with a valid payload
    response = test_client.post(
        '/api/users/',
        data=json.dumps(guest_user_data_1),
        content_type='application/json'
    )

    # then ... API endpoint should return 201 along with new user data
    user_data = response.get_json()
    assert response.status_code == 201
    assert user_data['email'] == guest_user_data_1['email']
    token_obj = Token.query.filter_by(user_id=user_data['id']).one()
    assert user_data['token'] == token_obj.key


def test_authorization(test_client, api_test_user, couple_user_1, guest_user_1):
    # when ... attempt to retrieve users list without API token
    response = test_client.get(
        '/api/users/',
        data=json.dumps({}),
        content_type='application/json'
    )

    # then ... API endpoint should return 401
    assert response.status_code == 401

    # given ... a valid API token in request header
    token_key = api_test_user.tokens[0].key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token_key}'
    }

    # when ... attempt to retrieve users list with a valid API token
    response = test_client.get(
        '/api/users/',
        data=json.dumps({}),
        headers=headers,
    )

    # then ... API endpoint should return 200 along with users data
    users_data = response.get_json()
    assert response.status_code == 200
    assert len(users_data) == User.query.count()
