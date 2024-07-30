from flask import Blueprint, jsonify, request, current_app
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
    current_app.logger.info(f"Payment status changed: {request.json}")
    callback_data = request.json
    payment = Payment.query.filter_by(id=callback_data["id"]).first_or_404()
    payment.status = callback_data["status"]
    payment.payment_reference = callback_data["paymentReference"]
    payment.paid_at = datetime.strptime(
        callback_data["datePaid"], "%a, %d %b %Y %H:%M:%S %Z"
    )
    db.session.commit()

    return "", 200
