import pytest
from app import app, students, redeemable_items, redeemed_items

@pytest.fixture
def client():
    # Create a test client
    app.testing = True
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_state():
    """
    Reset the application state before each test.
    """
    global students, redeemable_items, redeemed_items

    # Reset students to their initial state
    students.clear()
    students.extend([
        {
            'id': 'A1234567X',
            'name': 'John Tan',
            'diploma': 'Diploma in IT',
            'year_of_entry': 2024,
            'email': 'john.tan.2024@example.edu',
            'points': 50
        },
        {
            'id': 'A1234568Y',
            'name': 'Sarah Lim',
            'diploma': 'Diploma in Business',
            'year_of_entry': 2023,
            'email': 'sarah.lim.2023@example.edu',
            'points': 80
        }
    ])

    # Reset redeemable_items to their initial state
    redeemable_items.clear()
    redeemable_items.extend([
        {'id': 1, 'name': 'Book', 'points_required': 100, 'quantity': 10},
        {'id': 2, 'name': 'Pen', 'points_required': 50, 'quantity': 20},
    ])

    # Reset redeemed_items to their initial state
    redeemed_items.clear()

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
        username='A1234567X',  # Valid student ID (John Tan)
        password='student'     # Valid password
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Student Page' in response.data  # Check if redirected to the student page

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
        username='A1234567X',  # Valid student ID (John Tan)
        password='student'     # Valid password
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Student Page' in response.data  # Check if redirected to the student page