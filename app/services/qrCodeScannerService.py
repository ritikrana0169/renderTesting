from app.models.model import QRCode, User, Attendance, db, Event, Device
from cryptography.fernet import Fernet
from flask import current_app
from app.routes.qrCodeGenerator_routes import decrypt_data
from datetime import datetime


class UserRepository:
    def find_user_by_id(self, user_id):
        user = User.query.get(user_id)
        return user


class EventRepository:
    def find_event_by_id(self, event_id):
        # Retrieve event by ID from the database
        return Event.query.get(event_id)


class DeviceRepository:
    def find_device_by_id(self, device_id):
        # Retrieve device by ID from the database
        return Device.query.get(device_id)


def check_qrcode_scanned(encrypted_qr_identifier, device_id):
    try:
        # Retrieve the Fernet key from the application configuration or any secure storage
        key = current_app.config['SECRET_KEY']
        cipher_suite = Fernet(key)

        # Decrypt the QR identifier using the Fernet key
        qr_identifier = decrypt_data(cipher_suite, encrypted_qr_identifier)

        #         # if qr_identifier:
        #         #     print(qr_identifier)

        # Find the QR code based on the decrypted identifier
        qr_code = QRCode.query.filter_by(identifier=qr_identifier).first()

        if qr_code:
            user_id = qr_code.user_id
            event_id = qr_code.event_id

            user_data = UserRepository().find_user_by_id(user_id)
            event_data = EventRepository().find_event_by_id(event_id)
            device_data = DeviceRepository().find_device_by_id(device_id)

            # Check if the device is associated with the event
            if device_data not in event_data.devices:
                return {'message': 'Device not associated with the event.'}

            if qr_code.is_scanned:
                return {
                    'email':user_data.email,
                    'name':user_data.first_name+" "+user_data.last_name,
                    'message': f'Qr Code Already Scanned'
                }  
            else:
                # If QR code is present but not scanned, update the status
                qr_code.is_scanned = True

                attendance_record = Attendance.query.filter_by(event_id=event_id, user_id=user_id).first()

                if attendance_record:
                    # Update the existing attendance record
                    attendance_record.check_in_time = datetime.now().time()
                    attendance_record.status = 'Present'
                    attendance_record.device_id = device_id  # Update device_id if needed

                    # Commit the changes to the database
                    db.session.commit()
                else:
                    # If the attendance record doesn't exist, you can create a new one

                    new_attendance_record = Attendance(
                        date=event_data.date,
                        check_in_time=datetime.now().time(),
                        check_out_time=event_data.end_time,
                        status='Present',
                        device_id=device_id,
                        event_id=event_id,
                        user_id=user_id
                    )

                    db.session.add(new_attendance_record)
                    db.session.commit()

                return {
                    'email':user_data.email,
                    'name':user_data.first_name+" "+user_data.last_name,
                    'message': f'Welcome! {user_data.first_name+" "+user_data.last_name} , Your QR code Scanned using device {device_data.name}. '
                               f'Now, you can join the event.'
                }
        else:
            return {'message': 'Invalid QR code identifier. Please register first.'}
    except Exception as e:
        return {'error': str(e)}
