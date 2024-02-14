# admin_user_service.py
from flask import jsonify
from app.models.model import User, Event,Attendance
from sqlalchemy import select
from datetime import datetime
from app.exception.admin_externalUser_exception import EventException, UserException, GenericException

class Get_event_by_EventId:
    @staticmethod
    def get_event_by_EventId_endpoint(event_id):
        event = Event.query.get(event_id)
        if(event == None):
            raise EventException(f'Event not found with event id: {event_id}')  
        event_data ={
            'event_id': event.id, 
            'event_title': event.event_title, 
            'event_type': event.event_type, 
            'event_description': event.event_description,
            'event_date': event.event_date.isoformat(),
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat(),
            'event_status': event.event_status,
            'event_location': event.event_location
        }   
        Users = event.participants
        p = Attendance.query.filter_by(event_id=event_id,status='Present').count()
        a = Attendance.query.filter_by(event_id=event_id,status='Absent').count()
        AttendanceData={'Absent':a,'Present':p,'total':p+a}

        Devices=event.devices
        Devices_data=[]
        for d in Devices:
            atd = Attendance.query.filter_by(event_id=event_id,device_id=d.id,status='Present').count()
            data={
                'id': d.id, 
                'name': d.name,
                'location': d.location,
                'availability': d.availability,
                'total_user':atd
            }
            Devices_data.append(data)

        details={
            'Event':event_data,
            'Attendance':AttendanceData,
            'Devices':Devices_data

        }
        return details

