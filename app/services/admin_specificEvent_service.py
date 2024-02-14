from flask import Flask, jsonify
from flask_restful import Api, Resource
from app.models.model import db, Event


class EventDetailsResource:
     
    def get_events_for_user(self,event_id):
        event = Event.query.get(event_id)

        try:
            if event:
                serialized_devices = []
                if len(event.devices) != 0:
                    for device in event.devices:
                        serialized_device = {
                            'id': device.id,
                            'name': device.name,
                            'ip_address': device.ip_address,
                            'location': device.location
                        }
                        serialized_devices.append(serialized_device)
                event_data = {
                    'Event_Title': event.event_title,
                    'Event_Type': event.event_type,
                    'Event_Description': event.event_description,
                    'Event_Date': event.event_date,
                    'Start_Time': event.start_time.strftime('%H:%M:%S'),
                    'End_Time': event.end_time.strftime('%H:%M:%S'),
                    'created_at':event.created_at,
                    'event_status':event.event_status,
                    'updated_at':event.updated_at,
                    'event_location':event.event_location,
                    # 'participants':event.participants,
                    'devices':serialized_devices
                }
                return event_data
            else:
                return jsonify({'message': 'Event not found'}), 404
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        

