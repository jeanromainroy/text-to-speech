# Personal Digital Assistant

A broad range of useful scripts made executable through speech. Running locally for privacy. 


## Domains

Productivity:  Emails, Slack, Whatsapp, Clients' instances

News:  Twitter, Traditional Media (e.g. Le Monde, NYT, FT), Stock Exchange

Knowledge:  Wikipedia, Google

Entertainment:  Audiobook, Music, Youtube, Conversational Agent (e.g. GPT)


_And custom stuff..._


## Architecture

### Speech

The speech engine is based on the [SpeechBrain Toolkit](https://speechbrain.github.io/)

The speech recognition model is fine-tuned on my voice. 

It runs inside a Flask server.

The config file can be found [here](./speech/config.py)


### ...


## Installation

Run the [install](./install.sh) script (it takes ~10 seconds to launch), 

    ./install.sh


## Author

Jean-Romain Roy

- [Portfolio](https://jeanromainroy.com/)

- [GitHub](https://github.com/jeanromainroy)
