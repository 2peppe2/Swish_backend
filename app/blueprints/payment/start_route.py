import threading
import time
from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import HTTPError


from app.models import Payment
from app.extensions import db, swish_client, csrf
from .validators import StartPaymentForm
from . import payment_bp

def cancel_payment_after_delay(payment_id, delay):
    time.sleep(delay)
    db_payment = Payment.query.filter_by(id=payment_id).first()
    if db_payment.status == "PROCESSING":
        db_payment.status = "CANCELLED"
        db.session.commit()
        swish_client.cancel_payment(payment_id)
        current_app.logger.info(f"Payment {payment_id} cancelled after {delay} seconds")


@payment_bp.route("/start", methods=["PUT"])
@csrf.exempt
def start_payment_route():
    """ """
    # Validation
    form = StartPaymentForm()
    if not form.validate_on_submit():
        return jsonify(form.errors), 400
    
    id = form.id.data
    payerAlias = form.phoneNumber.data

    db_payment = Payment.query.filter_by(id=id).first_or_404()
    if (db_payment.status != "CREATED"):
        if (db_payment.status != "PAID"):
            return jsonify({"error": "Payment already exists"}), 400
        return jsonify({"error": "Payment already processed"}), 200
    
    db_payment.payer_alias = payerAlias
    db.session.commit()

    try:
        # Create a payment request using the Swish client
        payment_request = swish_client.create_payment(
            id=id,
            amount=db_payment.amount,
            currency=db_payment.currency,
            callback_url="https://swish.p3trus.se/v1.0/backend/payment/callback",  # TODO fix this
            payee_payment_reference=db_payment.payee_payment_reference,
            message=db_payment.message,
            payer_alias=payerAlias,
        )
        db_payment.status = "PROCESSING"
        db.session.commit()

        t = threading.Thread(target=cancel_payment_after_delay, args=(db_payment.id, 300))
        t.start()

    except HTTPError as http_error:
        # Log the Swish server response error
        current_app.logger.error(
            f"Swish server response http_code {str(http_error.response.status_code)}, {str(http_error.response.content)}"
        )
        return http_error.response.text, http_error.response.status_code

    # Log the created payment request details
    current_app.logger.info(
        f"Payment request created {payment_request.id}, {payment_request.payee_payment_reference}, {payment_request.amount} {payment_request.currency}"
    )
    return "", 201
