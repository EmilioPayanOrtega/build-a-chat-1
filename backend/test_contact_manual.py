import requests
import json

def test_contact_endpoint():
    url = 'http://127.0.0.1:5000/api/contact'
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'subject': 'Test Subject',
        'message': 'This is a test message.'
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("SUCCESS: Contact endpoint works!")
        elif response.status_code == 500:
            print("WARNING: Endpoint reached but failed to send email (expected if no SMTP config).")
            print("Check backend logs for connection refused error, which confirms logic execution.")
        else:
            print("FAILURE: Unexpected status code.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_contact_endpoint()
