import os
from twilio.rest import Client
from model import User


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

erika_phone = "+19082477262"
phone_number = "+14159889986"
phone_sid = "PN907d0cc74c6fe911d898db9f3b55230b"


def make_call(num):
    call = client.calls.create(
        url='https://76e3bdbee915.ngrok.io/welcome',
        to=num,
        from_=phone_number
    )
    print("call sid", call.sid)


users = User.query.all()
for user in users:
    make_call(user.phone_number)
