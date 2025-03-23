from flask import Blueprint, jsonify, request, current_app
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

from app.models import Payment
from app.extensions import db
from . import payment_bp

load_dotenv()
allowed_ip = getenv("ALLOWED_SWISH_CALLBACK_IP")


@payment_bp.route("/callback", methods=["POST", "GET", "PUT", "DELETE", "PATCH"])
def callback_route():
    # if request.remote_addr != allowed_ip:
    #    return "Forbidden", 403
    current_app.logger.info(f"Incoming callback for payment: {request.json}")
    callback_data = request.json
    
    payment = Payment.query.filter_by(id=callback_data["id"]).first_or_404()
    payment.status = callback_data["status"]
    if callback_data["status"] == "PAID":
        current_app.logger.error(f"CAME HERE! TEMP")
        payment.payment_reference = callback_data["paymentReference"]
        payment.paid_at = datetime.strptime(
            callback_data["datePaid"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        current_app.logger.info(f"Payment paid: {payment.to_dict()}")
    if callback_data["status"] != "PAID":
        current_app.logger.error(f"Payment failed: {payment.to_dict()}")
    db.session.commit()
    current_app.logger.info(f"Payment updated: {payment.to_dict()}")

    return "", 200
    #TODO: THIS SHOULD USED WHEN MERCHANT IS UP
    response = requests.put(
        getenv("MERCHANT_BASE_URL")
        + f"/backend/payment/ref/{payment.payee_payment_reference}",
        json=payment.to_dict(),
        headers={"x-api-key": getenv("MERCHANT_API_KEY")},
    )
    if response.status_code != 200:
        #TODO: This should be a retry mechanism
        current_app.logger.error(
            f"Failed to update payment in merchant system: {response.content}"
        )
        return response.content, response.status_code
    return "", 200
