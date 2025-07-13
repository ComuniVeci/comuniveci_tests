import pytest

@pytest.mark.backend
def test_register_user_success(client, faker, track_created_user):
    user_data = {
        "username": faker.user_name(),
        "email": faker.email(),
        "password": "Password123"
    }

    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == 201
    response_json = response.json()
    assert "access_token" in response_json
    assert "token_type" in response_json
    assert "message" in response_json

    # Registrar para limpieza solo si se creó correctamente
    track_created_user(user_data["email"])

@pytest.mark.backend
def test_register_user_duplicate_email(client, faker, track_created_user):
    common_email = faker.email()

    # Primer registro exitoso
    user_data_1 = {
        "username": faker.user_name(),
        "email": common_email,
        "password": "Password123"
    }
    res1 = client.post("/api/auth/register", json=user_data_1)
    assert res1.status_code == 201

    # Registrar para limpieza
    track_created_user(common_email)

    # Segundo intento con mismo email
    user_data_2 = {
        "username": faker.user_name(),
        "email": common_email,
        "password": "Password456"
    }
    res2 = client.post("/api/auth/register", json=user_data_2)
    assert res2.status_code == 400
    assert "detail" in res2.json()

@pytest.mark.backend
def test_register_user_invalid_email(client):
    user_data = {
        "username": "invaliduser",
        "email": "notanemail",
        "password": "Password123"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 422  # Unprocessable Entity

