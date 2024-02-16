from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()
from flask_bcrypt import Bcrypt
app = Flask(__name__)
CORS(app, origins="*")

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# app = Flask(__name__)


CORS(app, origins='*')  # for ngrok integration
# CORS(app)

bcrypt = Bcrypt(app)  # bcrypt for hashing the password

# Set sql password
sql_username=os.getenv('MYSQL_USERNAME')
sql_db_name=os.getenv("MYSQL_DB_NAME")
sql_password = os.getenv("MYSQL_PASSWORD")

# Configure the database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{sql_username}:{sql_password}@localhost/{sql_db_name}'
# Set PostgreSQL credentials
db_username = 'db_0vxj_user'
db_password = 'UYyB3vLeKq78q3edzk35mFLXCeZQpMPU'
db_host = 'localhost'  # Render usually provides a connection via localhost
db_port = '5432'
db_name = 'db_0vxj'

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
