#!/bin/bash

# required to install 'sentencepiece'
brew install cmake
brew install pkgconfig

# clone the speechbrain repo
cd speech/libs/
git clone https://github.com/speechbrain/speechbrain/
cd speechbrain/

# install dependencies
pip3 install -r requirements.txt
pip3 install -e .
