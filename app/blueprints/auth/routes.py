from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import TokenBlocklist, User
from app.extensions import db, jwt
from datetime import datetime

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def create_payment():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@auth.route("/register", methods=["POST"])
@jwt_required()
def register():
    data = request.get_json()

    password = data.get("password")
    email = data.get("email")

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    new_user = User(email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti, created_at=datetime.now()))
    db.session.commit()
    return jsonify({"msg": "Successfully logged out"}), 200


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None
