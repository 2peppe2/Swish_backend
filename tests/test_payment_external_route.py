from . import client, get_version, teardown_database


def test_payment_external(client, get_version):
    response = client.get(
        f"/v{get_version}/backend/payment/external/123456789",
        headers={"x-api-key": "api-key"},
    )
    assert response.status_code == 200


def test_payment_external_not_found(client, get_version):
    response = client.get(
        f"/v{get_version}/backend/payment/external/404",
        headers={"x-api-key": "api-key"},
    )
    assert response.status_code == 404


def test_payment_external_unauthorized(client, get_version):
    response = client.get(
        f"/v{get_version}/backend/payment/external/123456789",
    )
    assert response.status_code == 401
