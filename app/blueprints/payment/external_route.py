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
from app.utils import generate_uuid


@payment_bp.route("/external/<ref>", methods=["GET"])
@csrf.exempt
def external_route(ref: str):
    """Get payment from the merchant system.
    Adds it to the database and the returns the necessary information to the client."""
    try:
        existing_payment = Payment.query.filter_by(payee_payment_reference=ref)
        if existing_payment.first():
            # Return the existing payment
            return (
                jsonify(
                    {
                        "id": existing_payment.first().id,
                        "phoneNumber": existing_payment.first().payer_alias,
                        "amount": existing_payment.first().amount,
                        "redirectCallback": existing_payment.first().redirect_callback_url,
                        "status": existing_payment.first().status,
                    }
                ),
                200,
            )
        id = generate_uuid()
        
        if(Payment.query.filter_by(payee_payment_reference=ref).first()):
            return jsonify({"error": "Payment already exists"}), 400
        
        #Here is should fetch the payment from the merchant system
        new_payment = Payment(
            id=str(id),
            payee_payment_reference=str(ref),
            payment_reference=None,
            payee_alias=str(getenv("MERCHANT_SWISH_NUMBER")),
            payer_alias="0705472993",
            currency=str(getenv("CURRENCY")),
            message=str("1"),
            status=str("CREATED"),
            amount=float(200),
            created_at=datetime.now(),
            paid_at=None,
            redirect_callback_url=str("https://www.example.com"),
        )
        db.session.add(new_payment)
        db.session.commit()
        return (
            jsonify(
                {
                    "id": id,
                    "phoneNumber": "",
                    "amount": new_payment.amount,
                    "redirectCallback": new_payment.redirect_callback_url,
                    "status": new_payment.status,
                }
            ),
            200,
        )
        """
        response = requests.get(
            f"{getenv('MERCHANT_BASE_URL')}/backend/payment/{ref}",
            headers={"x-api-key": getenv("MERCHANT_API_KEY")},
        )
        response.raise_for_status()

        response_data = response.json()
        id = generate_uuid()

        new_payment = Payment(
            id=str(id),
            payee_payment_reference=str(ref),
            payment_reference=None,
            payee_alias=str(getenv("MERCHANT_SWISH_NUMBER")),
            payer_alias=None,
            currency=str(getenv("CURRENCY")),
            message=str(response_data["message"]),
            status=str("CREATED"),
            amount=float(response_data["amount"]),
            created_at=datetime.now(),
            paid_at=None,
            redirect_callback_url=str(response_data["redirect_callback_url"]),
        )

        db.session.add(new_payment)
        db.session.commit()
        return jsonify({"id": id, "phoneNumber": response_data["payer_alias"], "amount": response_data["amount"]}), 200
        """

    except HTTPError as http_error:
        current_app.logger.error(
            f"Swish server response http_code {str(http_error.response.status_code)}, ref: {ref} tried fetching data"
        )
        return (
            jsonify(http_error.response.content.decode()),
            http_error.response.status_code,
        )
    except Exception as e:
        current_app.logger.error(
            f"An error occurred when trying to fetch payment with ref: {ref}, error: {str(e)}"
        )
        return jsonify({"error": "An error occurred"}), 500
