from flask import Flask
from config import config
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from .extensions import db, jwt, bcrypt



from typing import Dict

from .blueprints.payment import payment as payment_blueprint
from .blueprints.auth import auth as auth_blueprint


def register_blueprints(app: Flask):
    app.register_blueprint(payment_blueprint, url_prefix="/payment")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    

def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    configure_logging(app)
    
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()
        create_admin_acount()
        
    register_blueprints(app)
    return app


def create_admin_acount():
    from .models import User
    load_dotenv()
    admin_email = os.getenv('ADMIN_EMAIL', "admin.swish@konf.se")
    admin_password = generate_password_hash(os.getenv('ADMIN_PASSWORD', "admin"))

    if User.query.filter_by(email=admin_email).first():
        return
    admin_user = User(email=admin_email, password=admin_password)
    db.session.add(admin_user)
    db.session.commit()

def configure_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = TimedRotatingFileHandler('logs/flask_app.log', when='midnight', backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('App startup')