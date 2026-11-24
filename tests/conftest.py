import pytest
from app import create_app
#base sqlLite pour les tests

@pytest.fixture
def client(tmp_path):
    app = create_app({"DATABASE": str(tmp_path / "test.db"), "TESTING": True})
    return app.test_client()


@pytest.fixture
def incident_data():
    return {
        "titre": "Panne Wi-Fi",
        "description": "Pas de connexion dans le laboratoire.",
        "lieu": "Labo L3",
        "priorite": "Élevée",
    }