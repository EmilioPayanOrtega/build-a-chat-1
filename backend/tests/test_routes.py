import pytest

def test_signup_route_success(client):
    response = client.post('/signup', json={
        "username": "apiuser",
        "email": "api@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json['success'] is True

def test_signup_route_missing_data(client):
    response = client.post('/signup', json={
        "username": "apiuser"
    })
    assert response.status_code == 400
    assert response.json['success'] is False

def test_login_route_success(client):
    # Register first
    client.post('/signup', json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123"
    })
    
    # Login
    response = client.post('/login', json={
        "username": "loginuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'user_id' in response.json

def test_login_route_invalid(client):
    response = client.post('/login', json={
        "username": "nonexistent",
        "password": "password123"
    })
    assert response.status_code == 401
    assert response.json['success'] is False
