# service.py
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
def send_email(receiver_email, body,Subject):
    # 'kanhaiyatiwari1234@outlook.com'
    sender_email = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] =Subject
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    smtp_server = "smtp.outlook.com"  # Change this to your SMTP server address
    port = 587 # This is usually the default port for SMTP

    # Establish a connection
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # Enable TLS encryption

    try:
        # Login to your email account
        server.login(sender_email, PASSWORD)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        # print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email address and password.")
    except smtplib.SMTPException as e:
        print("An error occurred while sending the email:", e)
    finally:
        # Close the connection
        server.quit()
