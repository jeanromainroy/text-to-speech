from flask import Flask, request

# initiate app
app = Flask(__name__)

# import libs
from tts import run as tts_run

# variables
tts_running = False


@app.route("/")
def index():
    return "<p>Welcome, I am your digital assistant!</p>"


@app.post("/tts")
def tts():
    global tts_running

    # validate
    if request.method != 'POST': return "Error, wrong method\n"

    # extract request object
    try:
        text = request.form['text']
    except:
        return "Error, no input\n"

    # validate
    if type(text) != str or len(text) == 0: return "Error, invalid input"

    # if tts is already running, stop
    if tts_running: return "Error, please wait as TTS is already running"

    # run tts
    tts_running = True
    tts_run(text)
    tts_running = False

    return 'Success'
