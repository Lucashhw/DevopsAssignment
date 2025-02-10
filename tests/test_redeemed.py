import unittest
from app import app, db
from app.models import Student, RedeemableItem, RedeemedItem

class TestRedeemedPageProcess(unittest.TestCase):
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
                {'name': 'BBB', 'points_required': 200, 'quantity': 3},
                {'name': 'CCC', 'points_required': 600, 'quantity': 2}
            ]
            for data in items_data:
                item = RedeemableItem(**data)
                db.session.add(item)
            # Add redeemed items for the student
            redeemed_items_data = [
                {'student_id': 'A1234567X', 'item_name': 'AAA', 'points_used': 100},
                {'student_id': 'A1234567X', 'item_name': 'BBB', 'points_used': 200}
            ]
            for data in redeemed_items_data:
                redeemed_item = RedeemedItem(**data)
                db.session.add(redeemed_item)
            db.session.commit()

    def tearDown(self):
        """
        Clean up the test environment by dropping all tables.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_redeemed_items_page_with_redeemed_items(self):
        """
        Test that the redeemed items page lists all previously redeemed items for the logged-in student.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)

        # Access the redeemed items page
        response = self.app.get('/student/A1234567X/redeemed_items', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the redeemed items are displayed
        self.assertIn(b'AAA', response.data)
        self.assertIn(b'BBB', response.data)
        self.assertNotIn(b'CCC', response.data)  # CCC was not redeemed

    def test_redeemed_items_page_no_redeemed_items(self):
        """
        Test that the redeemed items page displays a message when no items have been redeemed.
        """
        # Add a new student with no redeemed items
        with app.app_context():
            student = Student(
                id='A1234568Y',
                name='Sarah Lim',
                diploma='Diploma in Business',
                year_of_entry=2023,
                email='sarah.lim.2023@example.edu',
                points=80,
                password_hash='student'
            )
            db.session.add(student)
            db.session.commit()

        # Log in as the new student
        self.app.post('/login', data=dict(
            username='A1234568Y',
            password='student'
        ), follow_redirects=True)

        # Access the redeemed items page
        response = self.app.get('/student/A1234568Y/redeemed_items', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that a message indicating no redeemed items is displayed
        self.assertIn(b'No items redeemed yet.', response.data)

    def test_unauthorized_access_to_redeemed_items(self):
        """
        Test that unauthorized users cannot access another student's redeemed items page.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)

        # Attempt to access another student's redeemed items page
        response = self.app.get('/student/A1234568Y/redeemed_items', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the user is redirected to the login page
        self.assertIn(b'Login', response.data)

    def test_redeemed_items_with_missing_student_record(self):
        """
        Test that the system handles gracefully when a redeemed item's associated student record is missing.
        """
        # Add a redeemed item with a non-existent student ID
        with app.app_context():
            redeemed_item = RedeemedItem(
                student_id='A1234569Z',  # Non-existent student
                item_name='AAA',
                points_used=100
            )
            db.session.add(redeemed_item)
            db.session.commit()

        # Log in as a valid student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)

        # Access the redeemed items page
        response = self.app.get('/student/A1234567X/redeemed_items', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Ensure the page does not crash and only displays valid redeemed items
        self.assertIn(b'AAA', response.data)  # Only valid redeemed items are shown
        self.assertNotIn(b'A1234569Z', response.data)  # Missing student ID is not displayed

if __name__ == '__main__':
    unittest.main()