import pytest


@pytest.fixture()
def refs(client, admin_headers):
    """Создаёт клиента, сотрудника и услугу, возвращает их id."""
    cid = client.post(
        "/api/v1/clients",
        headers=admin_headers,
        json={"name": "Клиент", "phone": "+70000000000"},
    ).json()["id"]
    eid = client.post(
        "/api/v1/employees",
        headers=admin_headers,
        json={"name": "Мастер", "position": "Барбер"},
    ).json()["id"]
    sid = client.post(
        "/api/v1/services",
        headers=admin_headers,
        json={"name": "Стрижка", "price": "1000.00", "duration_minutes": 45},
    ).json()["id"]
    return {"client_id": cid, "employee_id": eid, "service_id": sid}


def _create_appointment(client, headers, refs, status="new"):
    return client.post(
        "/api/v1/appointments",
        headers=headers,
        json={
            **refs,
            "scheduled_at": "2026-07-01T10:00:00+00:00",
            "status": status,
        },
    )


def test_create_appointment_with_relations(client, admin_headers, refs):
    resp = _create_appointment(client, admin_headers, refs)
    assert resp.status_code == 201
    body = resp.json()
    assert body["client"]["name"] == "Клиент"
    assert body["employee"]["position"] == "Барбер"
    assert body["service"]["name"] == "Стрижка"
    assert body["status"] == "new"


def test_create_appointment_invalid_client(client, admin_headers, refs):
    bad = {**refs, "client_id": 9999}
    resp = _create_appointment(client, admin_headers, bad)
    assert resp.status_code == 404


def test_update_appointment_status(client, admin_headers, refs):
    aid = _create_appointment(client, admin_headers, refs).json()["id"]
    resp = client.patch(
        f"/api/v1/appointments/{aid}",
        headers=admin_headers,
        json={"status": "confirmed"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "confirmed"


def test_filter_appointments_by_status(client, admin_headers, refs):
    _create_appointment(client, admin_headers, refs, status="new")
    _create_appointment(client, admin_headers, refs, status="done")

    resp = client.get(
        "/api/v1/appointments", headers=admin_headers, params={"status": "done"}
    )
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["status"] == "done"


def test_activity_log_records_actions(client, admin_headers, refs):
    _create_appointment(client, admin_headers, refs)
    resp = client.get("/api/v1/activity", headers=admin_headers)
    assert resp.status_code == 200
    actions = {item["entity"] for item in resp.json()["items"]}
    assert "appointment" in actions
