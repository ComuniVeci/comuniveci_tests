import pytest

def register_user_for_login(client, faker):
    user_data = {
        "username": faker.user_name(),
        "email": faker.email(),
        "password": "TestPass123"
    }
    res = client.post("/api/auth/register", json=user_data)
    assert res.status_code == 201
    return user_data

def test_login_success(client, faker):
    user_data = register_user_for_login(client, faker)
    login_payload = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    res = client.post("/api/auth/login", json=login_payload)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_login_wrong_password(client, faker):
    user_data = register_user_for_login(client, faker)
    login_payload = {
        "email": user_data["email"],
        "password": "WrongPassword"
    }
    res = client.post("/api/auth/login", json=login_payload)
    assert res.status_code == 401
    assert res.json()["detail"] == "Credenciales inválidas"

def test_login_nonexistent_email(client):
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "AnyPass123"
    }
    res = client.post("/api/auth/login", json=login_payload)
    assert res.status_code == 401
    assert res.json()["detail"] == "Credenciales inválidas"
