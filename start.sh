#!/bin/bash

# Launch Flask Server
tmux new -d -s digital-assistant &&
tmux send-keys -t digital-assistant 'python3 -m flask run' C-m
tmux detach -s digital-assistant
