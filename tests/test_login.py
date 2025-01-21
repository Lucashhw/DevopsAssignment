import pytest
from app import app  # Use absolute import

@pytest.fixture
def client():
    # Create a test client
    app.testing = True
    return app.test_client()

def test_valid_admin_login(client):
    # Test valid admin login
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Page' in response.data

def test_valid_student_login(client):
    # Test valid student login
    response = client.post('/login', data=dict(
        username='student',
        password='student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Student Page' in response.data

def test_invalid_login(client):
    # Test invalid login
    response = client.post('/login', data=dict(
        username='wrong',
        password='wrong'
    ))
    assert response.status_code == 200
    assert b'Invalid username' in response.data

def test_empty_fields(client):
    # Test empty username and password
    response = client.post('/login', data=dict(
        username='',
        password=''
    ))
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_invalid_username(client):
    # Test invalid username
    response = client.post('/login', data=dict(
        username='wrong_username',  # Invalid username
        password='admin'  # Valid password
    ))
    assert response.status_code == 200
    assert b'Invalid username' in response.data  # Check for the specific error message

def test_invalid_password(client):
    # Test invalid password
    response = client.post('/login', data=dict(
        username='admin',  # Valid username
        password='wrong_password'  # Invalid password
    ))
    assert response.status_code == 200
    assert b'Invalid password' in response.data  # Check for the specific error message

def test_recover_password_link(client):
    # Test recover password link
    response = client.get('/')
    assert response.status_code == 200
    assert b'href="/recover_password"' in response.data

def test_redirect_after_admin_login(client):
    # Test redirect to admin page after successful login
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Page' in response.data

def test_redirect_after_student_login(client):
    # Test redirect to student page after successful login
    response = client.post('/login', data=dict(
        username='student',
        password='student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Student Page' in response.data