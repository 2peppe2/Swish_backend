from run import app
from app.extensions import db
import pytest
import os
from datetime import datetime, timedelta


from app.models import Payment
from app.utils.wrapper import require_api_key


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def teardown_database():
    """Code to teardown or reset the database"""
    with app.app_context():
        db.create_all()
    yield
    with app.app_context():
        db.drop_all()


@pytest.fixture
def get_version():
    """Fixture to fetch an environment variable."""
    version = os.getenv("VERSION")
    yield version


@pytest.fixture(scope="session")
def merchant_mock_client():
    from flask import Flask, request, jsonify
    from flask.testing import FlaskClient

    mock_server = Flask(__name__)

    @mock_server.route("/backend/payment/<ref>", methods=["GET"])
    @require_api_key
    def get_payment(ref):
        if ref == "404":
            return "", 404
        return jsonify(
            {
                "amount": 100,
                "message": "payment test",
                "payer_alias": "46712347689",
                "redirect_callback_url": "https://example.com/callback",
            }
        )

    @mock_server.route("/backend/payment/ref/<ref>", methods=["PUT"])
    @require_api_key
    def put_payment(ref):
        return "", 200

    with mock_server.test_client() as client:
        yield client


def add_payment_to_database(uuid, message="payment test"):
    payment = Payment(
        id=uuid,
        payee_payment_reference="0123456789",
        payment_reference=None,
        payer_alias=None,
        payee_alias="1234679304",
        amount=100,
        currency="SEK",
        message=message,
        status="PROCESSING",
        created_at=datetime.now() - timedelta(seconds=5),
        paid_at=None,
        redirect_callback_url="https://example.com/callback",
    )
    with app.app_context():
        db.session.add(payment)
        db.session.commit()
