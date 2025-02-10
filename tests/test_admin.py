import unittest
from app import app, db
from app.models import Student, RedeemableItem
from io import BytesIO

class TestAdminProcess(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login_as_admin(self):
        """Helper function to log in as admin."""
        return self.client.post('/login', data=dict(
            username='admin',
            password='admin'
        ), follow_redirects=True)

    def test_create_student(self):
        """Test creating a new student account."""
        self.login_as_admin()
        response = self.client.post('/admin/create_student', data=dict(
            student_id='A1234500K',
            student_name='Joseph Wong',
            diploma='Diploma in Design',
            year_of_entry=2025,
            email='joseph.wong.2025@example.edu',
            student_points=100
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            student = Student.query.filter_by(id='A1234500K').first()
            self.assertIsNotNone(student)
            self.assertEqual(student.name, 'Joseph Wong')

    def test_csv_upload_success(self):
        """Test uploading a valid CSV file."""
        self.login_as_admin()
        csv_data = "Student ID,Student Name,Diploma,Year of Entry,Email,Student Points\nA1234500K,Joseph Wong,Diploma in Design,2025,joseph.wong.2025@example.edu,100"
        csv_file = BytesIO(csv_data.encode('utf-8'))
        response = self.client.post('/admin/upload_csv', data={
            'file': (csv_file, 'test.csv')
        }, content_type='multipart/form-data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            student = Student.query.filter_by(id='A1234500K').first()
            self.assertIsNotNone(student)
            self.assertEqual(student.name, 'Joseph Wong')

    def test_csv_upload_invalid_file(self):
        """Test uploading an invalid CSV file."""
        self.login_as_admin()
        response = self.client.post('/admin/upload_csv', data={
            'file': (BytesIO(b'Invalid file content'), 'test.txt')
        }, content_type='multipart/form-data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid file type', response.data)

    def test_edit_student(self):
        """Test modifying a student account."""
        self.login_as_admin()
        self.client.post('/admin/create_student', data=dict(
            student_id='A1234567X',
            student_name='John Tan',
            diploma='Diploma in IT',
            year_of_entry=2024,
            email='john.tan.2024@example.edu',
            student_points=50
        ), follow_redirects=True)
        response = self.client.post('/admin/update_student/A1234567X', data=dict(
            student_name='John Updated',
            diploma='Diploma in Business',
            year_of_entry=2023,
            email='john.updated@example.edu',
            student_points=60
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            student = db.session.get(Student, 'A1234567X')
            self.assertEqual(student.name, 'John Updated')

    def test_delete_student(self):
        """Test deleting a student account."""
        self.login_as_admin()
        self.client.post('/admin/create_student', data=dict(
            student_id='A1234567X',
            student_name='John Tan',
            diploma='Diploma in IT',
            year_of_entry=2024,
            email='john.tan.2024@example.edu',
            student_points=50
        ), follow_redirects=True)
        response = self.client.get('/admin/delete_student/A1234567X', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            student = db.session.get(Student, 'A1234567X')
            self.assertIsNone(student)

    def test_list_students(self):
        """Test listing all student accounts."""
        self.login_as_admin()
        self.client.post('/admin/create_student', data=dict(
            student_id='A1234567X',
            student_name='John Tan',
            diploma='Diploma in IT',
            year_of_entry=2024,
            email='john.tan.2024@example.edu',
            student_points=50
        ), follow_redirects=True)
        response = self.client.get('/admin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Tan', response.data)

    def test_search_student_by_id(self):
        """Test searching for a student by ID."""
        self.login_as_admin()
        self.client.post('/admin/create_student', data=dict(
            student_id='A1234567X',
            student_name='John Tan',
            diploma='Diploma in IT',
            year_of_entry=2024,
            email='john.tan.2024@example.edu',
            student_points=50
        ), follow_redirects=True)
        response = self.client.get('/admin/search_student?query=A1234567X', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Tan', response.data)

    def test_create_redeemable_item(self):
        """Test creating a new redeemable item."""
        self.login_as_admin()
        response = self.client.post('/admin/create_redeemable_item', data=dict(
            name='AAA',
            points_required=100,
            quantity=5
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            item = RedeemableItem.query.filter_by(name='AAA').first()
            self.assertIsNotNone(item)
            self.assertEqual(item.points_required, 100)

if __name__ == '__main__':
    unittest.main()