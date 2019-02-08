
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
import os
from twilio.http.http_client import TwilioHttpClient
from twilio.twiml.voice_response import Gather, VoiceResponse


app = Flask(__name__)
app.config["DEBUG"] = True


proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = 'AC9d38ae9e70ccaee447b341b68b3f1333'
auth_token = '08910c27a7a5163bcc0ed69421bf7c94'

client = Client(account_sid, auth_token, http_client=proxy_client)

@app.route("/", methods=["GET", "POST"])
def record_call():
    response = "Listen Up"
    if request.method == "POST":
        response = "Call in progess"
        response = VoiceResponse()
        response.say("Start taking notes after the beep, press # when finished.")
        response.record(transcribe=True, play_beep='true', max_length=20, finish_on_key='#', transcribeCallback="/transcribing")
        transcription = client.transcriptions(account_sid) \
            .fetch()
        print("TRANSCRIPTION: " + str(transcription))
        return str(response)
    else:
        return response


@app.route('/transcribing', methods=['GET', 'POST'])
def transcribing():
    print(request.values)

    recording_url = request.values.get('RecordingUrl')

    print 'RECORDING URL: ' + str(recording_url)