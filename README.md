# Library Board Platform System (LBPS)

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Flask-2.x-green) ![SQLite](https://img.shields.io/badge/SQLite-3.x-orange) ![DevOps](https://img.shields.io/badge/DevOps-Practices-red)

The **Library Board Platform System (LBPS)** is a gamified platform designed to enhance the user experience for students in a local library. This system allows students to earn points, redeem items, and manage their accounts while providing administrators with tools to manage student data and redeemable items.

This project was developed as part of the **DevOps (DOP) module** at the School of Infocomm Technology, Diploma in Information Technology (Year 3, 2024/25).

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Project Structure](#project-structure)
5. [Setup Instructions](#setup-instructions)
6. [Running the Application](#running-the-application)
7. [Testing](#testing)
8. [CI/CD Pipeline](#cicd-pipeline)
9. [Contributors](#contributors)

---

## Overview

The LBPS is a web-based application that provides a gamified experience for students. It includes functionalities for both **admin users** and **student users**, allowing them to interact with the system seamlessly. The application is built using Python's Flask framework and integrates a database-driven architecture with SQLite (and optionally PostgreSQL).

Key functionalities include:
- **Login Process:** Secure login for both admin and student users.
- **Admin Features:** Manage student accounts, redeemable items, and perform searches.
- **Student Features:** View redeemable items, redeem items, and track redeemed items.
- **Password Recovery:** Reset passwords securely by providing a username and new password.

---

## Features

### Login Process
- Users can log in with their username and password.
- Password fields are hidden by default, with an option to reveal the password.
- Invalid login attempts prompt appropriate error messages.
- Successful login redirects users to their respective dashboards:
  - Admin: Admin Dashboard
  - Student: Student Dashboard
- A "Recover Password" page is available for password resets.

### Admin Features
- **Create New Student Accounts:** Add new students manually or via CSV upload.
- **Modify Student Accounts:** Update student details such as name, diploma, email, and points.
- **Delete Student Accounts:** Remove student accounts after confirmation.
- **List All Student Accounts:** Display all registered students with options to modify or delete.
- **Search for Students:** Search by student ID or name.
- **Manage Redeemable Items:** Create, update, and delete items available for redemption.

### Student Features
- **Dashboard:** Displays student information (name, points, email, etc.).
- **Redeemable Items Page:** View and redeem items using points.
- **Redeemed Items Page:** Track previously redeemed items and remaining points.
- **Password Recovery:** Reset passwords securely by providing a username and new password.

---

## Technologies Used

- **Backend:** Python (Flask Framework)
- **Database:** SQLite (with SQLAlchemy ORM), PostgreSQL (optional for production)
- **Frontend:** HTML, CSS (Bootstrap for styling)
- **Testing Framework:** `unittest` (for unit tests)
- **CI/CD Tools:** GitHub Actions
- **Version Control:** Git and GitHub

---

## Project Structure

```
LBPS/
├── app/
│   ├── __init__.py          # Initializes the Flask app and database
│   ├── models.py            # Defines SQLAlchemy models (Student, RedeemableItem, RedeemedItem)
│   ├── routes.py            # Contains all route handlers for admin and student functionalities
│   ├── templates/           # HTML templates for user interfaces
│   │   ├── login.html       # Login page
│   │   ├── admin.html       # Admin dashboard
│   │   ├── student.html     # Student dashboard
│   │   ├── recover_password.html # Password recovery page
│   │   ├── redeemable_items.html # Redeemable items page
│   │   └── redeemed_items.html   # Redeemed items page
│   └── static/              # Static files (CSS, JS, images)
├── tests/                   # Unit tests for the application
│   ├── test_admin.py        # Tests for admin functionalities
│   ├── test_login.py        # Tests for login functionality
│   ├── test_recoverpassword.py # Tests for password recovery
│   ├── test_redeemable.py   # Tests for redeemable items
│   ├── test_redeemed.py     # Tests for redeemed items
│   └── test_student.py      # Tests for student functionalities
├── populate_db.py           # Script to populate the SQLite database with initial data
├── run.py                   # Entry point for running the Flask application
└── requirements.txt         # List of dependencies for the project
```

---

## Setup Instructions

### Prerequisites

- Python 3.x installed on your machine.
- Git installed for version control.
- A code editor (e.g., VS Code, PyCharm).

### Steps to Set Up

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<your-username>/LBPS.git
   cd LBPS
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv myvenv
   source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database:**
   Run the script to populate the database with initial data:
   ```bash
   python populate_db.py
   ```

5. **Run the Application:**
   Start the Flask development server:
   ```bash
   python run.py
   ```

6. **Access the Application:**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## Running the Application

Once the server is running, you can access the following pages:

- **Login Page:** `/login`
- **Admin Dashboard:** `/admin` (Login with `username=admin`, `password=admin`)
- **Student Dashboard:** `/student/<student_id>` (Login with valid student credentials)
- **Password Recovery Page:** `/recover_password`

---

## Testing

The project includes comprehensive unit tests for all implemented features. To run the tests:

```bash
python -m unittest discover tests
```

### Test Coverage

- **Admin Tests:**
  - CRUD operations for students and redeemable items.
  - CSV upload functionality.
- **Student Tests:**
  - Redeeming items.
  - Password recovery.
  - Edge cases (e.g., empty fields, invalid inputs).

---

## CI/CD Pipeline

A **basic CI/CD pipeline** is set up using **GitHub Actions** to automate testing and deployment. The pipeline performs the following tasks:

1. **Installs Dependencies:**
   - Installs all required dependencies listed in the `requirements.txt` file.

2. **Runs Unit Tests:**
   - Executes the unit tests using Python's `unittest` framework. These tests validate the functionality of the application, including both passing and failing scenarios.

3. **Deploys to Render:**
   - If all tests pass successfully, the pipeline triggers a deployment to **Render**, a cloud platform for hosting web applications. Render automatically pulls updates from the GitHub repository and deploys the application to a live environment.

4. **Notifies Stakeholders:**
   - Upon successful deployment, stakeholders are notified via **Discord**. A webhook integration sends a message to a designated Discord channel, informing the team that the application is live and ready for use.

---

## Contributors

This project was developed collaboratively by the following team members:

- **[Danish]:** Developer (Implemented database schema, all features, and unit tests)
- **[Raahil]:** Scrum Master (Managed sprints and backlog)
- **[Hanwen]:** Technical Lead 
- **[Hazel]:** Quality Assurance 
---