import io
import pytest
from app import app, db
from app.models import Student, RedeemableItem

@pytest.fixture
def client():
    # Create a test client using an in-memory SQLite database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection during tests
    with app.app_context():
        db.create_all()  # Create all tables
        yield app.test_client()
        db.session.remove()  # Clean up session
        db.drop_all()  # Drop all tables

@pytest.fixture(autouse=True)
def populate_db(client):
    """
    Populate the database with initial data before each test.
    """
    with app.app_context():
        # Add students
        students_data = [
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
            }
        ]
        for data in students_data:
            student = Student(**data)
            db.session.add(student)

        # Add redeemable items
        items_data = [
            {'name': 'AAA', 'points_required': 100, 'quantity': 5},
            {'name': 'BBB', 'points_required': 200, 'quantity': 3},
            {'name': 'CCC', 'points_required': 300, 'quantity': 2}
        ]
        for data in items_data:
            item = RedeemableItem(**data)
            db.session.add(item)

        db.session.commit()

# Test Admin Login Functionality
def test_login_as_admin(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Student List' in response.data  # Check if the admin page is shown

# Test Create New Student Accounts
def test_create_student(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    response = client.post('/admin/create_student', data=dict(
        student_id='A1234500K',
        student_name='Joseph Wong',
        diploma='Diploma in Design',
        year_of_entry=2025,
        email='joseph.wong.2025@example.edu',
        student_points=100
    ), follow_redirects=True)
    
    assert response.status_code == 200

    with app.app_context():
        student = Student.query.filter_by(id='A1234500K').first()
        assert student is not None
        assert student.name == 'Joseph Wong'
        assert student.diploma == 'Diploma in Design'
        assert student.year_of_entry == 2025
        assert student.email == 'joseph.wong.2025@example.edu'
        assert student.points == 100

# Test Modify Student Accounts
def test_edit_student(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    response = client.post('/admin/update_student/A1234568Y', data=dict(
        student_name='Sarah Lim Updated',
        diploma='Diploma in Marketing',
        year_of_entry=2022,
        email='sarah.lim.2022@example.edu',
        student_points=90
    ), follow_redirects=True)
    
    assert response.status_code == 200

    with app.app_context():
        student = Student.query.get('A1234568Y')
        assert student.name == 'Sarah Lim Updated'
        assert student.diploma == 'Diploma in Marketing'
        assert student.year_of_entry == 2022
        assert student.email == 'sarah.lim.2022@example.edu'
        assert student.points == 90

# Test Delete Student Accounts
def test_delete_student(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    response = client.get('/admin/delete_student/A1234567X', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        student = Student.query.get('A1234567X')
        assert student is None  # Check if the student is removed

# Test List All Student Accounts
def test_list_all_students(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    response = client.get('/admin', follow_redirects=True)
    assert response.status_code == 200

    # Decode the response data to a string and check for the presence of student names
    response_data = response.data.decode('utf-8')
    assert 'John Tan' in response_data  # Check if John Tan is listed
    assert 'Sarah Lim' in response_data  # Check if Sarah Lim is listed

# Test Search for Student Account by ID
def test_search_student_by_id(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    response = client.get('/admin/search_student?query=A1234567X', follow_redirects=True)
    assert response.status_code == 200

    # Decode the response data to a string and check for the presence of 'John Tan'
    response_data = response.data.decode('utf-8')
    assert 'John Tan' in response_data  # Check if the search result is correct
    assert 'Sarah Lim' not in response_data  # Check if other students are excluded

# Test Search for Student Account by Name
def test_search_student_by_name(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    response = client.get('/admin/search_student?query=Sarah', follow_redirects=True)
    assert response.status_code == 200

    # Decode the response data to a string and check for the presence of 'Sarah Lim'
    response_data = response.data.decode('utf-8')
    assert 'Sarah Lim' in response_data  # Check if the search result is correct
    assert 'John Tan' not in response_data  # Check if other students are excluded

# Test CSV Upload Success
def test_csv_upload_success(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    csv_data = "Student ID,Student Name,Diploma,Year of Entry,Email,Student Points\nA1234500K,Joseph Wong,Diploma in Design,2025,joseph.wong.2025@example.edu,100"
    csv_file = io.BytesIO(csv_data.encode('utf-8'))
    # Follow the redirect to the Admin Page
    response = client.post('/admin/upload_csv', data={
        'file': (csv_file, 'test.csv')
    }, content_type='multipart/form-data', follow_redirects=True)
    
    assert response.status_code == 200  # Check for successful response

    # Decode the response data to a string and check for the presence of the flash message
    response_data = response.data.decode('utf-8')
    assert 'CSV file uploaded successfully.' in response_data  # Check for flash message

    with app.app_context():
        student = Student.query.filter_by(id='A1234500K').first()
        assert student is not None
        assert student.name == 'Joseph Wong'
        assert student.diploma == 'Diploma in Design'
        assert student.year_of_entry == 2025
        assert student.email == 'joseph.wong.2025@example.edu'
        assert student.points == 100

# Test CSV Upload Invalid File Type
def test_csv_upload_invalid_file(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    # Test invalid file type
    response = client.post('/admin/upload_csv', data={
        'file': (io.BytesIO(b'Invalid file content'), 'test.txt')
    }, content_type='multipart/form-data', follow_redirects=True)
    
    assert response.status_code == 200  # Check for successful response

    # Decode the response data to a string and check for the presence of the flash message
    response_data = response.data.decode('utf-8')
    assert 'Invalid file type' in response_data  # Check for flash message

# Test CSV Upload Empty File
def test_csv_upload_empty_file(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    # Test empty file
    response = client.post('/admin/upload_csv', data={
        'file': (io.BytesIO(b''), 'empty.csv')
    }, content_type='multipart/form-data', follow_redirects=True)
    
    assert response.status_code == 200  # Check for successful response

    # Decode the response data to a string and check for the presence of the flash message
    response_data = response.data.decode('utf-8')
    assert 'Error processing CSV file' in response_data  # Check for flash message

# Test Create, Modify, and Delete Redeemable Items
def test_create_modify_delete_redeemable_item(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    # Test creating a new redeemable item
    response = client.post('/admin/create_redeemable_item', data=dict(
        name='DDD',
        points_required=150,
        quantity=4
    ), follow_redirects=True)
    
    assert response.status_code == 200

    with app.app_context():
        item = RedeemableItem.query.filter_by(name='DDD').first()
        assert item is not None
        assert item.points_required == 150
        assert item.quantity == 4

    # Test modifying the redeemable item
    response = client.post('/admin/update_redeemable_item/{}'.format(item.id), data=dict(
        name='DDD Updated',
        points_required=200,
        quantity=5
    ), follow_redirects=True)
    
    assert response.status_code == 200

    with app.app_context():
        updated_item = RedeemableItem.query.get(item.id)
        assert updated_item.name == 'DDD Updated'
        assert updated_item.points_required == 200
        assert updated_item.quantity == 5

    # Test deleting the redeemable item
    response = client.get('/admin/delete_redeemable_item/{}'.format(updated_item.id), follow_redirects=True)
    
    assert response.status_code == 200

    with app.app_context():
        deleted_item = RedeemableItem.query.get(updated_item.id)
        assert deleted_item is None  # Check if the item is removed