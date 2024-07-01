from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

from app.models import Payment
from app.extensions import db, swish_client
from .validators import CancelPaymentForm

payment = Blueprint("payment", __name__)


@payment.route("/cancel", methods=["POST"])
def callback_route():
    form = CancelPaymentForm()
    if not form.validate_on_submit():
        return jsonify(form.errors), 400
    id = form.id.data
    payment = Payment.query.filter_by(id=id).first_or_404()
    canceled_payment = swish_client.cancel_payment(id)
    payment.status = canceled_payment.status
    db.session.commit()
    return "", 200
