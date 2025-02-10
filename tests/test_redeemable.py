import unittest
from app import app, db
from app.models import Student, RedeemableItem, RedeemedItem


class TestRedeemablePageProcess(unittest.TestCase):
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
                {'name': 'CCC', 'points_required': 600, 'quantity': 2}  # Item with points > student's points
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
            db.drop_all()

    def test_display_redeemable_items(self):
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
        self.assertIn(b'CCC', response.data)

    def test_redeem_item_success(self):
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)
        
        # Redeem an item (BBB, 200 points)
        with app.app_context():
            # Fetch the student and the item to be redeemed
            student = db.session.get(Student, 'A1234567X')
            initial_points = student.points
            
            # Fetch the item "BBB" from the database
            item = RedeemableItem.query.filter_by(name='BBB').first()
            self.assertIsNotNone(item, "Item 'BBB' not found in the database")
            
            # Ensure the student has enough points to redeem the item
            self.assertGreaterEqual(student.points, item.points_required, "Student does not have enough points to redeem the item")
            
            # Simulate redemption
            response = self.app.post(f'/redeem_item/{item.id}', json={
                'student_id': 'A1234567X'
            }, follow_redirects=True)
            
            # Check response
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])
            self.assertEqual(response.json['points'], initial_points - item.points_required)
            
            # Refresh the item object from the database
            updated_item = db.session.get(RedeemableItem, item.id)
            
            # Verify database updates
            student = db.session.get(Student, 'A1234567X')
            self.assertEqual(student.points, initial_points - item.points_required)
            
            # Verify the redeemed item is recorded in the database
            redeemed_item = RedeemedItem.query.filter_by(student_id='A1234567X', item_name='BBB').first()
            self.assertIsNotNone(redeemed_item, "Redeemed item 'BBB' not found in the database")
            self.assertEqual(redeemed_item.points_used, item.points_required)
            
            # Verify item quantity is decremented
            self.assertEqual(updated_item.quantity, item.quantity)

    def test_redeem_item_insufficient_points(self):
        """
        Test that a student cannot redeem an item if they do not have sufficient points.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)

        # Attempt to redeem an item (CCC, 600 points) with insufficient points
        with app.app_context():
            item = RedeemableItem.query.filter_by(name='CCC').first()

            # Simulate redemption
            response = self.app.post(f'/redeem_item/{item.id}', json={
                'student_id': 'A1234567X'
            }, follow_redirects=True)

            # Check response
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.json['success'])
            self.assertIn('Not enough points', response.json['message'])

            # Verify no changes in the database
            student = db.session.get(Student, 'A1234567X')
            self.assertEqual(student.points, 500)  # Points remain unchanged
            redeemed_item = RedeemedItem.query.filter_by(student_id='A1234567X', item_name='CCC').first()
            self.assertIsNone(redeemed_item)

    def test_redeem_item_out_of_stock(self):
        """
        Test that a student cannot redeem an item if it is out of stock.
        """
        # Log in as a student
        self.app.post('/login', data=dict(
            username='A1234567X',
            password='student'
        ), follow_redirects=True)

        # Set an item's quantity to 0
        with app.app_context():
            item = RedeemableItem.query.filter_by(name='AAA').first()
            item.quantity = 0
            db.session.commit()

            # Attempt to redeem the out-of-stock item
            response = self.app.post(f'/redeem_item/{item.id}', json={
                'student_id': 'A1234567X'
            }, follow_redirects=True)

            # Check response
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.json['success'])
            self.assertIn('Item out of stock', response.json['message'])

            # Verify no changes in the database
            student = db.session.get(Student, 'A1234567X')
            self.assertEqual(student.points, 500)  # Points remain unchanged
            redeemed_item = RedeemedItem.query.filter_by(student_id='A1234567X', item_name='AAA').first()
            self.assertIsNone(redeemed_item)


if __name__ == '__main__':
    unittest.main()