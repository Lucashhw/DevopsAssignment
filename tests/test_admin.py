import io
import pytest
from app import app, students, redeemable_items, redeemed_items

@pytest.fixture
def client():
    # Create a test client
    app.testing = True
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_state():
    """
    Reset the application state before each test.
    """
    global students, redeemable_items, redeemed_items

    # Debug: Print the state before resetting
    print("\nBefore reset:")
    print("Students:", students)
    print("Redeemable Items:", redeemable_items)
    print("Redeemed Items:", redeemed_items)

    # Reset students to their initial state
    students.clear()
    students.extend([
        {
            'id': 'A1234567X',
            'name': 'John Tan',
            'diploma': 'Diploma in IT',
            'year_of_entry': 2024,
            'email': 'john.tan.2024@example.edu',
            'points': 50  # Initial points
        },
        {
            'id': 'A1234568Y',
            'name': 'Sarah Lim',
            'diploma': 'Diploma in Business',
            'year_of_entry': 2023,
            'email': 'sarah.lim.2023@example.edu',
            'points': 80  # Initial points
        },
        {
            'id': 'A1234569Z',
            'name': 'Alice Wong',
            'diploma': 'Diploma in Design',
            'year_of_entry': 2025,
            'email': 'alice.wong.2025@example.edu',
            'points': 100  # Initial points
        },
        {
            'id': 'A1234570A',
            'name': 'Bob Lee',
            'diploma': 'Diploma in Engineering',
            'year_of_entry': 2022,
            'email': 'bob.lee.2022@example.edu',
            'points': 120  # Initial points
        },
        {
            'id': 'A1234571B',
            'name': 'Charlie Ng',
            'diploma': 'Diploma in Science',
            'year_of_entry': 2021,
            'email': 'charlie.ng.2021@example.edu',
            'points': 90  # Initial points
        }
    ])

    # Reset redeemable_items to their initial state
    redeemable_items.clear()
    redeemable_items.extend([
        {'id': 1, 'name': 'AAA', 'points_required': 10, 'quantity': 5},
        {'id': 2, 'name': 'BBB', 'points_required': 200, 'quantity': 3},
        {'id': 3, 'name': 'CCC', 'points_required': 300, 'quantity': 2},
    ])

    # Reset redeemed_items to their initial state
    redeemed_items.clear()

    # Debug: Print the state after resetting
    print("After reset:")
    print("Students:", students)
    print("Redeemable Items:", redeemable_items)
    print("Redeemed Items:", redeemed_items)

    
def test_create_student(client):
    # Test creating a new student with all fields
    response = client.post('/admin/create_student', data=dict(
        student_id='A1234500K',
        student_name='Joseph Wong',
        diploma='Diploma in Design',
        year_of_entry=2025,
        email='joseph.wong.2025@example.edu',
        student_points=100
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Joseph Wong' in response.data  # Check if the new student is listed
    assert b'Diploma in Design' in response.data  # Check if diploma is listed
    assert b'2025' in response.data  # Check if year of entry is listed
    assert b'joseph.wong.2025@example.edu' in response.data  # Check if email is listed

def test_edit_student(client):
    # Test editing a student's details with all fields
    response = client.post('/admin/update_student/A1234568Y', data=dict(
        student_name='Sarah Lim Updated',
        diploma='Diploma in Marketing',
        year_of_entry=2022,
        email='sarah.lim.2022@example.edu',
        student_points=90
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Sarah Lim Updated' in response.data  # Check if the student's name is updated
    assert b'Diploma in Marketing' in response.data  # Check if diploma is updated
    assert b'2022' in response.data  # Check if year of entry is updated
    assert b'sarah.lim.2022@example.edu' in response.data  # Check if email is updated
    assert b'90' in response.data  # Check if the student's points are updated

def test_delete_student(client):
    # Test deleting a student
    response = client.get('/admin/delete_student/A1234567X', follow_redirects=True)
    assert response.status_code == 200
    assert b'John Tan' not in response.data  # Check if the student is removed

def test_search_student(client):
    # Test searching for a student by name
    response = client.get('/admin/search_student?query=Sarah', follow_redirects=True)
    assert response.status_code == 200
    assert b'Sarah Lim' in response.data  # Check if the search result is correct

def test_csv_upload_success(client):
    # Test successful CSV file upload
    csv_data = "Student ID,Student Name,Diploma,Year of Entry,Email,Student Points\nA1234567X,John Tan,Diploma in IT,2021,john.tan@example.com,100"
    csv_file = io.BytesIO(csv_data.encode('utf-8'))

    # Follow the redirect to the Admin Page
    response = client.post('/admin/upload_csv', data={
        'file': (csv_file, 'test.csv')
    }, content_type='multipart/form-data', follow_redirects=True)

    assert response.status_code == 200  # Check for successful response
    assert b'CSV file uploaded successfully' in response.data  # Check for flash message

def test_csv_upload_invalid_file(client):
    # Test invalid file type
    response = client.post('/admin/upload_csv', data={
        'file': (io.BytesIO(b'Invalid file content'), 'test.txt')
    }, content_type='multipart/form-data', follow_redirects=True)

    assert response.status_code == 200  # Check for successful response
    assert b'Invalid file type' in response.data  # Check for flash message

def test_csv_upload_empty_file(client):
    # Test empty file
    response = client.post('/admin/upload_csv', data={
        'file': (io.BytesIO(b''), 'empty.csv')
    }, content_type='multipart/form-data', follow_redirects=True)

    assert response.status_code == 200  # Check for successful response
    assert b'Error processing CSV file' in response.data  # Check for flash message