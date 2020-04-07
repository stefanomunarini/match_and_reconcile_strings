#!/bin/bash

# Wait 10s for all the dependency servers (DB) are up and running
sleep 10

# Apply database migrations
python manage.py migrate

# Start the server
python manage.py runserver 0.0.0.0:8000