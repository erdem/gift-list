import hashlib
import uuid


def hash_md5(value):
    return hashlib.md5(value.encode()).hexdigest()


def generate_token():
    return uuid.uuid4().hex
