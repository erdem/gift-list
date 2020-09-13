import hashlib
from uuid import UUID

from app.users.utils import generate_token, hash_md5


def test_generate_token():
    token = generate_token()
    try:
        UUID(token, version=4)
        token_is_valid = True
    except ValueError:
        token_is_valid = False
    assert token_is_valid is True


def test_hash_md5():
    password = 'secret_password'
    assert hash_md5(password) == hashlib.md5(password.encode()).hexdigest()
