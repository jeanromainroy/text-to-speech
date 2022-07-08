from flask import Flask, request

# initiate app
app = Flask(__name__)

# import libs
from tts import run as tts_run


@app.route("/")
def index():
    return "<p>Welcome, I am your digital assistant!</p>"


@app.post("/tts")
def tts():

    # validate
    if request.method != 'POST': return "Error, wrong method\n"

    # extract request object
    try:
        text = request.form['text']
    except:
        return "Error, no input\n"

    # validate
    if type(text) != str or len(text) == 0: return "Error, invalid input"

    # run tts
    tts_run(text)

    return 'Success'
