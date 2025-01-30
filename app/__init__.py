from flask import Flask
from .models import db, init_db  # Use relative import

app = Flask(__name__)
app.secret_key = '0cb6bd5d92641068ed7d480fd951eb0a7f1d3a032f32ad77'

# Initialize database
init_db(app)

# Import routes after initializing the database
from app import routes  # Simply import the module