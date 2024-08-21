from run import app
from app.extensions import db
import pytest
import os


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def demount_db():
    """Code to teardown or reset the database"""
    db.drop_all()
    yield

@pytest.fixture
def get_version():
    """Fixture to fetch an environment variable."""
    version = os.getenv('VERSION')
    yield version