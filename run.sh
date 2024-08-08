#!/bin/bash

# Start the server in the background
python3 server.py &

# Wait for a few seconds to ensure the server is up and running
sleep 2

# Start the client in a new terminal window
gnome-terminal -- bash -c "python3 client.py; exec bash"