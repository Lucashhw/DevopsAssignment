from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from app import app
import csv
from io import TextIOWrapper
from datetime import datetime  # Import the datetime module
from copy import deepcopy

# Dummy user data for testing
users = {
    'admin': 'admin',
    'A1234567X': 'student',  # Student John Tan
    'A1234568Y': 'student',  # Student Sarah Lim
    'A1234569Z': 'student',  # Student Alice Wong
    'A1234570A': 'student',  # Student Bob Lee
    'A1234571B': 'student',  # Student Charlie Ng

}

# Dummy student data for testing (replace with database later)
students = [
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
]

# Dummy redeemable items with quantity
redeemable_items = [
    {'id': 1, 'name': 'AAA', 'points_required': 10, 'quantity': 5},
    {'id': 2, 'name': 'BBB', 'points_required': 200, 'quantity': 3},
    {'id': 3, 'name': 'CCC', 'points_required': 300, 'quantity': 2},
]

# Dummy redeemed items for testing (replace with database later)
redeemed_items = []

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Debug: Print the student's points before login
    student = next((s for s in students if s['id'] == username), None)
    if student:
        print(f"Before login: Student points = {student['points']}")  # Debug statement
        print(f"Before login: Student username = {student['id']}")  # Debug statement

    # Check if username and password are provided
    if not username or not password:
        return render_template('login.html', error="Invalid username or password")

    # Check if username exists in the users dictionary
    if username not in users:
        return render_template('login.html', error="Invalid username")  # Specific error for invalid username

    # Check if the password matches
    if users[username] != password:
        return render_template('login.html', error="Invalid password")  # Specific error for invalid password

    # If username and password are valid
    if username == 'admin':
        return redirect(url_for('admin_page'))  # Redirect admin to the admin page
    else:
        # Find the student by username (replace with database query later)
        student = next((s for s in students if s['id'] == username), None)
        if student:
            # Debug: Print the student's points after login
            print(f"After login: Student points = {student['points']}")  # Debug statement
            print(f"After login: Student username = {student['id']}")  # Debug statement
            return redirect(url_for('student_page', student_id=student['id']))  # Redirect student to the student page
        else:
            return render_template('login.html', error="Student not found")  # Error if student ID is not in the students list

@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    if request.method == 'POST':
        email = request.form['email']
        # Add logic to handle password recovery (e.g., send email)
        return render_template('recover_password.html', message="Password recovery instructions sent to your email.")
    return render_template('recover_password.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html', students=students, redeemable_items=redeemable_items)

@app.route('/admin/create_student', methods=['POST'])
def create_student():
    student_id = request.form['student_id']
    student_name = request.form['student_name']
    diploma = request.form['diploma']
    year_of_entry = int(request.form['year_of_entry'])
    email = request.form['email']
    student_points = int(request.form['student_points'])
    
    # Add the new student to the list
    students.append({
        'id': student_id,
        'name': student_name,
        'diploma': diploma,
        'year_of_entry': year_of_entry,
        'email': email,
        'points': student_points
    })
    
    return redirect(url_for('admin_page'))

@app.route('/admin/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('admin_page'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin_page'))

    if file and file.filename.endswith('.csv'):
        try:
            csv_data = csv.reader(TextIOWrapper(file, 'utf-8'))
            next(csv_data)  # Skip header row

            has_invalid_rows = False  # Flag to track invalid rows

            for row in csv_data:
                if len(row) == 6:
                    student_id, student_name, diploma, year_of_entry, email, student_points = row
                    # Check if all fields are non-empty
                    if student_id and student_name and diploma and year_of_entry and email and student_points:
                        students.append({
                            'id': student_id,
                            'name': student_name,
                            'diploma': diploma,
                            'year_of_entry': int(year_of_entry),
                            'email': email,
                            'points': int(student_points)
                        })
                    else:
                        has_invalid_rows = True  # Mark as invalid
                else:
                    has_invalid_rows = True  # Mark as invalid

            # Check if there are any invalid rows
            if has_invalid_rows:
                flash('Invalid CSV file. Please ensure all rows have the correct format.', 'error')
            else:
                flash('CSV file uploaded successfully.', 'success')
        except Exception as e:
            flash(f'Error processing CSV file: {str(e)}', 'error')
    else:
        flash('Invalid file type. Please upload a CSV file.', 'error')

    return redirect(url_for('admin_page'))

@app.route('/admin/edit_student/<student_id>')
def edit_student(student_id):
    # Find the student by ID (replace with database query later)
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return render_template('edit_student.html', student=student)
    else:
        return "Student not found", 404

@app.route('/admin/update_student/<student_id>', methods=['POST'])
def update_student(student_id):
    student_name = request.form['student_name']
    diploma = request.form['diploma']
    year_of_entry = int(request.form['year_of_entry'])
    email = request.form['email']
    student_points = int(request.form['student_points'])
    
    # Update the student in the list
    for student in students:
        if student['id'] == student_id:
            student['name'] = student_name
            student['diploma'] = diploma
            student['year_of_entry'] = year_of_entry
            student['email'] = email
            student['points'] = student_points
            break
    
    return redirect(url_for('admin_page'))

@app.route('/admin/delete_student/<student_id>')
def delete_student(student_id):
    # Remove the student from the list (replace with database query later)
    global students
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('admin_page'))

@app.route('/admin/search_student', methods=['GET'])
def search_student():
    query = request.args.get('query')
    # Filter students by ID or name (replace with database query later)
    results = [s for s in students if query.lower() in s['id'].lower() or query.lower() in s['name'].lower()]
    return render_template('admin.html', students=results, redeemable_items=redeemable_items)

@app.route('/student/<student_id>')
def student_page(student_id):
    # Find the student by ID (replace with database query later)
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return render_template('student.html', student=student)  # Pass the student object here
    else:
        return "Student not found", 404

@app.route('/student/<student_id>/redeemable_items')
def redeemable_items_page(student_id):
    # Find the student by ID (replace with database query later)
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return render_template('redeemable_items.html', student=student, redeemable_items=redeemable_items)
    else:
        return "Student not found", 404

@app.route('/student/<student_id>/redeemed_items')
def redeemed_items_page(student_id):
    # Find the student by ID (replace with database query later)
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        # Filter redeemed items for the current student
        student_redeemed_items = [item for item in redeemed_items if item['student_id'] == student_id]
        return render_template('redeemed_items.html', student=student, redeemed_items=student_redeemed_items)
    else:
        return "Student not found", 404

@app.route('/redeem_item/<item_id>', methods=['POST'])
def redeem_item(item_id):
    # Get the student ID from the request (e.g., from JSON payload or form data)
    student_id = request.json.get('student_id')  # Assuming JSON payload is sent

    # Find the item by ID (replace with database query later)
    item = next((i for i in redeemable_items if i['id'] == int(item_id)), None)
    if item:
        # Find the student by ID (replace with database query later)
        student = next((s for s in students if s['id'] == student_id), None)
        if student:
            print(f"Before redemption: Student points = {student['points']}")  # Debug statement
            if student['points'] >= item['points_required'] and item['quantity'] > 0:
                # Deduct points and add to redeemed items
                student['points'] -= item['points_required']
                item['quantity'] -= 1  # Decrement item quantity

                # Get the current date and time
                current_date = datetime.now().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD

                redeemed_items.append({
                    'student_id': student_id,  # Track which student redeemed the item
                    'name': item['name'],
                    'points_used': item['points_required'],
                    'date_redeemed': current_date  # Use the actual date
                })

                print(f"After redemption: Student points = {student['points']}")  # Debug statement
                return jsonify({'success': True, 'points': student['points']})  # Return updated points
            elif item['quantity'] <= 0:
                return jsonify({'success': False, 'message': 'Item out of stock'})
            else:
                return jsonify({'success': False, 'message': 'Not enough points'})
        else:
            return jsonify({'success': False, 'message': 'Student not found'})
    else:
        return jsonify({'success': False, 'message': 'Item not found'})