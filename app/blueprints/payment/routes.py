import re
from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv

from app.models import Payment
from app.extensions import db, swish_client
from app.swish.exceptions import SwishError
from .validators import CreatePaymentForm


payment = Blueprint("payment", __name__)
load_dotenv()
allowed_ip = getenv("SWISH_CALLBACK_IP")


@payment.route("/create", methods=["POST"])
def create_payment_route():
    form = CreatePaymentForm()
    if not form.validate_on_submit():
        return jsonify(form.errors), 400
    payeePaymentReference = form.payeePaymentReference.data
    payerAlias = form.payerAlias.data
    amount = form.amount.data
    message = form.message.data

    try:
        payment_request = swish_client.create_payment(
            amount,
            "SEK",
            "https://p3trus.se/",
            payeePaymentReference,
            message,
            payerAlias,
        )
    except HTTPError as http_error:
        current_app.logger.error(
            "Swish server response http_code " + str(http_error.response.status_code)
        )
        return http_error.response.text, http_error.response.status_code
    except SwishError as swish_error:
        current_app.logger.error(
            "Request object error "
            + swish_error.error_message
            + " "
            + swish_error.error_code
        )
        return swish_error.error_message, swish_error.error_code
    new_payment = Payment(
        transaction_id=payment_request.id,
        payee_payment_reference=payment_request.payee_payment_reference,
        payment_reference=payment_request.payment_reference,
        payee_alias=payment_request.payee_alias,
        payer_alias=payment_request.payer_alias,
        currency=payment_request.currency,
        message=payment_request.message,
        status=payment_request.status,
        amount=payment_request.amount,
        created_at=payment_request.date_created,
        paid_at=None,
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify(new_payment.to_dict()), 200


@payment.route("/callback", methods=["POST"])
def callback_route():

    return "Callback route", 200
