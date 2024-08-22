from datetime import datetime, timedelta

from app.models import Payment
from run import app
from . import client, get_version, teardown_database
from app.extensions import db
from app.utils import generate_uuid


def add_payment_to_database(uuid, message="payment test"):
    payment = Payment(
        id=uuid,
        payee_payment_reference="0123456789",
        payment_reference=None,
        payer_alias=None,
        payee_alias="1234679304",
        amount=100,
        currency="SEK",
        message=message,
        status="PROCESSING",
        created_at=datetime.now() - timedelta(seconds=5),
        paid_at=None,
        redirect_callback_url="https://example.com/callback",
    )
    with app.app_context():
        db.session.add(payment)
        db.session.commit()


def test_payment_start_success(client, get_version):
    uuid = generate_uuid()
    add_payment_to_database(uuid)

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": uuid, "phoneNumber": "1234567890"},
    )
    assert response.status_code == 201


def test_payment_start_invalid_id(client, get_version):
    uuid = generate_uuid()
    add_payment_to_database(uuid)

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": "invalid-uuid", "phoneNumber": "1234567890"},
    )
    assert response.status_code == 400


def test_payment_start_missing_phone_number(client, get_version):
    uuid = generate_uuid()
    add_payment_to_database(uuid)

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": uuid},
    )
    assert response.status_code == 400


def test_payment_start_invalid_phone_number(client, get_version):
    uuid = generate_uuid()
    add_payment_to_database(uuid)

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": uuid, "phoneNumber": "invalid-phone-number"},
    )
    assert response.status_code == 400


def test_payment_start_nonexistent_payment(client, get_version):
    uuid = generate_uuid()
    add_payment_to_database(uuid)
    other_uuid = generate_uuid()

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": other_uuid, "phoneNumber": "1234567890"},
    )
    assert response.status_code == 404


def test_payment_start_already_processing_payment(client, get_version):
    uuid = generate_uuid()
    add_payment_to_database(uuid)

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": uuid, "phoneNumber": "1234567890"},
    )
    assert response.status_code == 201

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": uuid, "phoneNumber": "1234567890"},
    )
    assert response.status_code == 422


def test_payment_start_invalid_api_key(client, get_version):
    uuid = generate_uuid()
    add_payment_to_database(uuid)

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "invalid-api-key", "Content-Type": "application/json"},
        json={"id": uuid, "phoneNumber": "1234567890"},
    )
    assert response.status_code == 401


def test_payment_start_error_message(client, get_version):
    uuid = generate_uuid()
    add_payment_to_database(uuid, message="FF08")

    response = client.put(
        f"/v{get_version}/backend/payment/start",
        headers={"x-api-key": "api-key", "Content-Type": "application/json"},
        json={"id": uuid, "phoneNumber": "1234567890"},
    )
    assert response.status_code == 422
