#!/bin/bash


echo "Select game mode : (1) Solo (2) Multiplayer"
read -r game_mode


# Start the server in the background
python3 server.py "$game_mode" &

# Wait for a few seconds to ensure the server is up and running
sleep 2

# Start the client in a new terminal window
if [ "$game_mode" -eq 1 ]; then
    gnome-terminal -- bash -c "python3 client.py; exec bash"
elif [ "$game_mode" -eq 2 ]; then
    gnome-terminal -- bash -c "python3 client.py; exec bash"
    sleep 3
    gnome-terminal -- bash -c "python3 client.py; exec bash"
else
    echo "Invalid game mode selected."
fi