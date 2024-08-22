from . import client, get_version, teardown_database, merchant_mock_client


def test_payment_external(merchant_mock_client):
    response = merchant_mock_client.get(
        "/backend/payment/123456789",
        headers={"x-api-key": "api-key"},
    )
    assert response.status_code == 200


def test_payment_external_not_found(merchant_mock_client):
    response = merchant_mock_client.get(
        "/backend/payment/404",
        headers={"x-api-key": "api-key"},
    )
    assert response.status_code == 404


def test_payment_external_unauthorized(merchant_mock_client):
    response = merchant_mock_client.get(
        "/backend/payment/123456789",
    )
    assert response.status_code == 401
