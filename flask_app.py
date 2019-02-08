from flask import Flask, request
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
import os
from twilio.http.http_client import TwilioHttpClient
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="avantij14",
    password="Ookkenshoes@561176",
    hostname="avantij14.mysql.pythonanywhere-services.com",
    databasename="avantij14$numbers",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
#cur = db.cursor()

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = 'AC36a0380d74f87947b5728050e513c882'
auth_token = '011c51f0a2058c658bd1a54878bc1cb4'

client = Client(account_sid, auth_token, http_client=proxy_client)

class Number(db.Model):

    __tablename__ = "numbers"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

numbers = []

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        number = request.form['From']
        message_body = request.form['Body']
        message_body = str(message_body)
        message_body_alt = message_body[:]
        message_body_alt = message_body_alt.lower()
        message_body_alt = message_body_alt.replace(" ", "")
        resp = MessagingResponse()
        query = db.session.query(Number).all()
        for entry in query:
            numbers.append(entry.content)
        if str(message_body_alt) == "ookken" and number not in numbers:
            resp.message("You've signed up to receive Ookken updates!")
            #numbers.append(number)
            number = Number(content=request.form["From"])
            db.session.add(number)
            db.session.commit()
        elif str(number) == "+16785761491" or str(number) == "+16786443998":
            nums = db.session.query(Number).distinct()
            for num in nums:
                message = client.messages.create(body=str(message_body),
                from_='+16784985459',
                to=str(num.content))
        return str(resp)
    return 'ahh4'

