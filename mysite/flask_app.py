
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
import os
from twilio.http.http_client import TwilioHttpClient
from twilio.twiml.voice_response import Gather, VoiceResponse
from flask_sqlalchemy import SQLAlchemy
import urllib2
import speech_recognition as sr

import webbrowser

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="emarin6",
    password="listenup1",
    hostname="emarin6.mysql.pythonanywhere-services.com",
    databasename="emarin6$ListenUp",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}


account_sid = 'AC9d38ae9e70ccaee447b341b68b3f1333'
auth_token = '08910c27a7a5163bcc0ed69421bf7c94'

client = Client(account_sid, auth_token, http_client=proxy_client)

class Transcription(db.Model):

    __tablename__ = "transcriptions"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(4096))
    transcription = db.Column(db.String(4096))

@app.route("/", methods=["GET", "POST"])
def record_call():
    response = "Listen Up"
    if request.method == "POST":
        response = "Call in progess"
        response = VoiceResponse()
        response.say("Start taking notes after the beep, press # when finished.")
        response.record(transcribe=True, transcriptionType='slow' ,play_beep='true', max_length=20, finish_on_key='#', transcribeCallback="/transcribing")

        return str(response)
    else:
        return response


@app.route('/transcribing', methods=['GET', 'POST'])
def transcribing():
    print(request.values)

    recording_url = request.values.get('RecordingUrl')

    print 'RECORDING URL: ' + str(recording_url)
    print 'Transcription Id: ' + str(request.values.get('TranscriptionSid'))
    print 'Transcription: ' + str(request.values.get('TranscriptionText'))


    filename = 'speech.wav'
    #using urllib to get file from twilio url
    testfile = urllib2.urlopen(recording_url)
    testfile.retrieve(recording_url, filename)
    # instantiating speech recognition object
    r=sr.Recognizer()
    # creating recording from url
    recording = sr.AudioFile(filename)
    with recording as source:
        audio = r.record(source)
    #printing audio transcription
    print r.recognize_google(audio)

    #next step - add transcription to database 
    addTranscriptionToDatabase(str(recording_url), str(r.recognize_google(audio)))
    return str(request.values.get('TranscriptionText'))


def addTranscriptionToDatabase(url, transcription):
    tr = Transcription()
    tr.url = url
    tr.transcription = transcription
    db.session.add(tr)
    db.session.commit()
