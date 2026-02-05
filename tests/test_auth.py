def test_register_success_201(client):
    payload = {"email": "user1@test.com", "password": "StrongPass123!"}
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201, r.text

    data = r.json()
    assert "id" in data
    assert data["email"] == payload["email"]


def test_register_duplicate_email_400(client):
    payload = {"email": "dup@test.com", "password": "StrongPass123!"}
    r1 = client.post("/auth/register", json=payload)
    assert r1.status_code == 201, r1.text

    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 400, r2.text


def test_login_success_returns_token(client):
    # register first
    client.post("/auth/register", json={"email": "login@test.com", "password": "StrongPass123!"})

    # OAuth2PasswordRequestForm -> form-data: username/password
    r = client.post("/auth/login", data={"username": "login@test.com", "password": "StrongPass123!"})
    assert r.status_code == 200, r.text

    data = r.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


def test_login_wrong_password_401(client):
    client.post("/auth/register", json={"email": "wrong@test.com", "password": "StrongPass123!"})

    r = client.post("/auth/login", data={"username": "wrong@test.com", "password": "WRONGPASSWORD"})
    assert r.status_code == 401, r.text


def test_login_unknown_user_401(client):
    r = client.post("/auth/login", data={"username": "nouser@test.com", "password": "AnyPass123!"})
    assert r.status_code == 401, r.text