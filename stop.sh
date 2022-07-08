#!/bin/bash

# close all tmux sessions
tmux kill-server

# kill all node servers
killall node
