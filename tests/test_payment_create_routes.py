from datetime import datetime, timedelta

from app.models import Payment
from run import app
from . import client


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
    response = client.post(
        "/auth/login",
        json={
            "email": "admin.swish@konf.se",
            "password": "admin",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json