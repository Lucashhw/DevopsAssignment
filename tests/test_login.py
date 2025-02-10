import unittest
from app import app, db
from app.models import Student

class TestLoginProcess(unittest.TestCase):
    def setUp(self):
        """Set up the test environment before each test."""
        self.client = app.test_client()
        # Drop all tables and recreate them to ensure a clean slate
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        """Helper method to populate the database with test data."""
        with app.app_context():
            admin = Student(
                id='admin',
                name='Admin User',
                diploma='N/A',
                year_of_entry=0,
                email='admin@example.edu',
                points=0,
                password_hash='admin'
            )
            student = Student(
                id='A1234567X',
                name='John Tan',
                diploma='Diploma in IT',
                year_of_entry=2024,
                email='john.tan.2024@example.edu',
                points=50,
                password_hash='student'
            )
            db.session.add(admin)
            db.session.add(student)
            db.session.commit()

    def test_admin_login_success(self):
        """Test successful admin login."""
        self.create_test_data()
        response = self.client.post('/login', data=dict(
            username='admin',
            password='admin'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Page', response.data)

    def test_student_login_success(self):
        """Test successful student login."""
        self.create_test_data()
        response = self.client.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Page', response.data)

    def test_invalid_username(self):
        """Test login with invalid username."""
        self.create_test_data()
        response = self.client.post('/login', data=dict(
            username='invalid_user',
            password='student'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_invalid_password(self):
        """Test login with invalid password."""
        self.create_test_data()
        response = self.client.post('/login', data=dict(
            username='A1234567X',
            password='wrong_password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_recover_password_page_redirect(self):
        """Test redirection to the recover password page."""
        response = self.client.get('/recover_password', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recover Password', response.data)

if __name__ == '__main__':
    unittest.main()