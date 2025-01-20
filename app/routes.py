from flask import render_template, request, redirect, url_for
from app import app

# Dummy user data for testing
users = {
    'admin': 'admin',
    'student': 'student',
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Check if username and password match
    if username in users and users[username] == password:
        if username == 'admin':
            return redirect(url_for('admin_page'))
        else:
            return redirect(url_for('student_page'))
    else:
        # Pass an error message to the template
        return render_template('login.html', error="Invalid username or password")

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/student')
def student_page():
    return render_template('student.html')