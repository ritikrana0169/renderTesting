import re
from flask import Blueprint, jsonify, request
from app.services.admin_addEvent_service import CreateEventResource
from datetime import datetime
from app.exception.admin_externalUser_exception import EventException, GenericException
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.routes.user_routes import role_required

addEevent_bp = Blueprint('addEevent_bp', __name__)


# Route to create a new event
@addEevent_bp.route('/admin/events', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
def create_event():
  data = request.get_json()
  if 'event_type' not in data or data['event_type'].upper() not in ['ONCE', 'RECURRING']:
    return jsonify({'message': 'Inviled event_type.'}), 400

  if data['event_type'].upper()=='ONCE':
    data['repeat_days']=[]
    data['repeat_type']=None
  else:
    if 'repeat_type' not in data or data['repeat_type'].upper() not in ['WEEKLY','DAILY'] and data['event_type'].upper() != 'ONCE':
      return jsonify({'message': 'Inviled repeat_type.'}), 400
  # Validate repeat days
  repeat_days = data.get('repeat_days', [])

  uppercase_days = []
  for day in repeat_days:
    uppercase_days.append(day.upper())
    
  valid_repeat_days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
  invalid_days = set(uppercase_days) - set(valid_repeat_days)
  if invalid_days:
    return {'message': f'Invalid repeat days: {", ".join(invalid_days)}'}, 400
     
  if 'start_time' not in data or 'end_time' not in data:
    return jsonify({'message': 'start_time or  end_time not present.'}), 400
  
  data['start_time']=convert_to_hms(data['start_time'])
  data['end_time']=convert_to_hms(data['end_time'])

    #Validate time
  if not are_valid_times(data['start_time'],data['end_time']):
    return jsonify({'message': 'Inviled start_time or end_time .'}), 400
  
  if not validate_time(data['start_time'],data['end_time']):
    return jsonify({'message': 'Start time is not before end time.'}), 400
  
  if'event_date' not in data or not is_valid_date_and_time(data['event_date'],data['start_time']):
    return jsonify({'message': 'Invalid event_date or start_time (either in the past or incorrect format).'}), 400

  try:
    response = CreateEventResource.newEvent(data)
    response_message = {
      "data":response,
      "message":"Event created successfully"  
    },201
    return response_message
  
  except (EventException, GenericException) as e:
    return e.to_response()
    

def is_valid_date_and_time(date_str, time_str):
  try:
    input_date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert date string to date object
    input_time = datetime.strptime(time_str, '%H:%M:%S').time()  # Convert time string to time object
    current_datetime = datetime.now()  # Get current datetime

    # Get current date and time separately
    current_date = current_datetime.date()
    current_time = current_datetime.time()

    if input_date == current_date and input_time > current_time or input_date > current_date:
      return True  # Valid: Date is current and time is after current time
    else:
      return False  # Invalid: Date is not current or time is not after current time

  except ValueError:  # Catch error if the date or time format is incorrect
      return False  # Invalid date or time format




def validate_time(start_time, end_time):
    # Convert time strings to datetime objects
    start = datetime.strptime(start_time, '%H:%M:%S')
    end = datetime.strptime(end_time, '%H:%M:%S')

    # Check if start time is before end time
    if start < end:
        return True
    else:
        return False

def convert_to_hms(time_input):

  components = time_input.split(":")
  # If it's in hh:mm format, add seconds as 00
  if len(components) == 2:
    h, m = map(int, components)
    s = 0
  elif len(components) == 3:
      h, m, s = map(int, components)
  else:
    return "Invalid input format"
  
  # Constructing the time string in h:m:s format
  time_hms = f"{h:02d}:{m:02d}:{s:02d}"
  return time_hms

def are_valid_times(time1, time2):
  time_format = "%H:%M:%S"
  try:
    # Attempt to parse both time strings
    datetime.strptime(time1, time_format)
    datetime.strptime(time2, time_format)
    return True  # Both times are valid
  except ValueError:
    return False  # At least one time is invalid
