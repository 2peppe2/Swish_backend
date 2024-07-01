import pytest
from run import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        yield client


def test_payment_create_route(client):
    """Test the home route."""
    response = client.post(
        "/payment/create",
        json={
            "payeePaymentReference": "Id4",
            "payerAlias": "123456780",
            "amount": 100,
            "message": "Test",
        },
    )
    assert response.status_code == 200
