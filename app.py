from flask import Flask
from dotenv import dotenv_values
from waitress import serve
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # type: ignore
from typing import cast, Dict

from database.base import db
from database.models.token_blocklist import TokenBlocklist

from router.router import Router
from router.routes.temp import route_temp

env = dotenv_values()

def configure_jwt(app: Flask):
    app.config["JWT_SECRET_KEY"] = env.get("JWT_SECRET_KEY")

def configure_dev(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

def serve_dev(app: Flask):
    app.run(debug=True)
    
def configure_prod(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql+psycopg2://{env.get("DB")}'
    app.config["SQLALCHEMY_ECHO"] = True

def serve_prod(app: Flask):
    serve(app, host="0.0.0.0", port=8080)

def configure_environment(name: str):
    configs = {
        "prod": {
            "configure": configure_prod,
            "serve": serve_prod
        },
        "dev": {
            "configure": configure_dev,
            "serve": serve_dev
        },
        # Add more environments as needed
    }
    config = configs.get(name)
    if config:
        config["configure"](app)
        return config["serve"]
    else:
        return None
    
def setup_routes(app: Flask, bcrypt: Bcrypt):
    router = Router(app, db)
    router.register_route(route_temp)
    
def check_if_token_revoked(_, jwt_payload: Dict[str, str]) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

def setup_db(db: SQLAlchemy):
    db.init_app(app)

    with app.app_context():
        db.create_all()
        #init_halls()

if __name__ == "__main__":
    app = Flask(__name__)
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    serve_function = configure_environment(
            cast(str, env.get("ENVIRONMENT", "dev"))
        )
    setup_db(db)
    configure_jwt(app)
    setup_routes(app, bcrypt)
    jwt.token_in_blocklist_loader(check_if_token_revoked) # type: ignore
    if serve_function is not None:
        serve_function(app)
