# this file is for storing all the needed fixtures. Tthis file eliminates the need of import all the fixtures in each test file.

from app.database import get_db
from app.database import Base
import pytest
from fastapi.testclient import TestClient
from app.fast_orm import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.oauth import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    """creates a table in the test database and deletes it after the test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()  # this is a fixture. it runs before the test is run.
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db  # overrides the get_db dependency so infomation can be passed to the test database.

    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    """creates a test user"""
    user_data = {"email": "example@example.gmail.com", "password": "12345678", "username": "example1"}
    res = client.post("/createuser_sqlalchemy", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user

@pytest.fixture()
def test_token(client, test_user):
    """creates a test token"""
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture()
def authorized_client(client, test_token):
    """creates a test client with a test token"""
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token}"}
    return client