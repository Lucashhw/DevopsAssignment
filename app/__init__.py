from flask import Flask

app = Flask(__name__)

# Import routes and expose the students list
from app.routes import students

# Import routes
from app import routes