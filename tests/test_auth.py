def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_register_and_login(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@test.example.com",
            "full_name": "New User",
            "password": "password123",
            "role": "manager",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["email"] == "new@test.example.com"

    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "new@test.example.com", "password": "password123"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_duplicate_email_rejected(client):
    payload = {
        "email": "dup@test.example.com",
        "full_name": "Dup",
        "password": "password123",
    }
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "x@test.example.com", "full_name": "X", "password": "password123"},
    )
    resp = client.post(
        "/api/v1/auth/login", json={"email": "x@test.example.com", "password": "wrong"}
    )
    assert resp.status_code == 401


def test_me_requires_auth(client):
    assert client.get("/api/v1/auth/me").status_code == 401


def test_me_returns_current_user(client, admin_headers):
    resp = client.get("/api/v1/auth/me", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["role"] == "admin"
