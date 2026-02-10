import uuid


def _email() -> str:
    return f"user_{uuid.uuid4().hex[:10]}@example.com"


def register_user(client, email: str, password: str = "password123"):
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 201, r.text
    return r.json()


def login_user(client, email: str, password: str = "password123") -> str:
    # OAuth2PasswordRequestForm -> form-data: username/password
    r = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def create_task(client, token: str, title: str = "My task"):
    r = client.post(
        "/tasks",
        json={
            "title": title,
            "description": "d",
            "status": "todo",
            "priority": "medium",
        },
        headers=auth_headers(token),
    )
    assert r.status_code == 201, r.text
    return r.json()


def test_get_foreign_task_returns_403(client):
    email_a, email_b = _email(), _email()
    password = "password123"

    register_user(client, email_a, password)
    register_user(client, email_b, password)

    token_a = login_user(client, email_a, password)
    token_b = login_user(client, email_b, password)

    task = create_task(client, token_a, title="A task")
    task_id = task["id"]

    r = client.get(f"/tasks/{task_id}", headers=auth_headers(token_b))
    assert r.status_code == 403, r.text


def test_patch_foreign_task_returns_403(client):
    email_a, email_b = _email(), _email()
    password = "password123"

    register_user(client, email_a, password)
    register_user(client, email_b, password)

    token_a = login_user(client, email_a, password)
    token_b = login_user(client, email_b, password)

    task = create_task(client, token_a, title="A task")
    task_id = task["id"]

    r = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Hacked"},
        headers=auth_headers(token_b),
    )
    assert r.status_code == 403, r.text


def test_delete_foreign_task_returns_403(client):
    email_a, email_b = _email(), _email()
    password = "password123"

    register_user(client, email_a, password)
    register_user(client, email_b, password)

    token_a = login_user(client, email_a, password)
    token_b = login_user(client, email_b, password)

    task = create_task(client, token_a, title="A task")
    task_id = task["id"]

    r = client.delete(f"/tasks/{task_id}", headers=auth_headers(token_b))
    assert r.status_code == 403, r.text


def test_not_found_stays_404(client):
    email = _email()
    password = "password123"

    register_user(client, email, password)
    token = login_user(client, email, password)

    r = client.get("/tasks/99999999", headers=auth_headers(token))
    assert r.status_code == 404, r.text