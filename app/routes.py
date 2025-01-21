from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, render_template, request, redirect, url_for, jsonify
from app import app
import csv
from io import TextIOWrapper

# Dummy user data for testing
users = {
    'admin': 'admin',  # Admin login
    'A1234567X': 'student',  # Student John Tan
    'A1234568Y': 'student',  # Student Sarah Lim
    'admin': 'admin',  # Admin login
    'A1234567X': 'student',  # Student John Tan
    'A1234568Y': 'student',  # Student Sarah Lim
}

# Dummy student data for testing (replace with database later)
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

# Dummy redeemable items for testing (replace with database later)
redeemable_items = [
    {'id': 1, 'name': 'Book', 'points_required': 100, 'quantity': 10},
    {'id': 2, 'name': 'Pen', 'points_required': 50, 'quantity': 20},
]

# Dummy redeemed items for testing (replace with database later)
redeemed_items = []

# Dummy redeemed items for testing (replace with database later)
redeemed_items = []

@app.route('/')
def home():
    return render_template('login.html')




@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return render_template('login.html', error="Invalid username or password")

    elif username not in users:
        return render_template('login.html', error="Invalid username")  # Specific error for invalid username
    elif users[username] != password:
        return render_template('login.html', error="Invalid password")  # Specific error for invalid password
    else:
        if username == 'admin':
            return redirect(url_for('admin_page'))
        else:
            # Find the student by username (replace with database query later)
            student = next((s for s in students if s['id'] == username), None)
            if student:
                return redirect(url_for('student_page', student_id=student['id']))
            else:
                return render_template('login.html', error="Student not found")
            return redirect(url_for('student_page'))




@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    if request.method == 'POST':
        email = request.form['email']
        # Add logic to handle password recovery (e.g., send email)
        return render_template('recover_password.html', message="Password recovery instructions sent to your email.")
    return render_template('recover_password.html')
            # Find the student by username (replace with database query later)
            student = next((s for s in students if s['id'] == username), None)
            if student:
                return redirect(url_for('student_page', student_id=student['id']))
            else:
                return render_template('login.html', error="Student not found")
    else:
        # Pass an error message to the template
        return render_template('login.html', error="Invalid username or password")

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
            for row in csv_data:
                if len(row) == 6:
                    student_id, student_name, diploma, year_of_entry, email, student_points = row
                    students.append({
                        'id': student_id,
                        'name': student_name,
                        'diploma': diploma,
                        'year_of_entry': int(year_of_entry),
                        'email': email,
                        'points': int(student_points)
                    })
                else:
                    flash(f'Invalid row: {row}. Skipping.', 'warning')
            flash('CSV file uploaded successfully', 'success')
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
@app.route('/student/<student_id>')
def student_page(student_id):
    # Find the student by ID (replace with database query later)
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return render_template('student.html', student=student)  # Pass the student object here
    else:
        return "Student not found", 404

@app.route('/redeemable_items')
def redeemable_items_page():
    return render_template('redeemable_items.html', redeemable_items=redeemable_items)
    return render_template('redeemable_items.html', redeemable_items=redeemable_items)

@app.route('/redeemed_items')
def redeemed_items_page():
    return render_template('redeemed_items.html', redeemed_items=redeemed_items)

@app.route('/redeem_item/<item_id>', methods=['POST'])
def redeem_item(item_id):
    # Find the item by ID (replace with database query later)
    item = next((i for i in redeemable_items if i['id'] == int(item_id)), None)
    if item:
        # Check if the student has enough points (replace with database query later)
        student = students[0]  # Assuming the first student is the one redeeming
        if student['points'] >= item['points_required']:
            # Deduct points and add to redeemed items
            student['points'] -= item['points_required']
            redeemed_items.append({
                'name': item['name'],
                'points_used': item['points_required'],
                'date_redeemed': '2023-10-01'  # Replace with actual date
            })
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Not enough points'})
    else:
        return jsonify({'success': False, 'message': 'Item not found'})
@app.route('/redeemed_items')
def redeemed_items_page():
    return render_template('redeemed_items.html', redeemed_items=redeemed_items)

@app.route('/redeem_item/<item_id>', methods=['POST'])
def redeem_item(item_id):
    # Find the item by ID (replace with database query later)
    item = next((i for i in redeemable_items if i['id'] == int(item_id)), None)
    if item:
        # Check if the student has enough points (replace with database query later)
        student = students[0]  # Assuming the first student is the one redeeming
        if student['points'] >= item['points_required']:
            # Deduct points and add to redeemed items
            student['points'] -= item['points_required']
            redeemed_items.append({
                'name': item['name'],
                'points_used': item['points_required'],
                'date_redeemed': '2023-10-01'  # Replace with actual date
            })
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Not enough points'})
    else:
        return jsonify({'success': False, 'message': 'Item not found'})