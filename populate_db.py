from app import app, db
from app.models import Student, RedeemableItem

# Populate the database with initial data
def populate_database():
    with app.app_context():
        # Drop all tables to ensure a clean slate
        db.drop_all()
        # Recreate all tables
        db.create_all()

        # Add students with initial passwords
        students_data = [
            {'id': 'A1234567X', 'name': 'John Tan', 'diploma': 'Diploma in IT', 'year_of_entry': 2024, 'email': 'john.tan.2024@example.edu', 'points': 50, 'password_hash': 'student'},
            {'id': 'A1234568Y', 'name': 'Sarah Lim', 'diploma': 'Diploma in Business', 'year_of_entry': 2023, 'email': 'sarah.lim.2023@example.edu', 'points': 80, 'password_hash': 'student'},
            {'id': 'A1234569Z', 'name': 'Alice Wong', 'diploma': 'Diploma in Design', 'year_of_entry': 2025, 'email': 'alice.wong.2025@example.edu', 'points': 100, 'password_hash': 'student'},
            {'id': 'A1234570A', 'name': 'Bob Lee', 'diploma': 'Diploma in Engineering', 'year_of_entry': 2022, 'email': 'bob.lee.2022@example.edu', 'points': 120, 'password_hash': 'student'},
            {'id': 'A1234571B', 'name': 'Charlie Ng', 'diploma': 'Diploma in Science', 'year_of_entry': 2021, 'email': 'charlie.ng.2021@example.edu', 'points': 90, 'password_hash': 'student'},
            {'id': 'A1234572C', 'name': 'David Koh', 'diploma': 'Diploma in Arts', 'year_of_entry': 2020, 'email': 'david.koh.2020@example.edu', 'points': 200, 'password_hash': 'student'}
        ]
        for data in students_data:
            student = Student(**data)
            db.session.add(student)

        # Add redeemable items
        items_data = [
            {'name': 'AAA', 'points_required': 100, 'quantity': 5},
            {'name': 'BBB', 'points_required': 200, 'quantity': 3},
            {'name': 'CCC', 'points_required': 300, 'quantity': 2},
        ]
        for data in items_data:
            item = RedeemableItem(**data)
            db.session.add(item)

        # Commit changes to the database
        db.session.commit()

if __name__ == '__main__':
    populate_database()