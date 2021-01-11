import os
from twilio.rest import Client
from model import User
import sched
import time

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

erika_phone = "+19082477262"
phone_number = "+14159889986"
phone_sid = "PN907d0cc74c6fe911d898db9f3b55230b"


def make_call(num):
    call = client.calls.create(
        url='https://42445d3159ec.ngrok.io/welcome',
        to=num,
        from_=phone_number
    )
    print("call sid", call.sid)


def get_nums():
    users = User.query.all()
    for user in users:
        make_call(user.phone_number)


s = sched.scheduler(time.time, time.sleep)


def call_some_times():
    s.enter(60, 1, get_nums)
    s.run()


while True:
    call_some_times()
