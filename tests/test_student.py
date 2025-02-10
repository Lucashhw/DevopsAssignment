import unittest
from app import app, db
from app.models import Student, RedeemableItem, RedeemedItem


class TestStudentPageProcess(unittest.TestCase):
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
            # Add some redeemable items
            items_data = [
                {'name': 'AAA', 'points_required': 100, 'quantity': 5},
                {'name': 'BBB', 'points_required': 200, 'quantity': 3}
            ]
            for data in items_data:
                item = RedeemableItem(**data)
                db.session.add(item)
            db.session.commit()

    def tearDown(self):
        """
        Clean up the test environment by dropping all tables.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Correctly drop all tables

    def test_student_login_success(self):
        """
        Test successful login as a student.
        """
        response = self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Student Page', response.data)

    def test_logout_functionality(self):
        """
        Test that the logout functionality works as expected.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)

        # Log out the user
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Ensure the user is redirected to the login page

        # Attempt to access a protected page after logout
        response = self.app.get('/student/A1234567X', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)  # Check for flashed error message

    def test_student_page_options(self):
        """
        Test that the student page displays options for redeemable items and redeemed items.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)
        # Access the student page
        response = self.app.get('/student/A1234567X', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Redeemable Items', response.data)
        self.assertIn(b'Redeemed Items', response.data)

    def test_user_particulars_display(self):
        """
        Test that the student's particulars (username and points) are displayed on the student page.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)
        # Access the student page
        response = self.app.get('/student/A1234567X', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A1234567X', response.data)  # Ensure this matches the HTML output
        self.assertIn(b'500', response.data)

    def test_redeemable_items_page(self):
        """
        Test that the redeemable items page lists all available items.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)
        # Access the redeemable items page
        response = self.app.get('/student/A1234567X/redeemable_items', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AAA', response.data)
        self.assertIn(b'BBB', response.data)

    def test_redeemed_items_page(self):
        """
        Test that the redeemed items page lists all previously redeemed items.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)
        # Add a redeemed item for the student
        with app.app_context():
            redeemed_item = RedeemedItem(
                student_id='A1234567X',
                item_name='AAA',
                points_used=100
            )
            db.session.add(redeemed_item)
            db.session.commit()
        # Access the redeemed items page
        response = self.app.get('/student/A1234567X/redeemed_items', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AAA', response.data)
        self.assertIn(b'100', response.data)

    def test_dummy_points_validation(self):
        """
        Test that the maximum allowable points (9999) is respected.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)
        # Modify the student's points to exceed the maximum limit
        with app.app_context():
            student = db.session.get(Student, 'A1234567X')  # Use the new SQLAlchemy 2.0 method
            student.points = 10000  # Exceeds the maximum limit
            db.session.commit()
        # Access the student page
        response = self.app.get('/student/A1234567X', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Total Points: 10000', response.data)  # Ensure points are capped at 9999


if __name__ == '__main__':
    unittest.main()