from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from dotenv import load_dotenv
from os import getenv
from app.swish.client import SwishClient
from app.swish.environment import Environment

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

load_dotenv()
_cert_path = getenv('ROOT_PATH') + "certs/"
swish_client =  SwishClient(
    environment= getenv('ENVIRONMENT'),
    merchant_swish_number=getenv('MERCHANT_SWISH_NUMBER'),
    cert=(_cert_path + getenv('PEM_CERT_NAME'), 
          _cert_path + getenv('KEY_CERT_NAME')),
    verify= _cert_path + getenv('SWISH_ROOT_CERT_NAME')
    )