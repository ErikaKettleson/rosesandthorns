from flask import Flask, request, redirect
import flask
from twilio.twiml.voice_response import VoiceResponse, Gather, Record, Redirect

app = Flask(__name__)


def internal_redirect():
    response = VoiceResponse()
    response.say("Returning to the main menu")
    response.redirect('https://b499c6e58fea.ngrok.io/welcome')

    return twiml(response)


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'

    return resp


@app.route('/rose_transcription', methods=['POST'])
def rose_transcription():
    text = request.form['TranscriptionText']
    print('rose text: ', text)

    return twiml(text)


@app.route('/thorn_transcription', methods=['POST'])
def thorn_transcription():
    text = request.form['TranscriptionText']
    print('thorn text: ', text)

    return twiml(text)


@app.route('/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    with response.gather(
        num_digits=1,
        action='https://b499c6e58fea.ngrok.io/menu',
        method="POST"
    ) as g:
        g.say(message="This is roses and thorns " +
              "Press 1 to leave your roses")

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
        thorn = get_thorn(response)
        print('in menu -> thorn: ', thorn)

    return twiml(response)


@app.route('/recordings', methods=['POST'])
def recordings():
    recording_sid = request.form['RecordingSid']
    print('rec sid: ', recording_sid)

    return twiml(recording_sid)


def get_rose(response):
    print('rose response: ', response)

    response.say('Tell me your rose for today?')
    response.record(transcribe=True,
                    timeout=3, 
                    maxLength=20,
                    # action="https://b499c6e58fea.ngrok.io/recordings",
                    transcribeCallback="https://b499c6e58fea.ngrok.io/rose_transcription")
    response.say('Bleep bloop test test test?')

    return twiml(response)


def get_thorn(response):
    print('thorn response: ', response)

    response.say('Tell me your thorn for today?')
    response.record(transcribe=True,
                    timeout=3, 
                    maxLength=20,
                    # action="https://b499c6e58fea.ngrok.io/recordings",
                    transcribeCallback="https://b499c6e58fea.ngrok.io/thorn_transcription")

    return twiml(response)