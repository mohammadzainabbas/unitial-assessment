from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analysis():
    response = client.post("/analyze", json={
        "machines": [{
            "id": "test1",
            "manufacturer": "TestCo",
            "type": "excavator",
            "fuel_type": "electric",
            "battery_size": 100
        }],
        "data": [{
            "timestamp": 1672549200000,  # 2023-01-01 09:00:00
            "machine_id": "test1",
            "battery_SoC": 0.8
        }, {
            "timestamp": 1672556400000,  # 2023-01-01 11:00:00
            "machine_id": "test1",
            "battery_SoC": 0.4
        }]
    })
    
    assert response.status_code == 200
    result = response.json()
    assert result['machine_metrics'][0]['consumption'] == 40.0
    assert result['efficiency_metrics']['most_efficient'] == "test1"