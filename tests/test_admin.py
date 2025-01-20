import unittest
from app import app, students  # Import the students list

class TestAdminPage(unittest.TestCase):
    def setUp(self):
        
        # Create a test client
        self.app = app.test_client()
        # Propagate exceptions to the test client
        self.app.testing = True

    def test_create_student(self):
        # Test creating a new student
        response = self.app.post('/admin/create_student', data=dict(
            student_id='A1234569Z',
            student_name='Alice Wong',
            student_points=100
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice Wong', response.data)  # Check if the new student is listed


    def test_edit_student(self):
        # Test editing a student's details
            response = self.app.post('/admin/update_student/A1234568Y', data=dict(
                student_name='Sarah Lim',
                student_points=90
            ), follow_redirects=True)



            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sarah Lim', response.data)  # Check if the student's name is updated
            self.assertIn(b'90', response.data)  # Check if the student's points are updated

    
    def test_delete_student(self):
        # Test deleting a student
        response = self.app.get('/admin/delete_student/A1234567X', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'John Tan', response.data)  # Check if the student is removed



    def test_search_student(self):
        # Test searching for a student
        response = self.app.get('/admin/search_student?query=Sarah', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sarah Lim', response.data)  # Check if the search result is correct
    
    



if __name__ == '__main__':
    unittest.main()