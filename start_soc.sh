#!/bin/bash
# start_soc.sh v2 – Cyber Blueprint 2026
# One-click deploy for hiring managers & future you

set -e  # Exit on any error

echo "Starting Cyber Blueprint 2026 Mini-SIEM..."
echo "Generating fresh attack logs..."

# Generate realistic attack + normal background
python month1/generate_logs.py 25 --normal 15

echo "Starting Flask dashboard on http://127.0.0.1:5000"
echo "Press Ctrl+C to stop"
echo ""

# Run Flask app
python month1/app.py