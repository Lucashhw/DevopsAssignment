from flask import render_template, request, redirect, url_for
from app import app

# Dummy data for testing
students = [
    {'id': 'A1234567X', 'name': 'John Tan', 'points': 50},
    {'id': 'A1234568Y', 'name': 'Sarah Lim', 'points': 80},
]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Dummy validation
    if username == 'admin' and password == 'admin':
        return redirect(url_for('admin_page'))
    elif username == 'student' and password == 'student':
        return redirect(url_for('student_page'))
    else:
        return "Invalid username or password"

@app.route('/admin')
def admin_page():
    return render_template('admin.html', students=students)

@app.route('/student')
def student_page():
    return render_template('student.html')