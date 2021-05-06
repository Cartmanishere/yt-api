#!/bin/bash

echo "Starting youtube runner..."
python runner.py &

echo "Starting flask api..."
python app.py

