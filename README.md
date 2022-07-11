# Text-to-Speech

A natural sounding text-to-speech accessible through a chrome extension. Running locally for privacy. 


## Architecture

### Speech

The speech engine is based on the [SpeechBrain Toolkit](https://speechbrain.github.io/)

The speech recognition model is fine-tuned on my voice. 

It runs inside a Flask server.

The config file can be found [here](./speech/config.py)


## Installation

Run the [install](./install.sh) script (it takes ~10 seconds to launch), 

    ./install.sh


Then install the chrome extension, 

1. In your chrome-based browser go to extensions (e.g. chrome://extensions, brave://extensions)

2. Click on "Load unpacked"

3. Select the chrome-extension/public/ folder of this repository
