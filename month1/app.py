# Day 12: Flask Web Dashboard
from flask import Flask, render_template, jsonify, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)
ALERTS_FILE = 'month1/alerts.json'

def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, 'r') as f:
            return json.load(f)
    return []

@app.route('/')
def dashboard():
    alerts = load_alerts()
    return render_template('index.html', alerts=alerts, alert_count=len(alerts), last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/api/alerts')
def api_alerts():
    alerts = load_alerts()
    return jsonify(alerts)

@app.route('/clear', methods=['POST'])
def clear_alerts():
    if os.path.exists(ALERTS_FILE):
        os.remove(ALERTS_FILE)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)