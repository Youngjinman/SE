from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
import logging

import pymysql
pymysql.install_as_MySQLdb()

from . import templates

import config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, resources={r"/*":{"origins": "*"}}, supports_credentials=True)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from . import models
    
    from .views import auth_views, find_views, main_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(find_views.bp)

    return app