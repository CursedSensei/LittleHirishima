#!/bin/bash
tmux new-session -d -t "little_hirishima"
tmux send-keys -t "little_hirishima:0" "/home/aoi/Documents/hirishima_bot/.venv/bin/python3 /home/aoi/Documents/hirishima_bot/little_hirishima.pyw" C-m
