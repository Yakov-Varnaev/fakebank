import pytest
from fastapi.testclient import TestClient

from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app.main import app
from app.users.models import User


@pytest.fixture
def as_anon():
    return TestClient(app=app, base_url='http://localhost:8000')


class UserFactory(SQLAlchemyFactory[User]):
    pass


@pytest.fixture
def user() -> User:
    return UserFactory.build()
