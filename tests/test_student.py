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
            'points': 80
        }
    ])

    # Reset redeemable_items to their initial state
    redeemable_items.clear()
    redeemable_items.extend([
        {'id': 1, 'name': 'Book', 'points_required': 100, 'quantity': 10},
        {'id': 2, 'name': 'Pen', 'points_required': 50, 'quantity': 20},
    ])

    # Reset redeemed_items to their initial state
    redeemed_items.clear()

    # Debug: Print the state after resetting
    print("After reset:")
    print("Students:", students)
    print("Redeemable Items:", redeemable_items)
    print("Redeemed Items:", redeemed_items)

def test_student_login(client):
    """
    Test that a student can log in successfully and is redirected to the student page.
    """
    # Simulate a student login
    response = client.post('/login', data=dict(
        username='A1234567X',  # Valid student ID
        password='student'     # Valid password
    ), follow_redirects=True)

    # Check that the login was successful and the student is redirected to the student page
    assert response.status_code == 200
    assert b'Student Page' in response.data

def test_student_page_displays_user_info(client):
    """
    Test that the student page displays the correct user information.
    """
    # Simulate a student login
    client.post('/login', data=dict(
        username='A1234568Y',  # Valid student ID
        password='student'     # Valid password
    ), follow_redirects=True)

    # Access the student page
    response = client.get('/student/A1234568Y')

    # Debug: Print the response data
    print("\nResponse data:")
    print(response.data.decode('utf-8'))  # Decode bytes to string for readability

    # Check that the student page displays the correct user information
    assert b'A1234568Y' in response.data  # Check for the username
    assert b'80' in response.data  # Check for the total points

def test_redeemable_items_page(client):
    """
    Test that the redeemable items page displays the correct items.
    """
    # Simulate a student login
    client.post('/login', data=dict(
        username='A1234567X',  # Valid student ID
        password='student'     # Valid password
    ), follow_redirects=True)

    # Access the redeemable items page
    response = client.get('/student/A1234567X/redeemable_items')

    # Check that the redeemable items page displays the correct items
    assert b'Book' in response.data
    assert b'Pen' in response.data
    assert b'100' in response.data  # Points required for Book
    assert b'50' in response.data   # Points required for Pen

def test_redeem_item_updates_points(client):
    """
    Test that redeeming an item updates the student's points correctly.
    """
    # Simulate a student login
    client.post('/login', data=dict(
        username='A1234568Y',  # Valid student ID (Sarah Lim)
        password='student'     # Valid password
    ), follow_redirects=True)

    # Debug: Print the student's initial points
    student = next((s for s in students if s['id'] == 'A1234568Y'), None)
    initial_points = student['points']  # Sarah Lim starts with 80 points
    print(f"\nInitial points for student {student['id']} ({student['name']}): {initial_points}")

    # Redeem an item (e.g., Pen with ID 2, which costs 50 points)
    print(f"Attempting to redeem item: Pen (ID: 2, Cost: 50 points)")
    response = client.post('/redeem_item/2', json={'student_id': 'A1234568Y'}, follow_redirects=True)

    # Debug: Print the response from the redemption request
    print(f"Redemption response: {response.json}")

    # Check that the item was redeemed successfully
    assert response.status_code == 200
    assert response.json['success'] == True

    # Verify that the student's points were updated
    student = next((s for s in students if s['id'] == 'A1234568Y'), None)
    updated_points = response.json['points']
    print(f"Updated points for student {student['id']} ({student['name']}): {updated_points}")
    assert updated_points == initial_points - 50  # 80 - 50 = 30

    # Verify that the redeemed item was added to the redeemed_items list
    assert len(redeemed_items) == 1
    assert redeemed_items[0]['name'] == 'Pen'
    assert redeemed_items[0]['points_used'] == 50
    assert redeemed_items[0]['student_id'] == 'A1234568Y'  # Ensure the student ID is tracked

    # Debug: Print the redeemed items list
    print(f"Redeemed items: {redeemed_items}")

def test_redeemed_items_page(client):
    """
    Test that the redeemed items page displays the correct items after redemption.
    """
    # Set the student's points to 50 explicitly
    student = next((s for s in students if s['id'] == 'A1234567X'), None)
    student['points'] = 50  # Explicitly set points

    # Simulate a student login
    client.post('/login', data=dict(
        username='A1234567X',  # Valid student ID
        password='student'     # Valid password
    ), follow_redirects=True)

    # Redeem an item (e.g., Pen with ID 2)
    client.post('/redeem_item/2', json={'student_id': 'A1234567X'}, follow_redirects=True)

    # Access the redeemed items page
    response = client.get('/student/A1234567X/redeemed_items')

    # Check that the redeemed items page displays the correct items
    assert b'Pen' in response.data
    assert b'50' in response.data  # Points used for Pen
    assert b'2023-10-01' in response.data  # Date redeemed