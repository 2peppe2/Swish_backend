from flask import Blueprint, jsonify, request, current_app
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

from app.models import Payment
from app.extensions import db, swish_client, csrf
from .validators import StatusPaymentForm
from . import payment_bp
from app.utils import generate_uuid


@payment_bp.route("/<payment_id>", methods=["GET"])
@csrf.exempt
def payment_route(payment_id):
    """Get the payment status from the database."""
    if len(payment_id) != 32:
        return jsonify("Payment ID must be 32 characters long"), 400
    payment = Payment.query.filter_by(id=payment_id).first_or_404()
    return jsonify(payment.to_dict()), 200
