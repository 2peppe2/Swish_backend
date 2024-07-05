from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import HTTPError


from app.models import Payment
from app.extensions import db, swish_client
from .validators import CreatePaymentForm
from . import payment_bp


@payment_bp.route("/create", methods=["POST"])
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
    
    current_app.logger.info(
        f"Payment request created {payment_request.id}, {payment_request.payee_payment_reference}, {payment_request.amount} {payment_request.currency}"
    )
    new_payment = Payment(
        id=str(payment_request.id),
        payee_payment_reference=str(payment_request.payee_payment_reference),
        payment_reference=None,
        payee_alias=str(payment_request.payee_alias),
        payer_alias=str(payment_request.payer_alias),
        currency=str(payment_request.currency),
        message=str(payment_request.message),
        status=str(payment_request.status),
        amount=float(payment_request.amount),
        created_at=payment_request.date_created,
        paid_at=None,
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify(new_payment.to_dict()), 201
