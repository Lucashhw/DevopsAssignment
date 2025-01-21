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
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Page', response.data)

    def test_valid_student_login(self):
        # Test valid student login
        response = self.app.post('/login', data=dict(
            username='student',
            password='student'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Page', response.data)

    def test_invalid_login(self):
        # Test invalid login
        response = self.app.post('/login', data=dict(
            username='wrong',
            password='wrong'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username', response.data)



    def test_empty_fields(self):
        # Test empty username and password
        response = self.app.post('/login', data=dict(
            username='',
            password=''
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_invalid_username(self):
        # Test invalid username
        response = self.app.post('/login', data=dict(
            username='wrong_username',  # Invalid username
            password='admin'  # Valid password
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username', response.data)  # Check for the specific error message


    def test_invalid_password(self):
        # Test invalid password
        response = self.app.post('/login', data=dict(
            username='admin',  # Valid username
            password='wrong_password'  # Invalid password
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid password', response.data)  # Check for the specific error message

    def test_recover_password_link(self):
        # Test recover password link
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'href="/recover_password"', response.data)

    def test_redirect_after_admin_login(self):
        # Test redirect to admin page after successful login
        response = self.app.post('/login', data=dict(
            username='admin',
            password='admin'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Page', response.data)

    def test_redirect_after_student_login(self):
        # Test redirect to student page after successful login
        response = self.app.post('/login', data=dict(
            username='student',
            password='student'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Page', response.data)

if __name__ == '__main__':
    unittest.main()