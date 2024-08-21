from datetime import datetime, timedelta

from app.models import Payment
from run import app
from app.extensions import db
from app.utils import generate_uuid
from . import client, get_version






""" def test_payment_callback_route(client, get_version):
    Test the callback route.
    uuid = generate_uuid()
    payment = Payment(
        id=uuid,
        payee_payment_reference="0123456789",
        payment_reference="652ED6A2BCDE4BA8AD11D7334E9567B7",
        payer_alias="46712347689",
        payee_alias="1234679304",
        amount=100.00,
        currency="SEK",
        message="payment test",
        status="CREATED",
        created_at=datetime.now() - timedelta(seconds=5),
        paid_at=None,
        redirect_callback_url="https://example.com/callback",
    )
    with app.app_context():
        db.session.add(payment)
        db.session.commit()

    response = client.post(
        f"/v{get_version}/backend/payment/callback",
        json={
            "id": uuid,
            "payeePaymentReference": "0123456789",
            "paymentReference": "652ED6A2BCDE4BA8AD11D7334E9567B7",
            "callbackUrl": "https://example.com/api/swishcb/paymentrequests",
            "payerAlias": "46712347689",
            "payeeAlias": "1234679304",
            "amount": 100.00,
            "currency": "SEK",
            "message": "payment test",
            "status": "PAID",
            "dateCreated": datetime.now() - timedelta(seconds=5),
            "datePaid": datetime.now(),
            "errorCode": None,
            "errorMessage": None,
        },
    )
    assert response.status_code == 200 """
 #REMOVE

