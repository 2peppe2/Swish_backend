from datetime import datetime, timedelta

from app.models import Payment
from run import app
from app.extensions import db
from app.utils import generate_uuid
from . import client, get_version, teardown_database, add_payment_to_database 


def start_payment_flow(client, get_version, uuid):
    add_payment_to_database(uuid)

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": uuid, "phoneNumber": "1234567890"},
    )
    assert response.status_code == 201

def test_cancel_payment(client, get_version):
    uuid = generate_uuid()
    start_payment_flow(client, get_version, uuid)

    response = client.post(f"/v{get_version}/backend/payment/cancel", json={"id": uuid})

    # Check the response status code
    assert response.status_code == 200

    # Check the payment status
    updated_payment = Payment.query.filter_by(id=uuid).first()
    assert updated_payment.status == "CANCELLED"



def test_cancel_nonexistent_payment(client, get_version):
    # Send a cancel request for a non-existent payment
    uuid = generate_uuid()
    response = client.post(f"/v{get_version}/backend/payment/cancel", json={"id": uuid})
    # Check the response status code
    assert response.status_code == 404
    

def test_cancel_already_cancelled_payment(client, get_version):
    uuid = generate_uuid()
    start_payment_flow(client, get_version, uuid)

    # Cancel the payment
    client.post(f"/v{get_version}/backend/payment/cancel", json={"id": uuid})

    # Send another cancel request for the same payment
    response = client.post(f"/v{get_version}/backend/payment/cancel", json={"id": uuid})

    # Check the response status code
    assert response.status_code == 422

def test_cancel_bad_payment_id(client, get_version):
    # Send a cancel request with a bad payment ID
    response = client.post(f"/v{get_version}/backend/payment/cancel", json={"id": "bad_id"})
    # Check the response status code
    assert response.status_code == 400
