import pytest
from app import app, students, redeemable_items, redeemed_items
from datetime import datetime  # Import datetime for date validation

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
    assert b'AAA' in response.data
    assert b'BBB' in response.data
    assert b'CCC' in response.data
    assert b'10' in response.data  # Points required for AAA
    assert b'200' in response.data  # Points required for BBB
    assert b'300' in response.data  # Points required for CCC

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

    # Redeem an item (e.g., AAA with ID 1, which costs 10 points)
    print(f"Attempting to redeem item: AAA (ID: 1, Cost: 10 points)")
    response = client.post('/redeem_item/1', json={'student_id': 'A1234568Y'}, follow_redirects=True)

    # Debug: Print the response from the redemption request
    print(f"Redemption response: {response.json}")

    # Check that the item was redeemed successfully
    assert response.status_code == 200
    assert response.json['success'] == True

    # Verify that the student's points were updated
    student = next((s for s in students if s['id'] == 'A1234568Y'), None)
    updated_points = response.json['points']
    print(f"Updated points for student {student['id']} ({student['name']}): {updated_points}")
    assert updated_points == initial_points - 10  # 80 - 10 = 70

    # Verify that the redeemed item was added to the redeemed_items list
    assert len(redeemed_items) == 1
    assert redeemed_items[0]['name'] == 'AAA'
    assert redeemed_items[0]['points_used'] == 10
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

    # Redeem an item (e.g., AAA with ID 1)
    client.post('/redeem_item/1', json={'student_id': 'A1234567X'}, follow_redirects=True)

    # Access the redeemed items page
    response = client.get('/student/A1234567X/redeemed_items')

    # Debug: Print the response data for inspection
    print("\nResponse data:")
    print(response.data.decode('utf-8'))

    # Check that the redeemed items page displays the correct items
    assert b'AAA' in response.data  # Verify the item name is displayed
    assert b'10' in response.data   # Verify the points used are displayed

    # Verify that the date_redeemed field contains a valid date in the format YYYY-MM-DD
    date_redeemed = None
    for item in redeemed_items:
        if item['name'] == 'AAA' and item['student_id'] == 'A1234567X':
            date_redeemed = item['date_redeemed']
            break

    assert date_redeemed is not None, "Redeemed item not found in the list"

    # Validate the date format
    try:
        redeemed_date = datetime.strptime(date_redeemed, '%Y-%m-%d')
        assert redeemed_date <= datetime.now(), "Redeemed date is in the future"
    except ValueError:
        assert False, f"Invalid date format: {date_redeemed}. Expected format: YYYY-MM-DD"