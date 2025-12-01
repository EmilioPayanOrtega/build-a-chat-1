import pytest

def test_signup_route_success(client):
    response = client.post('/api/auth/register', json={
        "username": "apiuser",
        "email": "api@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json['success'] is True

def test_signup_route_creator_success(client):
    response = client.post('/api/auth/register', json={
        "username": "creator",
        "email": "creator@example.com",
        "password": "password123",
        "role": "creator"
    })
    assert response.status_code == 201
    assert response.json['success'] is True

def test_signup_route_missing_data(client):
    response = client.post('/api/auth/register', json={
        "username": "apiuser"
    })
    assert response.status_code == 400

def test_login_route_success(client):
    # Register first
    client.post('/api/auth/register', json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123"
    })
    
    response = client.post('/api/auth/login', json={
        "username": "loginuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json['success'] is True

def test_login_route_invalid(client):
    response = client.post('/api/auth/login', json={
        "username": "nonexistent",
        "password": "password123"
    })
    assert response.status_code == 401
    assert response.json['success'] is False
