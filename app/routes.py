from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from app import app, db
from app.models import Student, RedeemableItem, RedeemedItem
import csv
from io import TextIOWrapper
from datetime import datetime

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return render_template('login.html', error="Invalid username or password")
    if username == 'admin' and password == 'admin':
        session['user_id'] = 'admin'
        return redirect(url_for('admin_page'))
    
    # Updated line to use Session.get()
    student = db.session.get(Student, username)
    if student and student.password_hash == password:
        print(f"Before login: Student points = {student.points}")  # Debug statement
        print(f"Before login: Student username = {student.id}")  # Debug statement
        session['user_id'] = student.id
        return redirect(url_for('student_page', student_id=student.id))
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    if request.method == 'POST':
        username = request.form.get('username')  # Get the username from the form
        new_password = request.form.get('new_password')  # Get the new password from the form

        # Check for empty fields
        if not username or not new_password:
            flash("Please provide both username and a new password.", "error")
            return render_template('recover_password.html')

        # Check if the username exists in the database
        student = db.session.get(Student, username)
        if not student:
            flash("No account found with the provided username.", "error")
            return render_template('recover_password.html')

        # Update the password_hash field in the database
        student.password_hash = new_password
        db.session.commit()

        # Notify the user of success and redirect to the login page
        flash("Password has been successfully updated.", "success")
        return redirect(url_for('home'))  # Redirect back to the login page

    # For GET requests, render the recover password page
    return render_template('recover_password.html')

@app.route('/admin')
def admin_page():
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    items = RedeemableItem.query.all()
    return render_template('admin.html', students=Student.query.all(), redeemable_items=items)

@app.route('/admin/create_student', methods=['POST'])
def create_student():
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    student_id = request.form['student_id']
    student_name = request.form['student_name']
    diploma = request.form['diploma']
    year_of_entry = int(request.form['year_of_entry'])
    email = request.form['email']
    student_points = int(request.form['student_points'])
    new_student = Student(
        id=student_id,
        name=student_name,
        diploma=diploma,
        year_of_entry=year_of_entry,
        email=email,
        points=student_points,
        password_hash='student'  # Default password hash for new students
    )
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('admin_page'))

@app.route('/admin/upload_csv', methods=['POST'])
def upload_csv():
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
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
                        new_student = Student(
                            id=student_id,
                            name=student_name,
                            diploma=diploma,
                            year_of_entry=int(year_of_entry),
                            email=email,
                            points=int(student_points),
                            password_hash='student'  # Default password hash for new students
                        )
                        db.session.add(new_student)
                    else:
                        has_invalid_rows = True  # Mark as invalid
                else:
                    has_invalid_rows = True  # Mark as invalid
            # Check if there are any invalid rows
            if has_invalid_rows:
                flash('Invalid CSV file. Please ensure all rows have the correct format.', 'error')
            else:
                db.session.commit()
                flash('CSV file uploaded successfully.', 'success')
        except Exception as e:
            flash(f'Error processing CSV file: {str(e)}', 'error')
    else:
        flash('Invalid file type. Please upload a CSV file.', 'error')
    return redirect(url_for('admin_page'))

@app.route('/admin/edit_student/<student_id>')
def edit_student(student_id):
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    student = db.session.get(Student, student_id)
    if student:
        return render_template('edit_student.html', student=student)
    else:
        return "Student not found", 404

@app.route('/admin/update_student/<student_id>', methods=['POST'])
def update_student(student_id):
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    student = db.session.get(Student, student_id)
    if student:
        student.name = request.form['student_name']
        student.diploma = request.form['diploma']
        student.year_of_entry = int(request.form['year_of_entry'])
        student.email = request.form['email']
        student.points = int(request.form['student_points'])
        # Preserve the password_hash unless explicitly modified
        new_password = request.form.get('new_password')  # Optional field for changing password
        if new_password:
            student.password_hash = new_password  # Update password_hash if provided
        db.session.commit()
    return redirect(url_for('admin_page'))

@app.route('/admin/delete_student/<student_id>')
def delete_student(student_id):
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    student = db.session.get(Student, student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect(url_for('admin_page'))

@app.route('/admin/search_student', methods=['GET'])
def search_student():
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    query = request.args.get('query')
    results = Student.query.filter((Student.id.ilike(f'%{query}%')) | (Student.name.ilike(f'%{query}%'))).all()
    items = RedeemableItem.query.all()
    return render_template('admin.html', students=results, redeemable_items=items)

@app.route('/redeemable_items')
def redeemable_items_admin_page():
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    items = RedeemableItem.query.all()
    return render_template('admin_redeemable_items.html', redeemable_items=items)

@app.route('/admin/create_redeemable_item', methods=['POST'])
def create_redeemable_item():
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    name = request.form['name']
    points_required = int(request.form['points_required'])
    quantity = int(request.form['quantity'])
    new_item = RedeemableItem(
        name=name,
        points_required=points_required,
        quantity=quantity
    )
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('redeemable_items_admin_page'))

@app.route('/admin/edit_redeemable_item/<item_id>')
def edit_redeemable_item(item_id):
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    item = db.session.get(RedeemableItem, item_id)
    if item:
        return jsonify({
            'id': item.id,
            'name': item.name,
            'points_required': item.points_required,
            'quantity': item.quantity
        })
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/admin/update_redeemable_item/<item_id>', methods=['POST'])
def update_redeemable_item(item_id):
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    item = db.session.get(RedeemableItem, item_id)
    if item:
        item.name = request.form['name']
        item.points_required = int(request.form['points_required'])
        item.quantity = int(request.form['quantity'])
        db.session.commit()
        flash('Item updated successfully.', 'success')
    else:
        flash('Item not found.', 'error')
    return redirect(url_for('redeemable_items_admin_page'))

@app.route('/admin/delete_redeemable_item/<item_id>')
def delete_redeemable_item(item_id):
    if session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    item = db.session.get(RedeemableItem, item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('redeemable_items_admin_page'))

@app.route('/student/<student_id>')
def student_page(student_id):
    if session.get('user_id') != student_id and session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    student = db.session.get(Student, student_id)
    if student:
        return render_template('student.html', student=student)
    else:
        return "Student not found", 404

@app.route('/student/<student_id>/redeemable_items')
def redeemable_items_page(student_id):
    if session.get('user_id') != student_id and session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    student = db.session.get(Student, student_id)
    if student:
        items = RedeemableItem.query.all()
        return render_template('redeemable_items.html', student=student, redeemable_items=items)
    else:
        return "Student not found", 404

@app.route('/student/<student_id>/redeemed_items')
def redeemed_items_page(student_id):
    if session.get('user_id') != student_id and session.get('user_id') != 'admin':
        return redirect(url_for('home'))  # Redirect unauthorized users to the login page
    
    # Updated line to use Session.get()
    student = db.session.get(Student, student_id)
    if student:
        redeemed_items = RedeemedItem.query.filter_by(student_id=student_id).all()
        return render_template('redeemed_items.html', student=student, redeemed_items=redeemed_items)
    else:
        return "Student not found", 404

@app.route('/redeem_item/<item_id>', methods=['POST'])
def redeem_item(item_id):
    if session.get('user_id') != request.json.get('student_id') and session.get('user_id') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized access'})
    student_id = request.json.get('student_id')
    
    # Updated line to use Session.get()
    item = db.session.get(RedeemableItem, item_id)
    if item:
        # Updated line to use Session.get()
        student = db.session.get(Student, student_id)
        if student:
            print(f"Before redemption: Student points = {student.points}")
            if student.points >= item.points_required and item.quantity > 0:
                student.points -= item.points_required
                item.quantity -= 1
                current_date = datetime.now().date()  # Correctly using datetime here
                redeemed_item = RedeemedItem(
                    student_id=student_id,
                    item_name=item.name,
                    points_used=item.points_required
                )
                db.session.add(redeemed_item)
                db.session.commit()
                print(f"After redemption: Student points = {student.points}")
                return jsonify({'success': True, 'points': student.points})
            elif item.quantity <= 0:
                return jsonify({'success': False, 'message': 'Item out of stock'})
            else:
                return jsonify({'success': False, 'message': 'Not enough points'})
        else:
            return jsonify({'success': False, 'message': 'Student not found'})
    else:
        return jsonify({'success': False, 'message': 'Item not found'})