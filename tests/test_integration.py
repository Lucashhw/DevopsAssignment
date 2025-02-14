import requests
import pytest

# Base URL of the backend API 
BASE_URL = "http://127.0.0.1:3000"  

# Test user credentials
TEST_USER = {"username": "john.tan", "password": "test123"}
NEW_USER = {"student_id": "A1234569Z", "name": "New Student", "points": 100}

@pytest.fixture(scope="session")
def get_auth_token():
    """Login and retrieve authentication token"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    assert response.status_code == 200
    return response.json().get("token")

def test_login_success():
    """Test successful login"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    """Test login with incorrect password"""
    response = requests.post(f"{BASE_URL}/login", json={"username": "john.tan", "password": "wrongpass"})
    assert response.status_code == 401  # Unauthorized

def test_create_student(get_auth_token):
    """Test admin creates a new student account"""
    headers = {"Authorization": f"Bearer {get_auth_token}"}
    response = requests.post(f"{BASE_URL}/admin/students", json=NEW_USER, headers=headers)
    assert response.status_code == 201
    assert response.json()["message"] == "Student created successfully"

def test_get_student_list(get_auth_token):
    """Test retrieving student list"""
    headers = {"Authorization": f"Bearer {get_auth_token}"}
    response = requests.get(f"{BASE_URL}/admin/students", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_modify_student(get_auth_token):
    """Test updating student information"""
    headers = {"Authorization": f"Bearer {get_auth_token}"}
    update_data = {"name": "Updated Student", "points": 200}
    response = requests.put(f"{BASE_URL}/admin/students/A1234569Z", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Student updated successfully"

def test_delete_student(get_auth_token):
    """Test deleting a student"""
    headers = {"Authorization": f"Bearer {get_auth_token}"}
    response = requests.delete(f"{BASE_URL}/admin/students/A1234569Z", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Student deleted successfully"

def test_redeem_item(get_auth_token):
    """Test student redeems an item"""
    headers = {"Authorization": f"Bearer {get_auth_token}"}
    redeem_data = {"student_id": "A1234567X", "item_id": 1}  # Adjust item ID if needed
    response = requests.post(f"{BASE_URL}/redeem", json=redeem_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_password_recovery():
    """Test password recovery process"""
    response = requests.post(f"{BASE_URL}/recover-password", json={"username": "john.tan"})
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset link sent"

if __name__ == "__main__":
    pytest.main()
