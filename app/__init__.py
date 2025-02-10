from flask import Flask
from .models import db, init_db  # Use relative import

app = Flask(__name__)
app.secret_key = '0cb6bd5d92641068ed7d480fd951eb0a7f1d3a032f32ad77'

# Update the database configuration for PostgreSQL
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('postgresql://databasedevops_user:uuA9jjnKdIEL7hgmlMwpjEOjIpnFdAmY@dpg-cul0kad2ng1s73829jn0-a.singapore-postgres.render.com/databasedevops', 'sqlite:///library.db')  # Fallback to SQLite for local development
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize database
init_db(app)

# Import routes after initializing the database
from app import routes  # Simply import the module