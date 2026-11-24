def test_page_accueil_accessible(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Liste des incidents" in response.get_data(as_text=True)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "OK"