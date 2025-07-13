import pytest

def register_user_for_login(client, faker, track_created_user):
    user_data = {
        "username": faker.user_name(),
        "email": faker.email(),
        "password": "TestPass123"
    }
    res = client.post("/api/auth/register", json=user_data)
    assert res.status_code == 201
    # Registrar para eliminación
    track_created_user(user_data["email"])
    return user_data

@pytest.mark.backend
def test_login_success(client, faker, track_created_user):
    user_data = register_user_for_login(client, faker, track_created_user)
    login_payload = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    res = client.post("/api/auth/login", json=login_payload)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

@pytest.mark.backend
def test_login_wrong_password(client, faker, track_created_user):
    user_data = register_user_for_login(client, faker, track_created_user)
    login_payload = {
        "email": user_data["email"],
        "password": "WrongPassword"
    }
    res = client.post("/api/auth/login", json=login_payload)
    assert res.status_code == 401
    assert res.json()["detail"] == "Credenciales inválidas"

@pytest.mark.backend
def test_login_nonexistent_email(client):
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "AnyPass123"
    }
    res = client.post("/api/auth/login", json=login_payload)
    assert res.status_code == 401
    assert res.json()["detail"] == "Credenciales inválidas"
