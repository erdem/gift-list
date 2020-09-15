import pytest

from app.users.models import User, Token


@pytest.fixture()
def guest_user_data_1():
    return {
        'first_name': 'Guido',
        'last_name': 'van Rossum',
        'email': 'guido@mail.com',
    }


@pytest.fixture()
def guest_user_data_2():
    return {
        'first_name': 'Jessica',
        'last_name': 'Jay',
        'email': 'jess@mail.com',
    }


@pytest.fixture()
def couple_user_data_1():
    return {
        'first_name': 'John',
        'last_name': 'Chris',
        'email': 'john@mail.com',
    }


@pytest.fixture()
def guest_user_1(guest_user_data_1, session):
    guest_user = User(**guest_user_data_1)
    guest_user.set_password('123123')
    token = Token()
    guest_user.tokens.append(token)
    session.add(guest_user)
    session.commit()


@pytest.fixture()
def guest_user_2(guest_user_data_2, session):
    guest_user = User(**guest_user_data_2)
    guest_user.set_password('123123')
    session.add(guest_user)
    session.commit()


@pytest.fixture()
def couple_user_1(couple_user_data_1, session):
    couple_user = User(**couple_user_data_1)
    couple_user.set_password('123123')
    token = Token()
    couple_user.tokens.append(token)
    session.add(couple_user)
    session.commit()
