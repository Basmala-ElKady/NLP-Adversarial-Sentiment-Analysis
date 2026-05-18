from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Robust Sentiment Analysis API is running."

def test_prediction():
    response = client.post(
        "/predict",
        json={"text": "This movie is amazing"}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] in ["Positive", "Negative"]

def test_attack_endpoint():
    response = client.post(
        "/attack",
        json={
            "text": "This movie is amazing",
            "attack_name": "deepwordbug"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "perturbed_text" in data
    assert "prediction" in data
    assert "original_text" in data
