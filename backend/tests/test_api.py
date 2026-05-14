from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200


def test_prediction():

    response = client.post(
        "/predict",
        json={
            "text": "This movie is amazing"
        }
    )

    assert response.status_code == 200

    assert "prediction" in response.json()
