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
    response.say(message="Welcome to roses and thorns.")

    response.redirect("https://3a9885c11e19.ngrok.io/menu?step=rose")

    return twiml(response)


@app.route('/menu', methods=['POST'])
def menu():
    step = request.args.get('step')
    response = VoiceResponse()
    if (step == 'rose'):
        rose = get_rose(response)
        print('rose: ', rose)
    elif (step == 'thorn'):
        thorn = get_thorn(response)
        print('thorn: ', thorn)
    elif (step == 'rating'):
        rating = get_rating(response)
        print('rating: ', rating)
    else:
        response = VoiceResponse()
        response.say('Okay, thanks! feel free to call us at any time and \
            leave your roses and thorns')
        response.hangup()

    return twiml(response)


def get_rose(response):
    print('rose response: ', response)

    response.say('Tell me your rose for today?')
    response.record(transcribe=True,
                    timeout=2,
                    maxLength=20,
                    action="https://3a9885c11e19.ngrok.io/menu?step=thorn",
                    transcribeCallback="https://3a9885c11e19.ngrok.io/rose_transcription")

    return twiml(response)


def get_rating(response):
    print('in get rate', response)

    gather = Gather(input='dtmf speech',
                    num_digits=1,
                    action="https://3a9885c11e19.ngrok.io/menu")

    gather.say('Rate the day from 1 to 5')
    response.append(gather)

    return twiml(response)


def get_thorn(response):
    print('thorn response: ', response)

    response.say('Tell me your thorn for today?')
    response.record(transcribe=True,
                    timeout=2,
                    maxLength=20,
                    action="https://3a9885c11e19.ngrok.io/menu?step=rating",
                    transcribeCallback="https://3a9885c11e19.ngrok.io/thorn_transcription")

    return twiml(response)


def internal_redirect():
    response = VoiceResponse()
    response.say("Returning to the main menu")
    response.redirect('https://3a9885c11e19.ngrok.io/welcome')

    return twiml(response)


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'

    return resp


@app.route('/rose_transcription', methods=['POST'])
def rose_transcription():

    call_sid = request.form['CallSid']
    text = request.form['TranscriptionText']
    rose_transcription_sid = request.form['TranscriptionSid']
    rose_recording_sid = request.form['RecordingSid']
    
    user = User.query.filter_by(phone_number=request.form['To']).first()

    new_entry = Entries(
            rose_transcription_sid=rose_transcription_sid,
            rose_recording_sid=rose_recording_sid,
            user_id=user.user_id,
            call_sid=call_sid
            )
    print('rose text: ', text, "user: ", user, "new_rose: ", new_entry)

    existing_call = Entries.query.filter_by(call_sid=call_sid).first()

    if not existing_call:
        db.session.add(new_entry)
        db.session.commit()
    else:
        existing_call.rose_transcription_sid = rose_transcription_sid
        existing_call.rose_recording_sid = rose_recording_sid
        db.session.commit()

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
