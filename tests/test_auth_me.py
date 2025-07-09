import pytest

def test_me_success(client, faker):
    # Registro de usuario
    user_data = {
        "username": faker.user_name(),
        "email": faker.email(),
        "password": "Password123"
    }
    register_resp = client.post("/api/auth/register", json=user_data)
    assert register_resp.status_code == 201

    # Login para obtener el token
    login_resp = client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Acceder al endpoint /me con el token
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 200

    user = me_resp.json()
    assert user["username"] == user_data["username"]
    assert user["email"] == user_data["email"]
    assert "id" in user
    assert "is_admin" in user


def test_me_without_token(client):
    me_resp = client.get("/api/auth/me")
    assert me_resp.status_code == 401
    assert me_resp.json()["detail"] == "Not authenticated"


def test_me_invalid_token(client):
    headers = {"Authorization": "Bearer invalid.token.value"}
    me_resp = client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 401
    assert me_resp.json()["detail"] in ["Token inválido", "Not authenticated", "No autenticado"]
