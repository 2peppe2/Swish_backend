from flask import Blueprint, jsonify, request, current_app
from uuid import uuid4 as uuid
from app.models import Payment
from app.extensions import db, swish_client
from requests.exceptions import HTTPError
from app.swish.exceptions import SwishError


payment = Blueprint("payment", __name__)



@payment.route('/create', methods=['POST'])
def create_payment_route():
    data = request.get_json()
    payeePaymentReference = data.get('payeePaymentReference')
    payerAlias = data.get('payerAlias')
    amount = data.get('amount')
    message = data.get('message')
    try:
        payment_request = swish_client.create_payment(amount, 'SEK', 'https://p3trus.se/', payeePaymentReference, message, payerAlias)
    except HTTPError as http_error:
        current_app.logger.error("Swish server response http_code " + str(http_error.response.status_code))
        return http_error.response.text, http_error.response.status_code
    except SwishError as swish_error:
        current_app.logger.error("Request object error " + swish_error.error_message + " " + swish_error.error_code)
        return swish_error.error_message, swish_error.error_code


    new_payment = Payment(id= payment_request.id, 
                        payee_payment_reference= payment_request.payee_payment_reference,
                        payment_reference= payment_request.payment_reference,
                        payee_alias= payment_request.payee_alias,
                        payer_alias= payment_request.payer_alias,
                        currency= payment_request.currency,
                        message= payment_request.message,
                        status= payment_request.status,
                        amount= payment_request.amount,
                        created_at= payment_request.date_created)
    db.session.add(new_payment)
    db.session.commit()
    return "Payment created"
