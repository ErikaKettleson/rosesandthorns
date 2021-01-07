from flask import Flask, request, redirect
import flask
import datetime
from twilio.twiml.voice_response import VoiceResponse, Gather, Record, Redirect
from model import db, User, Entries


app = Flask(__name__)


def internal_redirect():
    response = VoiceResponse()
    response.say("Returning to the main menu")
    response.redirect('https://7f6e1c2ecb68.ngrok.io/welcome')

    return twiml(response)


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'

    return resp


@app.route('/rose_transcription', methods=['POST'])
def rose_transcription():
    # print(request.form)

    text = request.form['TranscriptionText']
    rose_transcription_sid = request.form['TranscriptionSid']
    rose_recording_sid = request.form['RecordingSid']
    user = User.query.filter_by(phone_number=request.form['To']).first()

    print('rose text: ', text)

    new_rose = Entries(
            rose_transcription_sid=rose_transcription_sid,
            rose_recording_sid=rose_recording_sid,
            user_id=user.id
            )

    db.session.add(new_rose)

    return twiml(text)


@app.route('/thorn_transcription', methods=['POST'])
def thorn_transcription():
    # print(request.form)
    
    text = request.form['TranscriptionText']
    thorn_transcription_sid = request.form['TranscriptionSid']
    thorn_recording_sid = request.form['RecordingSid']
    user_phone = request.form['To']
    
    print('thorn text: ', text)

    return twiml(text)


@app.route('/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    with response.gather(
        num_digits=1,
        action='https://7f6e1c2ecb68.ngrok.io/menu',
        method="POST"
    ) as g:
        g.say(message="This is roses and thorns " +
              "Press 1 to leave your roses and thorns")

    return twiml(response)


@app.route('/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']

    if (selected_option == '1'):
        response = VoiceResponse()
        rose = get_rose(response)
        print('in menu -> rose: ', rose)
    else:
        response = VoiceResponse()
        response.say('Okay, feel free to call us at any time and \
            leave your roses and thorns')
        response.hangup()

    return twiml(response)


@app.route('/recordings', methods=['POST'])
def recordings():
    recording_sid = request.form['RecordingSid']
    print('rec sid: ', recording_sid)

    return twiml(recording_sid)


@app.route('/trigger_thorn', methods=['POST'])
def trigger_thorn():
    response = VoiceResponse()
    thorn = get_thorn(response)
    print('in thorn: ', thorn)
    return twiml(response)


@app.route('/trigger_rating', methods=['POST'])
def rate():
    response = VoiceResponse()
    get_rating(response)

    response.hangup()

    return twiml(response)


@app.route('/post_rating', methods=['POST'])
def posting_rate():
    rating = request.form['Digits']
    # post rating

    return str(rating)


def get_rose(response):
    print('rose response: ', response)

    response.say('Tell me your rose for today?')
    response.record(transcribe=True,
                    timeout=3,
                    maxLength=20,
                    action="https://7f6e1c2ecb68.ngrok.io/trigger_thorn",
                    transcribeCallback="https://7f6e1c2ecb68.ngrok.io/rose_transcription")

    return twiml(response)


def get_rating(response):
    print('in get rate', response)

    gather = Gather(input='dtmf speech',
                    num_digits=1,
                    action="https://7f6e1c2ecb68.ngrok.io/post_rating")

    gather.say('Rate the day from 1 to 5')
    response.append(gather)

    return twiml(response)


def get_thorn(response):
    print('thorn response: ', response)

    response.say('Tell me your thorn for today?')
    response.record(transcribe=True,
                    timeout=3, 
                    maxLength=20,
                    action="https://7f6e1c2ecb68.ngrok.io/trigger_rating",
                    transcribeCallback="https://7f6e1c2ecb68.ngrok.io/thorn_transcription")

    return twiml(response)
