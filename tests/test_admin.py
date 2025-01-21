import unittest
from app import app, students  # Import the students list

class TestAdminPage(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Propagate exceptions to the test client
        self.app.testing = True
        # Reset the students list to its initial state
        global students
        students = [
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
        ]

    def test_create_student(self):
        # Test creating a new student with all fields
        response = self.app.post('/admin/create_student', data=dict(
            student_id='A1234569Z',
            student_name='Alice Wong',
            diploma='Diploma in Design',
            year_of_entry=2025,
            email='alice.wong.2025@example.edu',
            student_points=100
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice Wong', response.data)  # Check if the new student is listed
        self.assertIn(b'Diploma in Design', response.data)  # Check if diploma is listed
        self.assertIn(b'2025', response.data)  # Check if year of entry is listed
        self.assertIn(b'alice.wong.2025@example.edu', response.data)  # Check if email is listed

    def test_edit_student(self):
        # Test editing a student's details with all fields
        response = self.app.post('/admin/update_student/A1234568Y', data=dict(
            student_name='Sarah Lim Updated',
            diploma='Diploma in Marketing',
            year_of_entry=2022,
            email='sarah.lim.2022@example.edu',
            student_points=90
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sarah Lim Updated', response.data)  # Check if the student's name is updated
        self.assertIn(b'Diploma in Marketing', response.data)  # Check if diploma is updated
        self.assertIn(b'2022', response.data)  # Check if year of entry is updated
        self.assertIn(b'sarah.lim.2022@example.edu', response.data)  # Check if email is updated
        self.assertIn(b'90', response.data)  # Check if the student's points are updated

    def test_delete_student(self):
        # Test deleting a student
        response = self.app.get('/admin/delete_student/A1234567X', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'John Tan', response.data)  # Check if the student is removed

    def test_search_student(self):
        # Test searching for a student by name
        response = self.app.get('/admin/search_student?query=Sarah', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sarah Lim', response.data)  # Check if the search result is correct

if __name__ == '__main__':
    unittest.main()