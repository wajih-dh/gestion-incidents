def test_liste_vide(client):
    response = client.get("/")
    assert "Aucun incident" in response.get_data(as_text=True)


def test_ajouter_incident(client, incident_data):
    response = client.post("/ajouter", data=incident_data, follow_redirects=True)
    assert response.status_code == 200
    assert "Panne Wi-Fi" in response.get_data(as_text=True)


def test_ajouter_incident_invalide(client):
    response = client.post("/ajouter", data={"titre": ""})
    assert response.status_code == 400


def test_detail_incident(client, incident_data):
    client.post("/ajouter", data=incident_data)
    response = client.get("/incident/1")
    assert response.status_code == 200
    assert "Labo L3" in response.get_data(as_text=True)


def test_modifier_statut(client, incident_data):
    client.post("/ajouter", data=incident_data)
    response = client.post(
        "/incident/1/statut", data={"statut": "Résolu"}, follow_redirects=True
    )
    assert "Résolu" in response.get_data(as_text=True)


def test_supprimer_incident(client, incident_data):
    client.post("/ajouter", data=incident_data)
    client.post("/incident/1/supprimer")
    assert client.get("/incident/1").status_code == 404