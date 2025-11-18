# Day 12: Flask Web Dashboard
from flask import Flask, render_template, jsonify, redirect, url_for
from datetime import datetime
import json
import os
import shutil

app = Flask(__name__)
ALERTS_FILE = 'month1/alerts.json'

def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, 'r') as f:
            return json.load(f)
    return []

@app.route('/history')
def history():
    history = []
    if os.path.exists('month1/alerts_history.json'):
        with open('month1/alerts_history.json', 'r') as f:
            history = json.load(f)
    return render_template('history.html', alerts=history)

@app.route('/')
def dashboard():
    alerts = load_alerts()
    history_count = 0
    if os.path.exists('month1/alerts_history.json'):
        with open('month1/alerts_history.json', 'r') as f:
            history_count = len(json.load(f))
    return render_template(
        'index.html', 
        alerts=alerts, alert_count=len(alerts), 
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), history_count=history_count)

@app.route('/api/alerts')
def api_alerts():
    alerts = load_alerts()
    return jsonify(alerts)

@app.route('/clear', methods=['POST'])
def clear_alerts():
    if os.path.exists(ALERTS_FILE):
        # Archive current alerts
        history_file = 'month1/alerts_history.json'
        if os.path.exists(ALERTS_FILE):
            # Append to history (create if not exists)
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []

            with open(ALERTS_FILE, 'r') as f:
                current = json.load(f)

            history.extend(current)

            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
        os.remove(ALERTS_FILE)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)