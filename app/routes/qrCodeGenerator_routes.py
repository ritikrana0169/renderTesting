# Import necessary modules and classes
from flask import Blueprint, jsonify, request, current_app, send_file
from cryptography.fernet import Fernet
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.model import Attendance, QRCode,db
from app.routes.user_routes import role_required
from app.services.qrCodeGeneratorService import DeviceRepository, EventRepository, createQr, generate_random, find_user_and_event_data, generate_qrcode,get_image, QRCodeRepository,delete_image_by_path,AttendanceRepository,UserRepository,EmailErrorRepository, send_email_with_attachment
from app.services.admin_eventUser_service import admin_eventUser_service


qrRepository = QRCodeRepository()
# Create a Blueprint for QR code generator routes
qrCodeGenerator_routes = Blueprint('qrCodeGenerator_routes', __name__)


def initialize_cipher_suite():
    secret_key = current_app.config['SECRET_KEY']
    return Fernet(secret_key)


def encrypt_data(cipher_suite, data):
    data_bytes = data.encode('utf-8')
    encrypted_data = cipher_suite.encrypt(data_bytes)
    return encrypted_data.decode('utf-8')


def decrypt_data(cipher_suite, encrypted_data):
    try:
        decrypted_data_bytes = cipher_suite.decrypt(encrypted_data.encode('utf-8'))
        decrypted_data = decrypted_data_bytes.decode('utf-8')
        return decrypted_data
    except Exception as e:
        print(f"Decryption Error: {str(e)}")
        return None


@qrCodeGenerator_routes.route('/add/qrcode', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
def loop_qr_information():
    try:
        data = request.get_json()

        if not data or 'qr_data' not in data:
            return jsonify({'error': 'Invalid JSON format or missing "qr_data" field'}), 400

        qr_data = data['qr_data']

        # Check if qr_data is a list
        if not isinstance(qr_data, list):
            return jsonify({'error': '"qr_data" should be a list of objects'}), 400
        

        for entry in qr_data:
            user_id = entry.get('user_id')
            event_id = entry.get('event_id')

            if user_id is not None and event_id is not None:
                create_qr_code(user_id, event_id)
            else:
                return jsonify({'error': 'Each entry in "qr_data" must have "user_id" and "event_id"'}), 400

        return jsonify({'message': 'QR codes generated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_qr_code(user_id, event_id):
    try:
        # data = request.get_json()
        # user_id = data.get('user_id')
        # event_id = data.get('event_id')

        # key = Fernet.generate_key()
        # print(key)

        # Check whether the user of user_id and the event of event_id are available or not
        user_result, event_result = find_user_and_event_data(user_id, event_id)

        # print(user_result)

        # Generating a real random value
        real_random_value = generate_random()

        # Initialize the Fernet cipher suite with the secret key
        cipher_suite = initialize_cipher_suite()

        # Encrypt the real random value
        encrypted_random_value = encrypt_data(cipher_suite, real_random_value)

        # Creating imageUrl using user role + encrypted random value
        imgUrl = f'images/{user_result.role}{encrypted_random_value}.png'
        qrdata = QRCode(user_id=user_id, event_id=event_id, identifier=real_random_value, imageUrl=imgUrl)
       
        # Saving data in qr_code table
        saveQr = createQr(qrdata)
        admin_eventUser_service.add_User_in_event(event_id, user_id)
        if saveQr is None:
            return jsonify({'error': 'QR code already registered'}), 500
        else:
            attendance_record = Attendance(
                date=event_result.event_date,
                check_out_time=event_result.end_time,
                status='Absent',
                user_id=user_id,
                event_id=event_id  # Associate attendance with the event from QR code
                )
            db.session.add(attendance_record)
            db.session.commit()


        # Generating qr code and saving data in a local folder
        generate_qrcode(encrypted_random_value, user_result, imgUrl, event_result)

        # Decrypt the encrypted value for checking purposes
        decrypted_value = decrypt_data(cipher_suite, encrypted_random_value)
        # print(f"Decrypted Value: {decrypted_value}")

        return jsonify({'message': 'QR code created successfully'}), 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Route to get the QR code image for a user and event
@qrCodeGenerator_routes.route('/get/qrcode/<int:event_id>', methods=['GET'])
@jwt_required()
@role_required('User')
def get_image_route(event_id):
    try:
        current_user = get_jwt_identity()
        print(current_user)
        user_id = current_user.get('user_id')

        print(user_id)

        # Check if user_id and event_id are valid
        if user_id is None or event_id is None:
            return jsonify({'error': 'Invalid user_id or event_id'}), 400

        # Get the QR code image data
        image_data = get_image(user_id, event_id)

        # Check if the image_data exists
        if image_data:
            return send_file(image_data, mimetype='image/png'), 200
        else:
            return jsonify({'error': 'User or event not registered or no matching entry'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid user_id or event_id'}), 400


# Route to get all QR codes with pagination
@qrCodeGenerator_routes.route('/get/qrcodes', methods=['GET'])
@jwt_required()
@role_required('Admin')
def get_all_qrcodes_with_pagination_route():
    try:
        page = request.args.get('page', type=int, default=1)
        per_page = request.args.get('per_page', type=int, default=10)
        qrCodeRepository = QRCodeRepository()
        result = qrCodeRepository.get_all_qrcodes_with_pagination(page, per_page)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@qrCodeGenerator_routes.route('/delete/qrcode/<int:qr_id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin')
def delete_qr_code_by_id(qr_id):
    try:
        find_qrCode = qrRepository.delete_qr_by_id(qr_id)
        image_path = find_qrCode
        print(image_path)
        delete_image_by_path(f'app/{image_path}')
        return jsonify({'message': 'QR code deleted successfully'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500




#Route for attendence,event,userDetails,status
@qrCodeGenerator_routes.route('/get/status/<int:event_id>/<int:page>/<int:page_size>', methods=['GET'])
def get_details(event_id, page, page_size):
    count_present = 0
    count_absent = 0
    try:
        present_filter = request.args.get('present')
        absent_filter = request.args.get('absent')
        search_query = request.args.get('search')

        attendance_data = AttendanceRepository().find_attendance_by_event_id(event_id)
        if not attendance_data:
            raise AttributeError("No attendance data found for the event")

        total_records = len(attendance_data)
        total_registration = len(attendance_data)

        if page_size == 0:
            page_size = total_records

        for attendance_record in attendance_data:
            if attendance_record.status == "Present":
                count_present += 1
            elif attendance_record.status == "Absent":
                count_absent += 1

        filtered_data = attendance_data

        if present_filter == 'true' and absent_filter == 'true':
            raise ValueError("Please provide only one filter: present or absent")
        elif present_filter == 'true':
            filtered_data = [record for record in attendance_data if record.status == "Present"]
            total_records = len(filtered_data)
        elif absent_filter == 'true':
            filtered_data = [record for record in attendance_data if record.status == "Absent"]

        if search_query:
            # Retrieve user data for each attendance record and filter based on the user's name (case insensitive)
            filtered_data = [record for record in filtered_data if UserRepository().find_user_by_id(record.user_id).first_name.lower().startswith(search_query.lower())]

        total_records = len(filtered_data)


        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        user_event_details = []

        if start_index < total_records:
            for attendance_record in filtered_data[start_index:end_index]:
                user_id = attendance_record.user_id
                device_id = attendance_record.device_id
                device_result = DeviceRepository().find_device_by_device_id(device_id) if device_id is not None else None
                user_result, event_result = find_user_and_event_data(user_id, event_id)
                check_in_time = attendance_record.check_in_time
                checkin_time_str = "" if check_in_time is None else check_in_time.strftime('%H:%M:%S')

                device_name = device_result.name if device_result else ""
                device_location = device_result.location if device_result else ""

                user_event_details.append({
                    "user_id":user_result.id,
                    "name": user_result.first_name + " " + user_result.last_name,
                    "phone": user_result.phone,
                    "email": user_result.email,
                    "status": attendance_record.status,
                    "device_name": device_name,
                    "device_location": device_location,
                    "checkin_time": checkin_time_str,
                    "event_name": event_result.event_title,
                    "event_location": event_result.event_location,
                    "tags":attendance_record.tags
                })

        response_data = {
            "user_event_details": user_event_details,
            "total_records": total_records,
            "total_registration": total_registration,
            "present": count_present,
            "absent": count_absent,
            "page": page
        }

        return jsonify({"data": response_data}), 200
    except (AttributeError, ValueError) as e:
        return jsonify({"error": str(e)}), 404




#Api to get all users who didn't got emails due to wrong credentials or due to some errors
from flask import request

@qrCodeGenerator_routes.route('get/email_errors/<int:event_id>', methods=['GET'])
def get_email_errors(event_id):
    try:
        email_error_repository = EmailErrorRepository()
        user_repository = UserRepository()
        event_repository = EventRepository()


        email_errors = email_error_repository.get_all_email_errors(event_id=event_id)
        email_error_details = []
        total_email_errors = len(email_errors)

        if total_email_errors == 0:
            response_data = {"message": "Hurray! No email errors"}
        else:
            for error in email_errors:
                user_details = user_repository.find_user_by_id(error.user_id)
                event_details = event_repository.find_event_by_id(error.event_id)
                email_error_details.append({
                    'user_id': error.user_id,
                    'user_name': user_details.first_name + " " + user_details.last_name,
                    'phone': user_details.phone,
                    'email': user_details.email,
                    'event_id': error.event_id,
                    'event_details': event_details.event_title
                })
            response_data = {
                "total_email_errors": total_email_errors,
                "email_error_data": email_error_details
            }
    except Exception as e:
        response_data = {"error": str(e)}

    return jsonify(response_data)




#Api to send emails to those users who didn't recieved email yet
@qrCodeGenerator_routes.route('/send/qrcode', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
def loop_email_information():
    user_repository = UserRepository()
    event_repository = EventRepository()
    try:
        data = request.get_json()

        if not data or 'email_data' not in data:
            return jsonify({'error': 'Invalid JSON format or missing "qr_data" field'}), 400

        email_data = data['email_data']

        # Check if email_data is a list
        if not isinstance(email_data, list):
            return jsonify({'error': '"qr_data" should be a list of objects'}), 400
        response_trace=[]

        for entry in email_data:    
            user_id = entry.get('user_id')
            event_id = entry.get('event_id')
            image_data = get_image(user_id, event_id)
            user_result = user_repository.find_user_by_id(user_id)
            event_result = event_repository.find_event_by_id(event_id)
            image_path="app/"+image_data
            # Hardcoded recipient email for testing, should be user_result.email
            recipient_email = user_result.email
            find_and_delete_email_error_data=EmailErrorRepository().delete_email_error_by_ids(user_id,event_id)
            if(find_and_delete_email_error_data):
                if user_id is not None and event_id is not None:
                    send_email_with_attachment(recipient_email,image_path,event_result,user_result)
                else:
                    print({'error': 'Each entry in email_data must have user_id and event_id'})
                    response_trace.append({"user_id":user_id,"error":"Each entry in email_data must have user_id and event_id"})

                
        return jsonify({'message': response_trace}), 200
            


    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Api to Patch status and tags
@qrCodeGenerator_routes.route('/edit/attendance/<int:event_id>/<int:user_id>', methods=['PATCH'])
# @jwt_required()
# @role_required('Admin')
def edit_attendance(event_id, user_id):
    try:
        # Retrieve the data from the request
        data = request.json
        new_status = data.get('status')
        new_tags = data.get('tags')

        # Check if new_status is provided and is valid
        if new_status and new_status not in ["Present", "Absent"]:
            raise ValueError("Invalid status provided. Status must be 'Present' or 'Absent'.")

        # Retrieve the attendance record to edit
        attendance_record = AttendanceRepository().find_attendance_by_event_id_and_user_id(event_id, user_id)

        if not attendance_record:
            raise AttributeError("Attendance record not found")

        # Update the status if provided and not already the same
        if new_status and new_status != attendance_record.status:
            attendance_record.status = new_status

        # Update the tags if provided
        if new_tags:
            attendance_record.tags = new_tags

        # Save the changes to the database
        db.session.commit()

        # Return success response
        return jsonify({"message": "Attendance record updated successfully","status":new_status,"tags":new_tags}), 200
    except Exception as e:
        # Rollback changes if an error occurs
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



