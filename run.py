from flask import Flask, jsonify
from flask_cors import CORS
from app.routes.qrCodeScanner_routes import qrCodeScanner_routes
from app.database import app
from app.routes.admin_user_update_route import update_users_blueprint
from app.routes.qrCodeGenerator_routes import qrCodeGenerator_routes
from app.routes.admin_user_routes import user_blueprint
from app.routes.admin_overview_route import overview_blueprint
from app.routes.admin_eventUser_routes import eventUser_routes
from app.routes.admin_device_routes import eventDevice_routes
from app.routes.admin_event_routes import all_event_bp
from app.routes.admin_addEvent_routes import addEevent_bp
from app.routes.admin_specicEvent_routes import event_bp3
from app.routes.admin_external_user_route import Externaluser_blueprint
from app.routes.admin_getEventDetailsById_route import GetEvent_blueprint
from app.routes.all_attendance_history_of_organization_route import Allevent_attedance_history_blueprint
from app.routes.admin_event_attendance_route import admin_event_attendance_routes
from app.routes.user_routes import user_details_bp
from app.routes.admin_event_routes import event_bp
from app.routes.user_routes import events_blueprint, auth_bp, jwt, user_update
from dotenv import load_dotenv
from app.routes.admin_register_device_routes import device_routes
from app.routes.admin_event_attendance_mark import  event_userAttendance_mark

from app.routes.admin_remainder_email_routes import remainder_email
from app.scheduler.eventScheduler import initialize_scheduler

import os
from app.scheduler.scheduler import initialize_scheduler
# from app.DA.demo8 import fraudBp



# Loading evn variables
load_dotenv()

# getting jwt-secret-key from .env file
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')

# Initializing JWT
jwt.init_app(app)



# Allow all origins for all routes
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, origins="*")


# Register the Blueprint



app.config['SECRET_KEY'] = b'ezoKkYbFj0pxm66_SimGLr3sVZYzahm_LsWdD8JZF_U='

#Blueprint for Login Authorization
 
app.register_blueprint(auth_bp, url_prefix="/auth")

#Blueprint for qrCodeGenerator_routes

app.register_blueprint(qrCodeGenerator_routes, url_prefix='/qr')

# Blueprint for updating user details
app.register_blueprint(update_users_blueprint, url_prefix='/api')

# Blueprint for adding new user, getting user and deleting
app.register_blueprint(user_blueprint, url_prefix='/api')

app.register_blueprint(overview_blueprint, url_prefix='/api')


# Get all the events of a single user by user_id.
# This api will be used to show all events of user on user dashboard
app.register_blueprint(events_blueprint, url_prefix='/events')
app.register_blueprint(user_details_bp, url_prefix='/api')


# Scan QrCode
app.register_blueprint(qrCodeScanner_routes, url_prefix='/qr')


#getting all events
app.register_blueprint(event_bp, url_prefix='/admin')
app.register_blueprint(addEevent_bp, url_prefix='/api')
app.register_blueprint(event_bp3, url_prefix='/api')
app.register_blueprint(all_event_bp,url_prefix='/all_event_bp')
app.register_blueprint(GetEvent_blueprint, url_prefix='/admin')

#external user
app.register_blueprint(Externaluser_blueprint, url_prefix='/admin')
app.register_blueprint(Allevent_attedance_history_blueprint, url_prefix='/admin')

# upload user details blueprint
app.register_blueprint(user_update, url_prefix="/user")

app.register_blueprint(event_bp, url_prefix='/api', name='event')

# Register admin register device the Blueprint
app.register_blueprint(device_routes, url_prefix='/api')

# app.register_blueprint(fraudBp, url_prefix = "/api")

# Define a route for the root URL
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Tracer Project!'})


app.register_blueprint(eventUser_routes, url_prefix='/eventUser')
app.register_blueprint(eventDevice_routes, url_prefix='/eventDevice')
app.register_blueprint(event_userAttendance_mark, url_prefix='/api')
app.register_blueprint(admin_event_attendance_routes, url_prefix='/api')
app.register_blueprint(remainder_email, url_prefix='/api')
if __name__ == '__main__':
    initialize_scheduler(app)
    
    app.run(debug=True)

    # trainservice()