import pytest
from starlette.testclient import TestClient
from main import app

@pytest.fixture(scope="function", autouse=True)
def client():
    client = TestClient(app)
    yield client

