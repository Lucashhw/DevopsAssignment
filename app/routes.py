from flask import Flask, render_template, request, redirect, url_for
from app import app

# Dummy user data for testing
users = {
    'admin': 'admin',
    'student': 'student',
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
            return redirect(url_for('student_page'))




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


@app.route('/student')
def student_page():
    return render_template('student.html')

@app.route('/redeemable_items')
def redeemable_items_page():
    return render_template('redeemable_items.html')

