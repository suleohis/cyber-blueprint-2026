# Day 11: Email CRITICAL Alerts with JSON Attachment
import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import os
import smtplib
from email.message import EmailMessage

# Load config
with open('month1/config.json', 'r') as f:
    config = json.load(f)

# Setup logging
logging.basicConfig(
    level=config['log_level'],
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('month1/detection.log'),
        logging.StreamHandler()
    ]
)

logging.info("=== EMAIL ALERTS MODULE STARTED ===")

# [Same parsing + detection logic as Day 10]
attempts = defaultdict(list)
TIME_FORMAT = '%m/%d/%Y %I:%M:%S %p'

with open(config['log_file'], 'r') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if line.startswith('#') or not line or '4625' not in line:
            continue
        time_str = line.split(' - ')[0]
        try:
            timestamp = datetime.strptime(time_str, TIME_FORMAT)
        except ValueError:
            continue
        ip_start = line.find('Source IP: ') + 11
        ip_end = line.find(' ', ip_start)
        ip = line[ip_start:ip_end] if ip_end != -1 else line[ip_start:]
        attempts[ip].append((timestamp, line_num))

alerts = []
for ip, events in attempts.items():
    events.sort(key=lambda x: x[0])
    window_start = 0
    for i in range(2, len(events)):
        if events[i][0] - events[window_start][0] <= timedelta(minutes=config['time_window_minutes']):
            count = i - window_start + 1
            if count > config['threshold_count']:
                alert = {
                    "alert_type": config['alert_title'],
                    "ip": ip,
                    "attempt_count": count,
                    "window_minutes": (events[i][0] - events[window_start][0]).seconds // 60,
                    "first_attempt": events[window_start][0].isoformat(),
                    "last_attempt": events[i][0].isoformat(),
                    "log_lines": [e[1] for e in events[window_start:i+1]],
                    "severity": "CRITICAL",
                    "recommendation": "BLOCK IP + INVESTIGATE"
                }
                alerts.append(alert)
                logging.warning(f"ALERT: {ip} → {count} attempts")
                break
        else:
            window_start += 1

# Expor JSON
with open(config['output_file'], 'w') as f:
    json.dump(alerts, f, indent=2)

# SEND EMAIL IF ALERT
if alerts:
    msg = EmailMessage()
    msg['Subject'] = f"[CRITICAL] {len(alerts)} Brute-Force Alert(s)"
    msg['From'] = config['email_from']
    msg['To'] = config['email_to']
    msg.set_content(f"""
    CRITICAL: Brute-force detected!
                    
    IP: {alerts[0]['ip']}
    Attemps: {alerts[0]['attempt_count']} in {alerts[0]['window_minutes']} mins
    First: {alerts[0]['first_attempt']}
    Last: {alerts[0]['last_attempt']}

    See attached alerts.json for full details
    """)

    # Attach JSON
    with open(config['output_file'], 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype="json", filename="alerts.json")

    # Send
    with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
        server.starttls()
        server.login(config['email_from'], config['email_password'])
        server.send_message(msg)

    logging.info(f"EMAIL SENT: {len(alerts)} alert(s) to {config['email_to']}")
else:
    logging.info("No alerts → no email sent.")