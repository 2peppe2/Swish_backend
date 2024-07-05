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

def temp_test():
    from dotenv import load_dotenv
    from os import getenv
    import json


    data = {
            "payeePaymentReference": "0123456789",
            "callbackUrl": "https://example.com/api/swishcb/paymentrequests",
            "payerAlias": "4671234768",
            "payeeAlias": "1234679304",
            "amount": "100",
            "currency": "SEK",
            "message": "Kingston USB Flash Drive 8 GB"
        }
    data_dump = json.dumps(data)
    print(data_dump)
    response = requests.put(
        url="https://mss.cpc.getswish.net/swish-cpcapi/api/v2/paymentrequests/11A86BE70EA346E4B1C39C874173F088",
        headers={"Content-Type": "application/json"},
        cert=("certs/Swish_Merchant_TestCertificate_1234679304.pem", "certs/Swish_Merchant_TestCertificate_1234679304.key"),
        verify="certs/Swish_TLS_RootCA.pem",
        json=data_dump
        )
    print(response)
if __name__ == "__main__":
    pass
    # test_temp_endpoint()
    # auth_test()
    #test_swish()
    # test_create_payment()
    # print("All tests passed!")
    temp_test()