import pytest

def test_register_user_success(client, faker):
    user_data = {
        "username": faker.user_name(),
        "email": faker.email(),
        "password": "Password123"
    }

    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == 201
    response_json = response.json()
    assert "user_id" in response_json
    assert response_json["username"] == user_data["username"]
    assert response_json["email"] == user_data["email"]

def test_register_user_duplicate_email(client, faker):
    common_email = faker.email()

    # Primer registro exitoso
    user_data_1 = {
        "username": faker.user_name(),
        "email": common_email,
        "password": "Password123"
    }
    res1 = client.post("/api/auth/register", json=user_data_1)
    assert res1.status_code == 201

    # Segundo intento con mismo email
    user_data_2 = {
        "username": faker.user_name(),
        "email": common_email,
        "password": "Password456"
    }
    res2 = client.post("/api/auth/register", json=user_data_2)
    assert res2.status_code == 400
    assert "detail" in res2.json()

def test_register_user_invalid_email(client):
    user_data = {
        "username": "invaliduser",
        "email": "notanemail",
        "password": "Password123"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 422  # Unprocessable Entity

