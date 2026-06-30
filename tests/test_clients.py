def _create_client(client, headers, name="Анна", phone="+79001112233"):
    return client.post(
        "/api/v1/clients",
        headers=headers,
        json={"name": name, "phone": phone, "email": None, "comment": "vip"},
    )


def test_create_and_get_client(client, admin_headers):
    resp = _create_client(client, admin_headers)
    assert resp.status_code == 201
    client_id = resp.json()["id"]

    resp = client.get(f"/api/v1/clients/{client_id}", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Анна"


def test_list_and_search_clients(client, admin_headers):
    _create_client(client, admin_headers, name="Анна", phone="+70001")
    _create_client(client, admin_headers, name="Борис", phone="+70002")

    resp = client.get("/api/v1/clients", headers=admin_headers)
    assert resp.json()["total"] == 2

    resp = client.get("/api/v1/clients", headers=admin_headers, params={"q": "Борис"})
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["name"] == "Борис"


def test_update_client(client, admin_headers):
    cid = _create_client(client, admin_headers).json()["id"]
    resp = client.patch(
        f"/api/v1/clients/{cid}", headers=admin_headers, json={"comment": "updated"}
    )
    assert resp.status_code == 200
    assert resp.json()["comment"] == "updated"


def test_delete_client_requires_role(client, admin_headers, employee_headers):
    cid = _create_client(client, admin_headers).json()["id"]
    # employee не может удалять
    assert (
        client.delete(f"/api/v1/clients/{cid}", headers=employee_headers).status_code
        == 403
    )
    # admin может
    assert (
        client.delete(f"/api/v1/clients/{cid}", headers=admin_headers).status_code
        == 204
    )
    assert client.get(f"/api/v1/clients/{cid}", headers=admin_headers).status_code == 404


def test_client_not_found(client, admin_headers):
    assert client.get("/api/v1/clients/999", headers=admin_headers).status_code == 404
