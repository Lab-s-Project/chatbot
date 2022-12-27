import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from urllib.parse import quote

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from dotenv import load_dotenv

load_dotenv()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy(session_options={'autocommit': True})
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    _username = os.environ.get('DB_USERNAME')
    _password = os.environ.get('DB_PASSWORD')
    _port = os.environ.get('DB_PORT')
    _db_name = os.environ.get('DB_NAME')
    _host = os.environ.get('DB_HOST')

    app.secret_key = 'asdfghjklqwertyuzxcvbnm.qwertyu'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{_username}:%s@{_host}:{_port}/{_db_name}' % quote(
            _password)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_POOL_SIZE'] = 1
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

    login_manager.init_app(app)
    db.init_app(app)
    
    print("Database connected")
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app