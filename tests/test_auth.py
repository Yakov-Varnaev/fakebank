from http import HTTPStatus
from fastapi.testclient import TestClient

from app.main import app
from app.users.models import User


def test_register():
    client = TestClient(app, base_url='http://localhost:8000')
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK


def test_anonymouse_cannot_create_account(user: User):

    assert isinstance(user, User)
