#!/bin/bash
# Change directory to the folder containing this script
cd "$(dirname "$0")"

# Activate the virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the Python script, passing any arguments forwarded to this script
python3 extract.py "$@"

# Wait for user input if run interactively, so the window remains open
if [ -z "$1" ]; then
    echo ""
    read -p "Press Enter to exit..."
fi
