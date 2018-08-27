from kavenegar import *
import sendgrid
from sendgrid.helpers.mail import *

from dollarial.settings import SEND_GRID
from dollarial import settings


def send_sms_to_user(number, message):
    try:
        api = KavenegarAPI('457A5A6564762B35696C334E6D3957765672713035673D3D')
        params = {
            'sender': '',  # optinal
            'receptor': number,  # multiple mobile number, split by comma
            'message': message,
        }
        if settings.PRODUCTION or settings.SEND_NOTIFICATIONS:
            response = api.sms_send(params)
            print(response)
        else:
            print("Sending SMS with params: %s " % params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def send_email_to_user(subject, from_email, to_email, message):
    sg = sendgrid.SendGridAPIClient(
        apikey=SEND_GRID)
    from_email = Email(from_email)
    to_email = Email(to_email)
    subject = subject
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    if settings.PRODUCTION or settings.SEND_NOTIFICATIONS:
        sg.client.mail.send.post(request_body=mail.get())
    else:
        print("Sending Email with params: %s " % mail.get())


def send_notification_to_user(user, subject, message):
    print("here")
    print(user.notification_preference)
    if user.notification_preference in ['S', 'B']:
        send_sms_to_user(user.phone_number, subject + ": \n" + message)
    if user.notification_preference in ['E', 'B']:
        send_email_to_user(
            subject, "support@dollarial.com", user.email,
            "Dear " + user.first_name + ", \n" + message + "\n Best Regards, \n Dollarial Team"
        )

