from flask import Blueprint, jsonify, request, current_app
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

from app.models import Payment
from app.extensions import db, swish_client, csrf
from .validators import CancelPaymentForm
from . import payment_bp
from app.utils.wrapper import require_api_key


@payment_bp.route("/external/<ref>", methods=["GET"])
@csrf.exempt
@require_api_key
def external_route(ref: str):
    """Get payment from the merchant system.
    Adds it to the database and the returns the necessary information to the client."""
    try:
        response = requests.get(f"{getenv('MERCHANT_BASE_URL')}/backend/payment/{ref}",
                     headers={"x-api-key": getenv("MERCHANT_API_KEY")})
    except HTTPError as http_err:
        return jsonify(f"NÄ: {http_err}")
    return jsonify(ref), 200
