import pytest
import requests
from app.swish import client, environment
import time


def test_temp_endpoint():
    response = requests.get("http://127.0.0.1:5000/temp")
    assert response.status_code == 200
    assert response.json() == {"message": "Temp endpoint"}


def test_swish():
    swish_client = client.SwishClient(
        environment=environment.Environment.Test,
        merchant_swish_number="1234679304",
        cert=(
            "./certs/Swish_Merchant_TestCertificate_1234679304.pem",
            "./certs/Swish_Merchant_TestCertificate_1234679304.key",
        ),
        verify="./certs/Swish_TLS_RootCA.pem",
    )
    response = swish_client.create_payment(
        100, "SEK", "https://p3trus.se/", "Id2", "Test", "123456780"
    )
    response2 = swish_client.get_payment(response.id)
    print(response2.status)


def test_create_payment():
    response = requests.post(
        "http://127.0.0.1:5000/payment/create",
        json={
            "payeePaymentReference": "Id3",
            "payerAlias": "123456780",
            "amount": 100,
            "message": "Test",
        },
    )
    print(response)
    print(response.json())


def auth_test():
    response = requests.post(
        "http://127.0.0.1:5000/auth/login",
        json={"email": "admin.swish@konf.se", "password": "admin"},
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    assert access_token is not None
    response = requests.delete(
        "http://127.0.0.1:5000/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print(response)
    assert response.status_code == 200


if __name__ == "__main__":
    pass
    # test_temp_endpoint()
    # auth_test()
    # test_swish()
    # test_create_payment()
    # print("All tests passed!")
    from datetime import datetime, timedelta
    print()
    print(datetime.now())
