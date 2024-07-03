#!/bin/bash
echo "Starting Fishery ID Tool..."
echo "Checking pip and gunicorn installations..."

# Check pip installation
if command -v pip >/dev/null 2>&1; then
  echo "pip is installed"
else
  echo "pip is not installed"
  exit 127
fi

# Check gunicorn installation
if command -v gunicorn >/dev/null 2>&1; then
  echo "gunicorn is installed"
else
  echo "gunicorn is not installed"
  exit 127
fi

# Install necessary packages
echo "Installing required packages..."
pip install --user gunicorn flask

# Check installed paths
echo "Checking installed paths..."
echo "pip path: $(command -v pip)"
echo "gunicorn path: $(command -v gunicorn)"

# Start Gunicorn
if [ "$REPL_SLUG" != "" ]; then
  echo "Running on Replit with Gunicorn"
  ./.pythonlibs/bin/gunicorn main:app --bind 0.0.0.0:8080 --workers 1 --log-level info
else
  echo "Running locally with Flask development server"
  python main.py
fi
