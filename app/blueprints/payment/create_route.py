from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import HTTPError


from app.models import Payment
from app.extensions import db, swish_client, csrf
from .validators import CreatePaymentForm
from . import payment_bp


@payment_bp.route("/create", methods=["POST"])
@csrf.exempt
def create_payment_route():
    """
    Create a payment route.

    This function handles the creation of a payment route by validating the form data,
    creating a payment request using the Swish client, and storing the payment details
    in the database.

    Returns:
        A JSON response containing the payment details if successful, or the form errors
        and HTTP status code 400 if the form validation fails.
    """
    # Validate the form data
    form = CreatePaymentForm()
    if not form.validate_on_submit():
        return jsonify(form.errors), 400

    # Extract form data
    payeePaymentReference = form.payeePaymentReference.data
    payerAlias = form.payerAlias.data
    amount = form.amount.data
    message = form.message.data
    redirect_callback_url = form.redirectCallbackUrl.data

    try:
        # Create a payment request using the Swish client
        payment_request = swish_client.create_payment(
            amount,
            "SEK",
            "https://swish.p3trus.se/payment/callback",
            payeePaymentReference,
            message,
            payerAlias,
        )
    except HTTPError as http_error:
        # Log the Swish server response error
        current_app.logger.error(
            "Swish server response http_code " + str(http_error.response.status_code)
        )
        return http_error.response.text, http_error.response.status_code

    # Log the created payment request details
    current_app.logger.info(
        f"Payment request created {payment_request.id}, {payment_request.payee_payment_reference}, {payment_request.amount} {payment_request.currency}"
    )

    # Create a new payment object and store it in the database
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
        redirect_callback_url=str(redirect_callback_url),
    )
    db.session.add(new_payment)
    db.session.commit()
    return "", 201