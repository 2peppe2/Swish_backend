from datetime import datetime, timedelta

from app.models import Payment
from run import app
from . import client, get_version


def test_payment_create_route_success(client, get_version):
    response = client.post(
        f"/v{get_version}/backend/payment/create",
        json={
            "payeePaymentReference": "Id4",
            "payerAlias": "123456780",
            "amount": 100,
            "message": "Test",
            "redirectCallbackUrl": "https://example.se/callback",
        },
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201


def test_payment_create_route_missing_fields(client, get_version):
    response = client.post(
        f"/v{get_version}/backend/payment/create",
        json={
            "payeePaymentReference": "Id4",
            "payerAlias": "123456780",
            # Missing "amount" and "message" fields
        },
    )
    assert response.status_code == 400


def test_payment_create_route_invalid_fields(client, get_version):
    response = client.post(
        f"/v{get_version}/backend/payment/create",
        json={
            "payeePaymentReference": "Id4",
            "payerAlias": "123456780",
            "amount": "invalid",  # Invalid amount value
            "message": "Test",
        },
    )
    assert response.status_code == 400
