from flask import Flask, request, redirect
import flask
import flask_sqlalchemy
from twilio.twiml.voice_response import VoiceResponse, Gather, Record, Redirect
from model import User, Entries, Ratings


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask_sqlalchemy.SQLAlchemy(app)


@app.route('/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    response.say(message="Welcome")

    response.redirect("https://76e3bdbee915.ngrok.io/menu?step=rose")

    return twiml(response)


@app.route('/menu', methods=['POST'])
def menu():
    step = request.args.get('step')
    response = VoiceResponse()
    if (step == 'rose'):
        rose = get_rose(response)
    elif (step == 'thorn'):
        thorn = get_thorn(response)
    elif (step == 'rating'):
        rating = get_rating(response)
    else:
        response = VoiceResponse()
        response.say('Okay, thanks! feel free to call us at any time and \
            leave your roses and thorns')
        response.hangup()

    return twiml(response)


def get_rose(response):
    response.say('Tell me your rose for today?')
    response.record(transcribe=True,
                    timeout=2,
                    maxLength=20,
                    action="https://76e3bdbee915.ngrok.io/menu?step=thorn",
                    transcribeCallback="https://76e3bdbee915.ngrok.io/update?step=rose")

    return twiml(response)


def get_rating(response):
    gather = Gather(input='dtmf',
                    num_digits=1,
                    action="https://76e3bdbee915.ngrok.io/updaterating")

    gather.say('Rate the day from 1 to 5')
    response.append(gather)

    return twiml(response)


def get_thorn(response):
    response.say('Tell me your thorn for today?')
    response.record(transcribe=True,
                    timeout=2,
                    maxLength=20,
                    action="https://76e3bdbee915.ngrok.io/menu?step=rating",
                    transcribeCallback="https://76e3bdbee915.ngrok.io/update?step=thorn")

    return twiml(response)


def internal_redirect():
    response = VoiceResponse()
    response.say("Returning to the main menu")
    response.redirect('https://76e3bdbee915.ngrok.io/welcome')

    return twiml(response)


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'

    return resp


@ app.route('/update', methods=['POST'])
def update():
    step = request.args.get('step')
    call_sid = request.form['CallSid']
    transcription_sid = request.form['TranscriptionSid']
    recording_sid = request.form['RecordingSid']
    user = User.query.filter_by(phone_number=request.form['To']).first()

    new_entry = Entries(
        transcription_sid=transcription_sid,
        recording_sid=recording_sid,
        entry_type=step,
        user_id=user.user_id,
        call_sid=call_sid
    )
    db.session.add(new_entry)
    db.session.commit()

    return twiml(call_sid)


@ app.route('/updaterating', methods=['POST'])
def updaterating():
    call_sid = request.form['CallSid']
    existing_call = Ratings.query.filter_by(call_sid=call_sid).first()

    user = User.query.filter_by(phone_number=request.form['To']).first()
    rating = int(request.form['Digits'])

    new_rating = Ratings(
        rating=rating,
        user_id=user.user_id,
        call_sid=call_sid
    )
    if not existing_call:
        db.session.add(new_rating)
        db.session.commit()

    return twiml(call_sid)
