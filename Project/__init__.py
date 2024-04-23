import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from Project import auth, boeking, home
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()
basedir = os.path.abspath(os.path.dirname(__file__))


def register_extensions(app: Flask):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth_blueprint.login"


def register_blueprints(app: Flask):
    for module_name in ('auth', 'home', 'boeking'):
        module = import_module('Project.{}.pages'.format(module_name))
        app.register_blueprint(module.blueprint)


def register_config(app: Flask):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = "5678909876567890987654567898765"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['WTF_CSRF_ENABLED'] = False
    return app

def configure_database(app: Flask):
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:

        print('> Error: DBMS Exception: ' + str(e))

        # fallback to SQLite
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

        print('> Fallback to SQLite ')
        db.create_all()
    
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app():
    app = Flask(__name__)
    register_config(app)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
