from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Running"

def test_prediction_endpoint_exists():
    response = client.post(
        "/predict",
        json={
            "Age": 30,
            "Gender": "Male",
            "Education_Level": "Master's",
            "Job_Title": "Data Scientist",
            "Years_of_Experience": 5
        }
    )
    assert response.status_code == 200
