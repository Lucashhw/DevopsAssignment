from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import datetime module

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    diploma = db.Column(db.String, nullable=False)
    year_of_entry = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, default=0)

class RedeemableItem(db.Model):
    __tablename__ = 'redeemable_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment for ID
    name = db.Column(db.String, nullable=False)
    points_required = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class RedeemedItem(db.Model):
    __tablename__ = 'redeemed_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String, db.ForeignKey('students.id'), nullable=False)
    item_name = db.Column(db.String, nullable=False)
    points_used = db.Column(db.Integer, nullable=False)
    date_redeemed = db.Column(db.Date, nullable=False)

    def __init__(self, student_id, item_name, points_used):
        self.student_id = student_id
        self.item_name = item_name
        self.points_used = points_used
        self.date_redeemed = datetime.now().date()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()