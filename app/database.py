from urllib.parse import quote
from flask import Flask
from app.models.model import db
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app, origins="*")
from flask_bcrypt import Bcrypt

# from flask_cors import CORS

# app = Flask(__name__)


CORS(app, origins='*')  # for ngrok integration
# CORS(app)

bcrypt = Bcrypt(app)  # bcrypt for hashing the password

# Set sql password
sql_username=os.getenv('MYSQL_USERNAME')
sql_db_name=os.getenv("MYSQL_DB_NAME")
sql_password = os.getenv("MYSQL_PASSWORD")

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{sql_username}:{sql_password}@localhost/{sql_db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
