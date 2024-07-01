from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

from app.models import Payment
from app.extensions import db

payment = Blueprint("payment", __name__)
load_dotenv()
allowed_ip = getenv("SWISH_CALLBACK_IP")


@payment.route("/callback", methods=["POST"])
def callback_route():
    # if request.remote_addr != allowed_ip:
    #    return "Forbidden", 403
    callback_data = request.json
    payment = Payment.query.filter_by(id=callback_data["id"]).first_or_404()
    payment.status = callback_data["status"]
    payment.payment_reference = callback_data["paymentReference"]
    print(callback_data["datePaid"])
    print(datetime.strptime(callback_data["datePaid"], "%a, %d %b %Y %H:%M:%S %Z"))
    payment.paid_at = datetime.strptime(
        callback_data["datePaid"], "%a, %d %b %Y %H:%M:%S %Z"
    )
    db.session.commit()

    return "", 200
