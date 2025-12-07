import requests
import json
import os

# Si no existe la variable, usa localhost por default
BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5001")

def test_signup():
    print("Testing Signup...")
    url = f"{BASE_URL}/signup"
    payload = {
        "username": "testuser_controller_py",
        "email": "test_controller_py@example.com",
        "password": "password123"
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code in [201, 409]:
            print("Signup Test Passed")
        else:
            print("Signup Test Failed")
    except Exception as e:
        print(f"Signup Test Error: {e}")

def test_login():
    print("\nTesting Login...")
    url = f"{BASE_URL}/login"
    payload = {
        "username": "testuser_controller_py",
        "password": "password123"
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("Login Test Passed")
        else:
            print("Login Test Failed")
    except Exception as e:
        print(f"Login Test Error: {e}")

if __name__ == "__main__":
    print(f"Using API URL: {BASE_URL}")
    test_signup()
    test_login()
