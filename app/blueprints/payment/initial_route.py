from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

from app.models import Payment
from app.extensions import db, swish_client, csrf
from .validators import CancelPaymentForm
from . import payment_bp 


@payment_bp.route("/initial/<id>", methods=["GET"])
@csrf.exempt
def initial_route(id):
    return jsonify(id), 200


