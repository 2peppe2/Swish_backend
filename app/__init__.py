from flask import Flask, Blueprint
from config import config
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime
from flask_wtf.csrf import CSRFError

from .extensions import db, jwt, bcrypt, csrf


from typing import Dict

from .blueprints.payment import payment_bp as payment_blueprint
from .blueprints.auth import auth as auth_blueprint


def register_blueprints(app: Flask):
    main_bp = Blueprint("main", __name__)
    main_bp.register_blueprint(payment_blueprint, url_prefix="/payment")
    csrf.exempt(payment_blueprint)
    main_bp.register_blueprint(auth_blueprint, url_prefix="/auth")
    version = os.getenv("VERSION")
    app.register_blueprint(main_bp, url_prefix=f"/v{version}/backend")


def create_app(config_name: str):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    configure_logging(app)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
        create_admin_acount()
        create_temp_payment()
    register_error_handlers(app)
    register_blueprints(app)
    return app


def create_admin_acount():
    from .models import User

    admin_email = os.getenv("ADMIN_EMAIL", "admin.swish@konf.se")
    admin_password = generate_password_hash(os.getenv("ADMIN_PASSWORD", "admin"))

    if User.query.filter_by(email=admin_email).first():
        return
    admin_user = User(email=admin_email, password=admin_password)
    db.session.add(admin_user)
    db.session.commit()

def create_temp_payment():
    from .models import Payment
    load_dotenv()
    from app.utils import generate_uuid
    payment = Payment(
        id= generate_uuid(),
        payee_payment_reference="test_Ref",
        payment_reference=None,
        payer_alias=os.getenv("MERCHANT_SWISH_NUMBER", "1234567890"),
        payee_alias="123456789",
        amount=100,
        currency="SEK",
        message="test",
        status="Initiated",
        created_at=datetime.now(),
        paid_at=None,
        redirect_callback_url="https://example.com/callback"
    )
    db.session.add(payment)
    db.session.commit()


def configure_logging(app):
    
    # Get the current date
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")

    if not os.path.exists("logs"):
        os.mkdir("logs")
    
    # Define the log directory and file name
    log_dir = os.path.join("logs", year, month)
    log_file = os.path.join(log_dir, "app.log")
    os.makedirs(log_dir, exist_ok=True)
    
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("App startup")

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error('Unhandled Exception: %s', (error))
        return 'error', error.code
    

