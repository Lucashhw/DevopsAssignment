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
        },
        {
            'id': 'A1234572C',
            'name': 'David Koh',
            'diploma': 'Diploma in Arts',
            'year_of_entry': 2020,
            'email': 'david.koh.2020@example.edu',
            'points': 200  # Initial Points
        }
    ])

    # Reset redeemable_items to their initial state
    redeemable_items.clear()
    redeemable_items.extend([
        {'id': 1, 'name': 'AAA', 'points_required': 100, 'quantity': 5},
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
    assert b'100' in response.data  # Points required for AAA
    assert b'200' in response.data  # Points required for BBB
    assert b'300' in response.data  # Points required for CCC

def test_redeem_item_updates_points(client):
    """
    Test that redeeming an item updates the student's points correctly.
    """
    # Simulate a student login (use Alice Wong)
    client.post('/login', data=dict(
        username='A1234569Z',  # Valid student ID (Alice Wong)
        password='student'     # Valid password
    ), follow_redirects=True)

    # Debug: Print the student's initial points
    student = next((s for s in students if s['id'] == 'A1234569Z'), None)
    initial_points = student['points']  # Alice Wong starts with 200 points
    print(f"\nInitial points for student {student['id']} ({student['name']}): {initial_points}")

    # Redeem an item (e.g., AAA with ID 1, which costs 100 points)
    print(f"Attempting to redeem item: AAA (ID: 1, Cost: 100 points)")
    response = client.post('/redeem_item/1', json={'student_id': 'A1234569Z'}, follow_redirects=True)

    # Debug: Print the response from the redemption request
    print(f"Redemption response: {response.json}")

    # Check that the item was redeemed successfully
    assert response.status_code == 200
    assert response.json['success'] == True

    # Verify that the student's points were updated
    student = next((s for s in students if s['id'] == 'A1234569Z'), None)
    updated_points = response.json['points']
    print(f"Updated points for student {student['id']} ({student['name']}): {updated_points}")
    assert updated_points == initial_points - 100  # 200 - 100 = 100

    # Verify that the redeemed item was added to the redeemed_items list
    assert len(redeemed_items) == 1
    assert redeemed_items[0]['name'] == 'AAA'
    assert redeemed_items[0]['points_used'] == 100
    assert redeemed_items[0]['student_id'] == 'A1234569Z'  # Ensure the student ID is tracked

    # Debug: Print the redeemed items list
    print(f"Redeemed items: {redeemed_items}")

def test_redeem_item_not_enough_points(client):
    """
    Test that a student cannot redeem an item if they don't have enough points.
    """
    # Simulate a student login (use Charlie Ng)
    client.post('/login', data=dict(
        username='A1234571B',  # Valid student ID (Charlie Ng)
        password='student'     # Valid password
    ), follow_redirects=True)

    # Debug: Print the student's initial points
    student = next((s for s in students if s['id'] == 'A1234571B'), None)
    initial_points = student['points']  # Charlie Ng starts with 90 points
    print(f"\nInitial points for student {student['id']} ({student['name']}): {initial_points}")

    # Attempt to redeem an item (e.g., BBB with ID 2, which costs 200 points)
    print(f"Attempting to redeem item: BBB (ID: 2, Cost: 200 points)")
    response = client.post('/redeem_item/2', json={'student_id': 'A1234571B'}, follow_redirects=True)

    # Debug: Print the response from the redemption request
    print(f"Redemption response: {response.json}")

    # Check that the redemption failed due to insufficient points
    assert response.status_code == 200
    assert response.json['success'] == False
    assert response.json['message'] == 'Not enough points'

    # Verify that the student's points were not updated
    student = next((s for s in students if s['id'] == 'A1234571B'), None)
    assert student['points'] == initial_points  # Points should remain unchanged

    # Verify that no items were added to the redeemed_items list
    assert len(redeemed_items) == 0

def test_redeem_item_out_of_stock(client):
    """
    Test that a student cannot redeem an item if it is out of stock.
    """
    # Simulate a student login (use Bob Lee)
    client.post('/login', data=dict(
        username='A1234570A',  # Valid student ID (Bob Lee)
        password='student'     # Valid password
    ), follow_redirects=True)

    # Set the item quantity to 0 (out of stock)
    item = next((i for i in redeemable_items if i['id'] == 1), None)
    item['quantity'] = 0  # AAA is now out of stock

    # Debug: Print the item's quantity
    print(f"\nItem {item['name']} (ID: {item['id']}) is out of stock (Quantity: {item['quantity']})")

    # Attempt to redeem the out-of-stock item
    print(f"Attempting to redeem item: AAA (ID: 1, Cost: 10 points)")
    response = client.post('/redeem_item/1', json={'student_id': 'A1234570A'}, follow_redirects=True)

    # Debug: Print the response from the redemption request
    print(f"Redemption response: {response.json}")

    # Check that the redemption failed due to the item being out of stock
    assert response.status_code == 200
    assert response.json['success'] == False
    assert response.json['message'] == 'Item out of stock'

    # Verify that the student's points were not updated
    student = next((s for s in students if s['id'] == 'A1234570A'), None)
    assert student['points'] == 120  # Points should remain unchanged

    # Verify that no items were added to the redeemed_items list
    assert len(redeemed_items) == 0