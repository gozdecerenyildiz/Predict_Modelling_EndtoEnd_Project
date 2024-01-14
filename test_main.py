from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/model")
    assert response.status_code == 200
    assert b"Football Player Position Model" in response.content

    
def test_position_predict():
    payload = {
        "Positioning": 80,
        "Acceleration": 75,
        "Sprint_Speed": 78,
        "Finishing": 85,
        "Shot_Power": 88,
        "Long_Shots": 82,
        "Volleys": 79,
        "Penalties": 87,
        "Vision": 88,
        "Crossing": 75,
        "Free_Kick_Accuracy": 80,
        "Shot_Passing": 85,
        "Long_Passing": 83,
        "Curve": 78,
        "Agility": 80,
        "Balance": 82,
        "Reactions": 85,
        "Ball_Control": 87,
        "Detailed_Dribbling": 88,
        "Composure": 84,
        "Interception": 70,
        "Heading_Accuracy": 75,
        "Def_Awareness": 80,
        "Standing_Tackle": 77,
        "Sliding_Tackle": 75,
        "Jumping": 80,
        "Stamina": 82,
        "Strength": 84,
        "Aggression": 78,
        "Age": 28,
        "Att_Work_Rate": "Medium",
        "Def_Work_Rate": "High",
        "Foot": "Right",
}


    response = client.post("/position_predict", data=payload)
    assert response.status_code == 200
    assert "Prediction Result" in response.text
