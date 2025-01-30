from app import app, db
from app.models import Student, RedeemableItem, RedeemedItem

with app.app_context():
    # Drop all tables to ensure a clean slate
    db.drop_all()
    # Recreate all tables
    db.create_all()

    # Add students
    students_data = [
        {'id': 'A1234567X', 'name': 'John Tan', 'diploma': 'Diploma in IT', 'year_of_entry': 2024, 'email': 'john.tan.2024@example.edu', 'points': 50},
        {'id': 'A1234568Y', 'name': 'Sarah Lim', 'diploma': 'Diploma in Business', 'year_of_entry': 2023, 'email': 'sarah.lim.2023@example.edu', 'points': 80},
        {'id': 'A1234569Z', 'name': 'Alice Wong', 'diploma': 'Diploma in Design', 'year_of_entry': 2025, 'email': 'alice.wong.2025@example.edu', 'points': 100},
        {'id': 'A1234570A', 'name': 'Bob Lee', 'diploma': 'Diploma in Engineering', 'year_of_entry': 2022, 'email': 'bob.lee.2022@example.edu', 'points': 120},
        {'id': 'A1234571B', 'name': 'Charlie Ng', 'diploma': 'Diploma in Science', 'year_of_entry': 2021, 'email': 'charlie.ng.2021@example.edu', 'points': 90},
        {'id': 'A1234572C', 'name': 'David Koh', 'diploma': 'Diploma in Arts', 'year_of_entry': 2020, 'email': 'david.koh.2020@example.edu', 'points': 200}
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

    # Optionally add some dummy redeemed items if needed for testing
    # redeemed_items_data = [
    #     {'student_id': 'A1234567X', 'item_name': 'AAA', 'points_used': 100},
    #     {'student_id': 'A1234568Y', 'item_name': 'BBB', 'points_used': 200},
    # ]

    # for data in redeemed_items_data:
    #     redeemed_item = RedeemedItem(
    #         student_id=data['student_id'],
    #         item_name=data['item_name'],
    #         points_used=data['points_used']
    #     )
    #     db.session.add(redeemed_item)

    db.session.commit()