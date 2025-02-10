import unittest
from app import app, db
from app.models import Student

class TestRecoverPasswordProcess(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a test client and populating the database.
        """
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection during tests
        with app.app_context():
            db.drop_all()  # Drop all tables to ensure a clean slate
            db.create_all()  # Recreate all tables
            # Add a sample student
            student = Student(
                id='A1234567X',
                name='John Tan',
                diploma='Diploma in IT',
                year_of_entry=2024,
                email='john.tan.2024@example.edu',
                points=500,
                password_hash='student'  # Default password hash for testing
            )
            db.session.add(student)
            db.session.commit()

    def tearDown(self):
        """
        Clean up the test environment by dropping all tables.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_recover_password_page_redirect(self):
        """
        Test redirection to the recover password page.
        """
        response = self.app.get('/recover_password', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recover Password', response.data)

    def test_recover_password_with_valid_username(self):
        """
        Test successful password recovery with a valid username.
        """
        response = self.app.post('/recover_password', data=dict(
            username='A1234567X',
            new_password='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password has been successfully updated.', response.data)

        # Verify the password was updated in the database
        with app.app_context():
            student = db.session.get(Student, 'A1234567X')
            self.assertIsNotNone(student)
            self.assertEqual(student.password_hash, 'newpassword')

    def test_recover_password_with_invalid_username(self):
        """
        Test password recovery with an invalid username.
        """
        response = self.app.post('/recover_password', data=dict(
            username='INVALID_USER',
            new_password='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No account found with the provided username.', response.data)

    def test_recover_password_with_empty_username(self):
        """
        Test password recovery with an empty username.
        """
        response = self.app.post('/recover_password', data=dict(
            username='',
            new_password='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please provide both username and a new password.', response.data)

    def test_recover_password_with_empty_new_password(self):
        """
        Test password recovery with an empty new password.
        """
        response = self.app.post('/recover_password', data=dict(
            username='A1234567X',
            new_password=''
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please provide both username and a new password.', response.data)

if __name__ == '__main__':
    unittest.main()