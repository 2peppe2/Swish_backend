from datetime import datetime, timedelta

from app.models import Payment
from run import app
from app.extensions import db
from app.utils import generate_uuid
from . import client, get_version
from datetime import datetime, timedelta



def test_cancel_payment(client, get_version):
    # Create a payment
    create_response = client.post(f"/v{get_version}/backend/payment/create", json={
        "payeePaymentReference": "0123456789", 
        "payerAlias": "46712347689", 
        "amount": 100.00, 
        "message": "payment test"})
    payment_id = create_response.json["id"]

    # Send a cancel request
    response = client.post(f"/v{get_version}/backend/payment/cancel", json={"id": payment_id})

    # Check the response status code
    assert response.status_code == 200

    # Check the payment status
    updated_payment = Payment.query.filter_by(id=payment_id).first()
    assert updated_payment.status == "CANCELLED"

def test_cancel_nonexistent_payment(client, get_version):
    # Send a cancel request for a non-existent payment
    uuid = generate_uuid()
    response = client.post(f"/v{get_version}/backend/payment/cancel", json={"id": uuid})
    # Check the response status code
    assert response.status_code == 404
    

def test_cancel_already_cancelled_payment(client, get_version):
    # Create a payment
    create_response = client.post(f"/v{get_version}/backend/payment/create", json={
        "payeePaymentReference": "0123456789", 
        "payerAlias": "46712347689", 
        "amount": 100.00, 
        "message": "payment test"})
    payment_id = create_response.json["id"]
    # Cancel the payment
    client.post(f"/v{get_version}/backend/payment/cancel", json={"id": payment_id})
    # Send another cancel request for the same payment
    response = client.post(f"/v{get_version}/backend/payment/cancel", json={"id": payment_id})
    # Check the response status code
    assert response.status_code == 422

def test_cancel_bad_payment_id(client, get_version):
    # Send a cancel request with a bad payment ID
    response = client.post(f"/v{get_version}/backend/payment/cancel", json={"id": "bad_id"})
    # Check the response status code
    assert response.status_code == 400
