from flask import Flask, request, redirect
import flask
from twilio.twiml.voice_response import VoiceResponse, Gather, Record, Redirect

app = Flask(__name__)

@app.route('/get_rose', methods=['GET', 'POST'])
def get_rose(response):
    import ipdb; ipdb.set_trace()
    print('response: ', response)

    # response = VoiceResponse()
    response.say('Tell me your rose for today?')
    response.record(transcribe=True,
                timeout=3, 
                maxLength=20,
                action="https://02f04349c1e3.ngrok.io/test_action",
                transcribeCallback="https://02f04349c1e3.ngrok.io/handle_transcription")

    return response
    # return internal_redirect()

@app.route('/rate', methods=['GET', 'POST'])
def console():
    resp = VoiceResponse()
    req = request
    print('req', req)
    return req.values

@app.route('/test_action', methods=['GET', 'POST'])
def text():
    print('in /test_action')
    recording_sid = request.form['RecordingSid']
    print('recording sid: ', recording_sid)

    return str(recording_sid)

@app.route('/handle_transcription', methods=['GET', 'POST'])
def transcription():
    text = request.form['TranscriptionText']
    print('text: ', text)
    return str(text)


@app.route('/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    with response.gather(
        num_digits=1, action='https://02f04349c1e3.ngrok.io/menu', method="POST"
    ) as g:
        g.say(message="This is roses and thorns " +
              "Please press 1 for your rose" +
              "Please press 2 for your thorn" +
              "Press 3 to rate your day")
    return twiml(response)

@app.route('/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    print('selected_option: ', selected_option)

    if selected_option == '1':
        # import ipdb; ipdb.set_trace()
        response = VoiceResponse()
        get_rose(response)
        return twiml(response)
        # response.say("I'd love to hear your rose")
        # response.redirect('https://02f04349c1e3.ngrok.io/get_rose')

    # elif selected_option == '2':
    #     # tbd
    # elif selected_option == '3':
    #     # tbd
    # else:
    #     resp.say("Try again.")

    return internal_redirect()

def get_transcription(transcription_id):
    transcription = client.transcriptions(transcription_id).fetch()
    
    print(transcription.transcription_text)

def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

def rate():
    resp = VoiceResponse()
    gather = Gather(input='dtmf speech', num_digits=1, action='https://238d3bd215ade4a7f804504c20dba0aa.m.pipedream.net')
    gather.say('Rate the day from 1 to 5')
    resp.append(gather) 
    return internal_redirect()


# def get_rose():
#     resp = VoiceResponse()

#     resp.say('What\'s your rose today?')
#     resp.redirect('https://02f04349c1e3.ngrok.io/get_rose')
#     return internal_redirect()


def get_thorn():
    resp = VoiceResponse()

    resp.say('What\'s your thorn today?')
    resp.record(transcribe=True,
                timeout=3, 
                maxLength=20,
                action="https://02f04349c1e3.ngrok.io/test_action",
                transcribeCallback="https://02f04349c1e3.ngrok.io/handle_transcription")
    return redirect()

def internal_redirect():
    response = VoiceResponse()
    response.say("Returning to the main menu")
    response.redirect('https://02f04349c1e3.ngrok.io/welcome')

    return twiml(response)