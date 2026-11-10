def test_create_application(client):
    response = client.post(
        "/applications",
        json={"company": "Google", "position": "Junior Developer"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["company"] == "Google"
    assert data["status"] == "applied"


def test_get_application_not_found(client):
    response = client.get("/applications/999")
    assert response.status_code == 404


def test_update_status(client):
    created = client.post(
        "/applications",
        json={"company": "Google", "position": "Junior Developer"},
    ).json()

    response = client.patch(
        f"/applications/{created['id']}",
        json={"status": "interview"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "interview"
    assert response.json()["company"] == "Google"


def test_delete_application(client):
    created = client.post(
        "/applications",
        json={"company": "Google", "position": "Junior Developer"},
    ).json()

    response = client.delete(f"/applications/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/applications/{created['id']}")
    assert response.status_code == 404


def test_invalid_status_is_rejected(client):
    response = client.post(
        "/applications",
        json={"company": "Google", "position": "Junior Developer", "status": "Applied"},
    )
    assert response.status_code == 422


def test_filter_by_status(client):
    client.post(
        "/applications",
        json={"company": "Google", "position": "Dev", "status": "offer"},
    )
    client.post(
        "/applications",
        json={"company": "Spotify", "position": "Dev", "status": "applied"},
    )

    response = client.get("/applications", params={"status": "offer"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["company"] == "Google"




def test_analytics_summary(client):
    for status in ["applied", "interview", "offer", "rejected"]:
        client.post(
            "/applications",
            json={"company": "Test", "position": "Dev", "status": status},
        )

    response = client.get("/analytics/summary")
    data = response.json()
    assert data["total"] == 4
    assert data["waiting"] == 1
    assert data["responded"] == 3
    assert data["response_rate_percent"] == 75


def test_analytics_status_counts(client):
    for status in ["applied", "applied", "offer"]:
        client.post(
            "/applications",
            json={"company": "Test", "position": "Dev", "status": status},
        )

    response = client.get("/analytics/status-counts")
    assert response.json() == {"applied": 2, "offer": 1}


def test_analytics_monthly(client):
    for day in ["2026-10-15", "2026-10-20", "2026-11-03"]:
        client.post(
            "/applications",
            json={"company": "Test", "position": "Dev", "applied_date": day},
        )

    response = client.get("/analytics/monthly")
    assert response.json() == {"2026-10": 2, "2026-11": 1}


def test_analytics_summary_empty_database(client):
    response = client.get("/analytics/summary")
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["response_rate_percent"] == 0