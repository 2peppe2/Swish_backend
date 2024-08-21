from datetime import datetime, timedelta

from app.models import Payment
from run import app
from . import client, get_version


def test_payment_external(client, get_version):
    response = client.get(
        f"/v{get_version}/backend/payment/external/123456789",
        headers={"x-api-key": "api-key"},
    )
    assert response.status_code == 200