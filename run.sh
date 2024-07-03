#!/bin/bash
echo "Starting Fishery ID Tool..."
if [ "$REPL_SLUG" != "" ]; then
  echo "Running on Replit with Gunicorn"
  pip install --user gunicorn flask
  exec gunicorn main:app --bind 0.0.0.0:8080 --log-level info
else
  echo "Running locally with Flask development server"
  python main.py
fi
