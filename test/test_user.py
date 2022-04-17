from app import schema
import pytest

def test_create_user(client):
    res = client.post("/createuser_sqlalchemy", json={"email": "example@example.com", "password": "12345678", "username": "example1"})
    new_user = schema.UserResponse(**res.json())

    assert res.status_code == 201
    assert new_user.email == "example@example.com"
    assert new_user.username == "example1"


def test_login(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    assert res.status_code == 202


@pytest.mark.parametrize("email, password, status_code", [
    ("example@example.com","wrongpassword", 403),
    ("wrongemail@example.com","12345678", 403),
    ("wrongemail@example.com","wrongpassword", 403),
    (None,"12345678", 422),
    ("example@example.com",None, 422)])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
