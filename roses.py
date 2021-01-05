import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

erika_phone = "+19082477262"
phone_number = "+14159889986"
phone_sid = "PN907d0cc74c6fe911d898db9f3b55230b"


call = client.calls.create(
                    url='https://02f04349c1e3.ngrok.io/welcome',
                    to=erika_phone,
                    from_=phone_number
                )
print("call sid", call.sid)


def get_transcription(transcription_id):
    transcription = client.transcriptions(transcription_id).fetch()
    
    print(transcription.transcription_text)

def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

def get_rose():
    resp = VoiceResponse()

    resp.say('What\'s your rose today?')
    resp.record(transcribe=True,
                timeout=3, 
                maxLength=20,
                action="https://02f04349c1e3.ngrok.io/test_action",
                transcribeCallback="https://02f04349c1e3.ngrok.io/handle_transcription")

def get_thorn():
    resp = VoiceResponse()

    resp.say('What\'s your thorn today?')
    resp.record(transcribe=True,
                timeout=3, 
                maxLength=20,
                action="https://02f04349c1e3.ngrok.io/test_action",
                transcribeCallback="https://02f04349c1e3.ngrok.io/handle_transcription")

def redirect():
    response = VoiceResponse()
    response.say("Returning to the main menu")
    response.redirect('https://02f04349c1e3.ngrok.io/welcome')

    return twiml(response)