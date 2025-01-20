import unittest
from app import app  # Import the Flask app

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Propagate exceptions to the test client
        self.app.testing = True

    def test_valid_admin_login(self):
        # Test valid admin login
        response = self.app.post('/login', data=dict(
            username='admin',
            password='admin'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Check if the response is successful
        self.assertIn(b'Welcome to the Admin Page', response.data)  # Check if redirected to Admin Page

    def test_valid_student_login(self):
        # Test valid student login
        response = self.app.post('/login', data=dict(
            username='student',
            password='student'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Check if the response is successful
        self.assertIn(b'Welcome to the Student Page', response.data)  # Check if redirected to Student Page

    def test_invalid_login(self):
        # Test invalid login
        response = self.app.post('/login', data=dict(
            username='wrong',
            password='wrong'
        ))
        self.assertEqual(response.status_code, 200)  # Check if the response is successful
        self.assertIn(b'Invalid username or password', response.data)  # Check error message

    def test_empty_fields(self):
        # Test empty username and password
        response = self.app.post('/login', data=dict(
            username='',
            password=''
        ))
        self.assertEqual(response.status_code, 200)  # Check if the response is successful
        self.assertIn(b'Invalid username or password', response.data)  # Check error message

if __name__ == '__main__':
    unittest.main()