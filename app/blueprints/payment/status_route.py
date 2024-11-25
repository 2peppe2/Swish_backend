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


@payment_bp.route("/status/", methods=["POST"])
@csrf.exempt
def status_route():
    """Get the payment status from the database."""
    # Validate the form data
    form = StatusPaymentForm()
    if not form.validate_on_submit():
        return jsonify(form.errors), 400
    id = form.id.data
    payment = Payment.query.filter_by(id=id).first_or_404()
    return jsonify(payment.status), 200
