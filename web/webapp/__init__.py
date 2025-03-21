from glob import glob
from flask import Flask
from flask_jwt_extended import JWTManager
from importlib import import_module
from flask_login import LoginManager

login_manager = LoginManager()


def register_blueprints(app):
    for module_name in glob("webapp/blueprints/*/"):
        module = import_module(module_name.replace('/', '.') + 'routes')
        app.register_blueprint(module.blueprint)


def register_extensions(app):
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    JWTManager(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object('webapp.config.Config')

    register_blueprints(app)
    register_extensions(app)

    with app.app_context():
        # Imports
        from . import routes

        return app
