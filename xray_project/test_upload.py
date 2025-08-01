import requests
import json

# Test data
data = {
    "patient_id": "test123",
    "body_part": "Chest",
    "scan_date": "2025-07-31",
    "institution": "Test Hospital",
    "description": "Test scan",
    "diagnosis": "Normal",
    "tags": json.dumps(["test"])
}

# Make the request
response = requests.post('http://localhost:8000/api/scans/', data=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")