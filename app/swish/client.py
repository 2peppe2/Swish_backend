import requests
from datetime import datetime
import json


from .environment import Environment
from .models import Payment, Refund
from app.utils import generate_uuid

try:
    from urllib3.contrib import pyopenssl

    pyopenssl.extract_from_urllib3()
except ImportError:
    pass


class SwishClient(object):
    def __init__(self, environment, merchant_swish_number, cert, verify=False):
        
        self.environment = Environment.parse_environment(environment)
        self.merchant_swish_number = merchant_swish_number
        self.cert = cert
        self.verify = verify

    def post(self, endpoint:str, payload:dict)->requests.Response:
        url = self.environment.base_url + endpoint
        return requests.put(
            url=url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            cert=self.cert
        )
    def patch(self, endpoint:str, payload:dict)->requests.Response:
        url = self.environment.base_url + endpoint
        return requests.patch(
            url=url,
            data=payload,
            headers={"Content-Type": "application/json-patch+json"},
            cert=self.cert,
            verify=self.verify,
        )

    def get(self, endpoint:str)->requests.Response:
        url = self.environment.base_url + endpoint
        return requests.get(url, cert=self.cert, verify=self.verify)

    def create_payment(
        self,
        amount:float,
        currency:str,
        callback_url:str,
        payee_payment_reference:str,
        message:str,
        payer_alias:str,
    )->Payment:
        payment_request = Payment(
            {
                "payee_alias": self.merchant_swish_number,
                "amount": str(amount),
                "currency": currency,
                "callback_url": callback_url,
                "payee_payment_reference": payee_payment_reference,
                "message": message,
                "payer_alias": payer_alias,
            }
        )

        uuid = generate_uuid()
        response = self.post("v2/paymentrequests/" + uuid, payment_request.to_primitive())
        response.raise_for_status()
        updated_payment_request_data = {
            "id": uuid,
            "location": response.headers.get("Location"),
            "status": "CREATED",
            "date_created": datetime.now(),
        }
        payment_request.import_data(updated_payment_request_data)
        return payment_request

    def get_payment(self, payment_request_id):
        response = self.get("v1/paymentrequests/" + payment_request_id)
        response.raise_for_status()
        response_dict = response.json()
        del response_dict["callbackIdentifier"]
        return Payment(response_dict)
    
    def cancel_payment(self, payment_request_id):
        response = self.patch("v1/paymentrequests/" + payment_request_id, {
            "op": "replace",
            "path": "/status",
            "value": "cancelled"
        })
        response.raise_for_status()
        return Payment(response.json())

    def create_refund(
        self,
        original_payment_reference,
        amount,
        currency,
        callback_url,
        payer_payment_reference=None,
        payment_reference=None,
        payee_alias=None,
        message=None,
    ):
        refund_request = Refund(
            {
                "payer_alias": self.merchant_swish_number,
                "payee_alias": payee_alias,
                "original_payment_reference": original_payment_reference,
                "amount": amount,
                "currency": currency,
                "callback_url": callback_url,
                "payer_payment_reference": payer_payment_reference,
                "payment_reference": payment_reference,
                "message": message,
            }
        )

        response = self.post("refunds", refund_request.to_primitive())
        response.raise_for_status()

        return Refund(
            {
                "id": response.headers.get("Location").split("/")[-1],
                "location": response.headers.get("Location"),
            }
        )

    def get_refund(self, refund_id):
        response = self.get("refunds/" + refund_id)
        response.raise_for_status()
        return Refund(response.json())
