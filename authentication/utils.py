import random
from django.core.mail import EmailMessage
from authentication.models import User,OneTimePassword
from django.conf import settings
from django.core.mail import send_mail,BadHeaderError,EmailMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.db import IntegrityError


import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


def generateotp():
    otp=""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp
        

def send_code_to_user(email):
    Subject="One time passcode for EmailVerification"
    otp_code=generateotp()
    print("this is the code",otp_code)
    user=User.objects.get(email=email)
    current_site="current_site.com"
    email_body=f"Hi {user.username} thanks for signing up to Renz. Please verify your email with the \n one time password {otp_code} " 
    from_email="opokuyawsarfo3@gmail.com"
    
    OneTimePassword.objects.create(user=user,code=otp_code)
    
    message = Mail(
    from_email=from_email,
    to_emails=email,
    subject=Subject,
    html_content=f'{email_body}')
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"SendGrid Error: {str(e)}")
        


def send_password_request_to_user(email, reset_link):
    subject = "Password Reset Request"  # Fixed: Removed extra comma
    message = f"Click the link to reset your password: {reset_link}"
    from_email = "opokuyawsarfo3@gmail.com"
    recipient_list = [email]  

    mail = Mail(
        from_email=from_email,
        to_emails=recipient_list,  # Fixed: List format required
        subject=subject,
        html_content=message
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"SendGrid Error: {str(e)}")

def send_reset_otp_to_user(email, otp_code):
    subject = "Your Password Reset Code"
    new_message = f"Use this OTP to reset your password: {otp_code}"
    from_email = "opokuyawsarfo3@gmail.com"
    recipient_list = [email]
    
    try:
        user = User.objects.get(email=email)

        message = Mail(
            from_email=from_email,
            to_emails=recipient_list,
            subject=subject,
            html_content=new_message
        )

        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(f"SendGrid Error: {str(e)}")



        

def generate_unique_otp():
    """Generate a unique OTP that does not already exist in the database."""
    while True:
        otp_code = random.randint(100000, 999999) 
        print("updates otp",otp_code)
        if not OneTimePassword.objects.filter(code=otp_code).exists():  # Check uniqueness
            return otp_code
        
# utils.py (or wherever the OTP logic is defined)
def generate_and_store_otp(email):
    try:
        user = User.objects.get(email=email)

        otp_code = generate_unique_otp()  
        print(f"Generated OTP: {otp_code}")

        otp_entry = OneTimePassword.objects.filter(user=user, used=False).order_by('-created_at').first()
        if otp_entry:
            otp_entry.used = True  # Mark the previous OTP as used
            otp_entry.save()
            print("Previous OTP marked as used.")
        
        OneTimePassword.objects.create(user=user, code=otp_code)
        print("New OTP created.")
        return otp_code
    
    except User.DoesNotExist:
        return None  



# def generate_and_store_otp(email):
#     try:
#         user = User.objects.get(email=email)

#         otp_code = random.randint(100000, 999999)
#         print("cooooode", otp_code)

#         otp_entry = OneTimePassword.objects.filter(user=user).first()

#         if otp_entry:
#             otp_entry.code = otp_code
#             otp_entry.save()
#         else:
#             OneTimePassword.objects.create(user=user, code=otp_code)  # Fixed missing OTP creation
        
#         return otp_code

#     except Exception as e:
#         print(f"Error generating OTP: {str(e)}")
#         return None  # Fixed syntax error