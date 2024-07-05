from datetime import datetime, timedelta
import pytest

from app.models import Payment
from run import app
from app.extensions import db
from app.utils import generate_uuid


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        yield client


def test_payment_create_route_success(client):
    response = client.post(
        "/payment/create",
        json={
            "payeePaymentReference": "Id4",
            "payerAlias": "123456780",
            "amount": 100,
            "message": "Test",
        },
    )
    assert response.status_code == 201
def test_payment_create_route_missing_fields(client):
    response = client.post(
        "/payment/create",
        json={
            "payeePaymentReference": "Id4",
            "payerAlias": "123456780",
            # Missing "amount" and "message" fields
        },
    )
    assert response.status_code == 400
def test_payment_create_route_invalid_fields(client):
    response = client.post(
        "/payment/create",
        json={
            "payeePaymentReference": "Id4",
            "payerAlias": "123456780",
            "amount": "invalid",  # Invalid amount value
            "message": "Test",
        },
    )
    assert response.status_code == 400
def test_payment_create_route_no_message(client):
    response = client.post(
        "/payment/create",
        json={
            "payeePaymentReference": "Id4",
            "payerAlias": "123456780",
            "amount": 100,
            "message": None,  # Missing message field
        },
    )
    assert response.status_code == 400



def test_payment_callback_route(client):
    """Test the callback route."""
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
    )
    with app.app_context():
        db.session.add(payment)
        db.session.commit()

    response = client.post(
        "/payment/callback",
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
    assert response.status_code == 200


def test_login_route(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "admin.swish@konf.se",
            "password": "admin",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json
