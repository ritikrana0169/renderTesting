# Import necessary modules for QR code generation, email sending, and database operations
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import string
from dotenv import load_dotenv
import qrcode
import random
import os
from app.models.model import EmailError, db, User, Event, QRCode,Attendance,Device

load_dotenv()
# Repositories for database operations related to users, events, and QR codes
class UserRepository:
    def find_user_by_id(self, user_id):
        # Retrieve user by ID from the database
        user = User.query.get(user_id)
        return user
 
class EventRepository:
    def find_event_by_id(self, event_id):
        # Retrieve event by ID from the database
        return Event.query.get(event_id)
    

class AttendanceRepository:
    def find_attendance_by_event_id(self, event_id):
        return Attendance.query.filter(Attendance.event_id == event_id).all()
    
    def find_attendance_by_event_id_and_user_id(self, event_id, user_id):
        return Attendance.query.filter(Attendance.event_id == event_id, Attendance.user_id == user_id).first()
    


class DeviceRepository:
    def find_device_by_device_id(self,device_id):
        return Device.query.get(device_id)


class EmailErrorRepository:
    def get_all_email_errors(self, event_id=None):
        if event_id is not None:
            email_errors = EmailError.query.filter_by(event_id=event_id).all()
        else:
            email_errors = EmailError.query.all()
        return email_errors


    def delete_email_error_by_ids(self, user_id, event_id):
        # Find the email error with matching user_id and event_id
        email_error = EmailError.query.filter_by(user_id=user_id, event_id=event_id).first()

        if email_error:
            # If the email error is found, delete it from the database
            db.session.delete(email_error)
            db.session.commit()
            return True
        else:
            # If the email error is not found, return False
            return False


# Function to create a QR code entry in the database
def createQr(qrData):
    try:
        # Add the new QR code entry to the database
        user_id = qrData.user_id
        event_id = qrData.event_id

        # Check if the entry already exists
        qr_code_entry = QRCode.query.filter_by(user_id=user_id, event_id=event_id).first()
        if qr_code_entry:
            # Return a flag indicating that the QR code is already registered
            return None
 
        # Add the new QR code entry to the database
        db.session.add(qrData)
        
        # Commit the changes to the database
        db.session.commit()

        # Return a flag indicating successful creation
        return True
    except Exception as e:
        print(f"Error: {e}")
        # Handle other exceptions here
        return False


class QRCodeRepository:
    # Function to get all QR codes with pagination from the database
    def get_all_qrcodes_with_pagination(self, page=1, per_page=10):
        try:
            # Query all QR codes with pagination
            qrcodes = QRCode.query.paginate(page=page, per_page=per_page, error_out=False)

            # Create a list of dictionaries for JSON response
            qrcodes_array = [
                {
                    'id': qr.id,
                    'identifier': qr.identifier,
                    'user_id': qr.user_id,
                    'event_id': qr.event_id,
                    'imageUrl': qr.imageUrl,
                    'is_scanned': qr.is_scanned
                }
                for qr in qrcodes.items
            ]

            # Return the formatted result along with pagination details
            return {'qrcodes': qrcodes_array, 'total_pages': qrcodes.pages, 'current_page': qrcodes.page}

        except Exception as e:
            raise e
        


    @staticmethod
    def delete_qr_by_id(qr_id):
        qr_to_delete = QRCode.query.get(qr_id)
        if qr_to_delete:
            image_url = qr_to_delete.imageUrl
            db.session.delete(qr_to_delete)
            db.session.commit()
            return image_url
        else:
            raise ValueError("QR code not found")
    
    
    

def delete_image_by_path(image_path):
    try:
        os.remove(image_path)
        return True
    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
        return False
    except Exception as e:
        print(f"Error deleting image at {image_path}: {str(e)}")
        return False
    
 
# Function to find user and event data
def find_user_and_event_data(user_id, event_id):
    user_repository = UserRepository()
    event_repository = EventRepository()
    user_data = user_repository.find_user_by_id(user_id)
    event_data = event_repository.find_event_by_id(event_id)
    
    # Check if both user and event data are found
    if user_data and event_data:
        return user_data, event_data
    else:
        return None, None
 

# Function to generate a QR code image and send an email with the image attached
def generate_qrcode(identifier, user_result, imgUrl,event_result):
    try:
        # Create data string for the QR code
        # data = f"identifier:{identifier} event_id:{event_result.id} user_id:{user_result.id}"
        data = f"identifier:{identifier}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # Add data to the QR code
        qr.add_data(data)
        qr.make(fit=True)
        # Generate the QR code image
        img = qr.make_image(fill_color="black", back_color="white")


        # Save the QR code image
        save_path = f'app/{imgUrl}'
        img.save(save_path)
        print("Image saved successfully")
        print(save_path)
        # Hardcoded recipient email for testing, should be user_result.email
        recipient_email = 'saviji520@gmail.com'

        # Call the function to send an email with the QR code attached
        send_email_with_attachment(recipient_email, save_path, event_result,user_result)

        # Return success message
        return {"success": True, "message": "QR code generated successfully"}
    except Exception as e:
        # Return an error message if an exception occurs
        return {"error": str(e)}


# Function to send an email with a QR code attached
def check_smtp_credentials(HOST, PORT, FROM_EMAIL, PASSWORD,eventData, userData):
    try:
        with smtplib.SMTP(HOST, PORT) as smtp:
            smtp.starttls()
            smtp.login(FROM_EMAIL, PASSWORD)
        return True
    except Exception as e:
        save_email_error(userData.id, eventData.id)
        print(f"SMTP credentials are incorrect or cannot connect to the server: {e}")
        return False

def send_email_with_attachment(recipient_email, image_path, eventData, userData):
    # SMTP email configuration
    HOST = "smtp-mail.outlook.com"
    PORT = 587
    FROM_EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    # print(FROM_EMAIL+" "+PASSWORD)
 
    # Check if SMTP credentials are correct
    if not check_smtp_credentials(HOST, PORT, FROM_EMAIL, PASSWORD,eventData, userData):
        print("SMTP credentials are incorrect. Please check and try again.")
        return
 
    # Email content 
    subject = f"Invitation to Our {eventData.event_title} Event"
    body = f"""
    Dear {userData.first_name} {userData.last_name},

    We are delighted to invite you to our {eventData.event_title} event. Join us for a day filled with
    joy, laughter, and memorable moments.

    Date: {eventData.event_date}
    Time: {eventData.start_time}
    Venue: {eventData.event_location}

    Attached to this email, you will find a personalized invitation QR Code.
    We hope to see you there!

    Best regards,
    Masai School
    """

    # Create a MIMEMultipart object for email composition
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient_email

    # Attach the email body as plain text
    msg.attach(MIMEText(body, 'plain'))

    # Attach the QR code image
    with open(image_path, 'rb') as image_file:
        image = MIMEImage(image_file.read(), name="invitation_image.png")
        msg.attach(image)

    try:
        # Attempt to send the email using SMTP
        with smtplib.SMTP(HOST, PORT) as smtp:
            smtp.starttls()
            smtp.login(FROM_EMAIL, PASSWORD)
            smtp.sendmail(FROM_EMAIL, recipient_email, msg.as_string())
        print("Email sent successfully")

    except Exception as e:
        # Print an error message if sending email fails
        save_email_error(userData.id, eventData.id)
        print(f"Error sending email: {e}")



def save_email_error(user_id, event_id):
    try:
        # Create an EmailError object with the provided details
        email_error = EmailError(user_id=user_id, event_id=event_id)
        # Add the EmailError object to the session and commit to the database
        db.session.add(email_error)
        db.session.commit()
        print("Email error details saved to the database")
    except Exception as e:
        # Print an error message if saving to the database fails
        print(f"Error saving email error details to the database: {e}")
        # Rollback the changes in case of an error
        db.session.rollback()


# Function to get the image URL for a user and event
def get_image(user_id, event_id):
    user_event_data = find_user_and_event_data(user_id, event_id)
    print('user and event found')
    # Check if user and event are registered
    if user_event_data is None:
        return None  
    # Fetch the image data from the QRCode table
    qr_code_entry = QRCode.query.filter_by(user_id=user_id, event_id=event_id).first()
    print('qr_code found')
    # Return the image URL if found, otherwise return None
    if qr_code_entry:
        return qr_code_entry.imageUrl
    else:
        return None 



#Generating the random and hashed value
def generate_random():
    # Set the length of the random value
    length = 15

    # Define the characters to choose from
    characters = string.digits  # numbers only

    # Generate a random value
    random_value = ''.join(random.choice(characters) for _ in range(length))


    # Return the original value and the hashed value
    return random_value

