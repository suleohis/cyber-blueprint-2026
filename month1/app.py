# Day 12: Flask Web Dashboard
from flask import Flask, render_template
import json
import os

app = Flask(__name__)
ALERTS_FILE = 'month1/alerts.json'

@app.route('/')
def dashboard():
    alerts = []
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, 'r') as f:
            alerts = json.load(f)
    return render_template('index.html', alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True)