from flask import Flask

# Initialize the Flask app
app = Flask(__name__)


# Set a secret key for session management
app.secret_key = '0cb6bd5d92641068ed7d480fd951eb0a7f1d3a032f32ad77'  # Replace with your generated key


# Import and expose the students list and redeemable_items list
from app.routes import students, redeemable_items

# Import routes
from app import routes