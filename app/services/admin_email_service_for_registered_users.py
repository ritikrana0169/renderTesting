# admin_email_service_for_registered_users.py
from email.message import EmailMessage
import smtplib
import ssl


def send_welcome_email(user_email, user_password):
    email_sender = 'rajeevranjanmishra4339@gmail.com'
    email_password = 'nbbz lklc dchs zmdv'

    subject = 'Welcome to Our App'
    body = (f'Thank you for registering with Our App! We hope you enjoy using our service. Please find your '
            f'credentials below:\n\nEmail: {user_email}\nPassword: {user_password}')

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = user_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465,
                          context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, user_email, em.as_string())
