from flask import Flask

from app.database import init_db
from app.lists.views import lists_api
from app.products.views import products_api
from app.users.views import users_api


def create_app(settings_module=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """

    if settings_module is None:
        settings_module = 'app.settings'

    app = Flask(__name__, **kwargs)

    try:
        app.config.from_object(settings_module)
    except ImportError:
        raise ImportError(f'The app settings file cannot import from {settings_module}')

    app.register_blueprint(users_api, url_prefix='/api/users/')
    app.register_blueprint(products_api, url_prefix='/api/products/')
    app.register_blueprint(lists_api, url_prefix='/api/lists/')

    init_db(app)
    return app
