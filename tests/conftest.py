import pytest

from app import create_app
from app.database import db as db_instance
from app.users.models import User, Token


@pytest.yield_fixture(scope='session')
def app():
    application = create_app()

    with application.app_context():
        yield application


@pytest.fixture
def app_context(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def test_client(app):
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    with app.app_context():
        db_instance.drop_all()
        db_instance.create_all()
        yield db_instance


@pytest.yield_fixture(scope="class", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = db_instance.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = db_instance.create_scoped_session(options=options)

        db_instance.session = sess
        yield sess

        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()


@pytest.fixture
def api_test_user(db, session):
    api_user = User(
        first_name='restful',
        last_name='api',
        email='api@restful.com'
    )
    api_user.set_password('123123')
    token = Token()
    api_user.tokens.append(token)
    db.session.add(api_user)
    db.session.add(token)
    db.session.commit()
    return api_user
