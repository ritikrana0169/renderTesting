# eventDeviceService.py

from app.models.model import db, Event, Device
from app.exception.eventDeviceExecption import EventException, DeviceException, GenericException

class admin_eventdevice_servic:

    def add_device_to_event(event_id, device_id):
        try:
            event = db.session.query(Event).get(event_id)
            device = db.session.query(Device).get(device_id)

            if not event:
                raise EventException(f'Event not found with this event id: {event_id}')
            if not device:
                raise DeviceException(f'Device not found with this device id: {device_id}')
            if device.availability =='Unavailable':
    
                raise DeviceException(f'this device is not available or already associated with the event')
            if device not in event.devices:
                device.availability = 'Unavailable'
                event.devices.append(device)
                db.session.commit()
                return {'message': 'Device added to the event successfully'}, 200
            else:
                return {'message': 'Device is already associated with the event'}, 200

        except (EventException, DeviceException) as e:
            raise e

        except Exception as e:
            raise GenericException(str(e))

    def get_devices_for_event(event_id):
        try:
            event = Event.query.get(event_id)

            if not event:
                raise EventException(f'Event not found with this event id: {event_id}')

            devices = event.devices
            if not devices:
                raise EventException(f'No devices available in this event id: {event_id}')

            serialized_devices = []
            for device in devices:
                serialized_device = {
                    'id': device.id,
                    'name': device.name,
                    'ip_address': device.ip_address,
                    'location': device.location
                    # Add other fields as needed
                }
                serialized_devices.append(serialized_device)

            return serialized_devices

        except EventException as e:
            raise e

        except Exception as e:
            raise GenericException(str(e))

    def remove_device_from_event(event_id, device_id):
        try:
            event = Event.query.get(event_id)
            device = Device.query.get(device_id)

            if not event:
                raise EventException(f'Event not found with this event id: {event_id}')
            if not device:
                raise DeviceException(f'Device not found with this device id: {device_id}')

            if device in event.devices:
                device.availability = 'Available'
                event.devices.remove(device)
                db.session.commit()
                return {'message': 'Device removed from the event successfully'}, 200
            else:
                raise EventException(f'There is no device in the event for this device id: {device_id}')

        except (EventException, DeviceException) as e:
            raise e

        except Exception as e:
            raise GenericException(str(e))
