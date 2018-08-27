from kavenegar import *
import sendgrid
from sendgrid.helpers.mail import *

from dollarial.settings import SEND_GRID


def send_sms_to_user(number, message):
    try:
        api = KavenegarAPI('457A5A6564762B35696C334E6D3957765672713035673D3D')
        params = {
            'sender': '',  # optinal
            'receptor': number,  # multiple mobile number, split by comma
            'message': message,
        }
        response = api.sms_send(params)
        print(response)
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
    sg.client.mail.send.post(request_body=mail.get())


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

