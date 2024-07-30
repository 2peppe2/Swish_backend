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
        headers={"Content-Type": "application/json"}
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


    
