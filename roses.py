import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

erika_phone = "+19082477262"
phone_number = "+14159889986"
phone_sid = "PN907d0cc74c6fe911d898db9f3b55230b"


call = client.calls.create(
                    url='https://b499c6e58fea.ngrok.io/welcome',
                    to=erika_phone,
                    from_=phone_number
                )
print("call sid", call.sid)

