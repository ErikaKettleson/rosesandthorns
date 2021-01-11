from flask import Flask, request, redirect
import flask
import flask_sqlalchemy
from twilio.twiml.voice_response import VoiceResponse, Gather, Record, Redirect
from model import User, Entries


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask_sqlalchemy.SQLAlchemy(app)


@app.route('/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    response.say(message="Welcome")

    response.redirect("https://b13852daa512.ngrok.io/menu?step=rose")

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
                    action="https://b13852daa512.ngrok.io/menu?step=thorn",
                    transcribeCallback="https://b13852daa512.ngrok.io/update?step=rose")

    return twiml(response)


def get_rating(response):
    gather = Gather(input='dtmf',
                    num_digits=1,
                    action="https://b13852daa512.ngrok.io/update?step=rating")

    gather.say('Rate the day from 1 to 5')
    response.append(gather)

    return twiml(response)


def get_thorn(response):
    response.say('Tell me your thorn for today?')
    response.record(transcribe=True,
                    timeout=2,
                    maxLength=20,
                    # action="https://b13852daa512.ngrok.io/menu?step=rating",
                    transcribeCallback="https://b13852daa512.ngrok.io/update?step=thorn")

    return twiml(response)


def internal_redirect():
    response = VoiceResponse()
    response.say("Returning to the main menu")
    response.redirect('https://b13852daa512.ngrok.io/welcome')

    return twiml(response)


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'

    return resp


@app.route('/update', methods=['POST'])
def update():
    step = request.args.get('step')
    call_sid = request.form['CallSid']

    if (step == 'rose'):
        existing_call = Entries.query.filter_by(call_sid=call_sid).first()

        rose_transcription_sid = request.form['TranscriptionSid']
        rose_recording_sid = request.form['RecordingSid']
        user = User.query.filter_by(phone_number=request.form['To']).first()

        rose_new_entry = Entries(
            rose_transcription_sid=rose_transcription_sid,
            rose_recording_sid=rose_recording_sid,
            user_id=user.user_id,
            call_sid=call_sid
        )
        if not existing_call:
            db.session.add(rose_new_entry)
        else:
            existing_call.rose_transcription_sid = rose_transcription_sid
            existing_call.rose_recording_sid = rose_recording_sid
    elif (step == 'thorn'):
        existing_call = Entries.query.filter_by(call_sid=call_sid).first()
        user = User.query.filter_by(phone_number=request.form['To']).first()

        thorn_transcription_sid = request.form['TranscriptionSid']
        thorn_recording_sid = request.form['RecordingSid']

        new_entry = Entries(
            thorn_transcription_sid=thorn_transcription_sid,
            thorn_recording_sid=thorn_recording_sid,
            user_id=user.user_id,
            call_sid=call_sid
        )
        if not existing_call:
            db.session.add(new_entry)
        else:
            update = Entries(
                thorn_transcription_sid=thorn_transcription_sid,
                thorn_recording_sid=thorn_recording_sid,
            )
            db.session.merge(update)
            # existing_call.thorn_transcription_sid = thorn_transcription_sid
            # existing_call.thorn_recording_sid = thorn_recording_sid
            # print(existing_call)
    # elif (step == 'rating'):
    #     existing_call = Entries.query.filter_by(call_sid=call_sid).first()
    #     user = User.query.filter_by(phone_number=request.form['To']).first()
    #     print('in rating, exsintg call: ', existing_call, 'user: ', user)

    #     rating = int(request.form['Digits'])
    #     print('rating: ', rating)

    #     new_entry = Entries(
    #         rating=rating,
    #         user_id=user.user_id,
    #         call_sid=call_sid
    #         )
    #     if not existing_call:
    #         print('in rating with no existing call')
    #         db.session.add(new_entry)
    #         db.session.commit()

    #     else:
    #         existing_call.rating = rating
    #         db.session.commit()
    # else:
    #     print('in updates: else condition')
    db.session.commit()
    db.session.flush()
    return twiml(call_sid)


# @app.route('/thorn_transcription', methods=['POST'])
# def thorn_transcription():
#     # print(request.form)

#     text = request.form['TranscriptionText']
#     thorn_transcription_sid = request.form['TranscriptionSid']
#     thorn_recording_sid = request.form['RecordingSid']
#     user_phone = request.form['To']

#     print('thorn text: ', text)

#     return twiml(text)
