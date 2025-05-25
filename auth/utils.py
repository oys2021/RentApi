import random
from django.core.mail import EmailMessage
from auth.models import User,OneTimePassword
from django.conf import settings


def generateotp():
    otp=""
    for i in range(6):
        otp += str(random.randint(1,9))
        

def send_code_to_user(email):
    Subject="One time passcode for EmailVerification"
    otp_code=generateotp()
    print(otp_code)
    user=User.objects.get(email=email)
    current_site="current_site.com"
    email_body=f"Hi {user.firstname} thanks for signing up to {current_site} please verify your email with the \n one time password {otp_code} " 
    from_email=settings.EMAIL_HOST_USER
    
    OneTimePassword.objects.create(user=user,code=otp_code)
    
    d_email=EmailMessage(subject=Subject,body=email_body,from_email=from_email,to=[email])
    d_email.send(fail_silently=True)