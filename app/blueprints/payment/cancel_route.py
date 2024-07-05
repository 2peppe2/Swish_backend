from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

from app.models import Payment
from app.extensions import db, swish_client
from .validators import CancelPaymentForm
from . import payment_bp


@payment_bp.route("/cancel", methods=["POST"])
def cancel_route():
    form = CancelPaymentForm()
    if not form.validate_on_submit():
        return jsonify(form.errors), 400
    id = form.id.data
    payment = Payment.query.filter_by(id=id).first_or_404()
    try:
        canceled_payment = swish_client.cancel_payment(id)
    except HTTPError as http_error:
        current_app.logger.error(f"Error canceling payment: {http_error}")
        return http_error.response.text, http_error.response.status_code
    payment.status = canceled_payment.status
    db.session.commit()
    return "", 200