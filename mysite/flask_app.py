
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
import os
from twilio.http.http_client import TwilioHttpClient
from twilio.twiml.voice_response import Gather, VoiceResponse
import requests
import speech_recognition as sr
from ibm_watson import ToneAnalyzerV3
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
import webbrowser
import json
import pymongo
from pymongo import MongoClient
import configparser

app = Flask(__name__)
app.config["DEBUG"] = True

config = configparser.ConfigParser()
config.read('/home/ajoshi/listen_up_config')

account_sid = config['TWILIO']['twilio_sid']
auth_token = config['TWILIO']['twilio_auth_token']

client = Client(account_sid, auth_token)

mongo_client = MongoClient(config['MONGO']['client'], int(config['MONGO']['port']))
db = mongo_client.listen_up
collection = db.voicemail_analysis

@app.route("/", methods=["GET", "POST"])
def record_call():
    response = "Listen Up"
    if request.method == "POST":
        response = "Call in progess"
        response = VoiceResponse()
        response.say("Start talking, press # when finished.")
        response.record(transcribe=True, transcriptionType='slow' ,play_beep='true', max_length=20, finish_on_key='#', transcribeCallback="/transcribing")

        return str(response)
    else:
        return response


@app.route('/transcribing', methods=['GET', 'POST'])
def transcribing():
    print(request.values)

    recording_url = request.values.get('RecordingUrl')

    t = requests.get(recording_url, allow_redirects=True)
    open('recording', 'wb').write(t.content)

    # instantiating speech recognition object
    r=sr.Recognizer()
    # creating recording from url
    recording = sr.AudioFile('recording')
    with recording as source:
        audio = r.record(source)
    #printing audio transcription
    print(r.recognize_google(audio))
    analyzeTextSentiment(str(r.recognize_google(audio)))
    analyzeTextKeywords(str(r.recognize_google(audio)))
    #next step - add transcription to database
    return str(request.values.get('TranscriptionText'))


def analyzeTextSentiment(text):
    authenticator = IAMAuthenticator(config['WATSON']['text_analysis_auth'])
    tone_analyzer = ToneAnalyzerV3(
        version='2019-07-12',
        authenticator=authenticator
    )

    tone_analyzer.set_service_url(config['WATSON']['text_analysis_service_url'])
 
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()
    print(json.dumps(tone_analysis, indent=2))
    x = collection.insert_one(tone_analysis)

def analyzeTextKeywords(text):
    authenticator = IAMAuthenticator(config['WATSON']['keyword_auth'])
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(config['WATSON']['keyword_service_url'])

    response = natural_language_understanding.analyze(
    text=text,
    features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                 limit=2))).get_result()

    print(json.dumps(response, indent=2))
    x = collection.insert_one(response)


if __name__=="__main__":
    app.run()