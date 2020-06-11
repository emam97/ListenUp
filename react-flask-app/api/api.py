import time
from flask import Flask
import yaml

config = yaml.safe_load(open("config.yml"))

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}