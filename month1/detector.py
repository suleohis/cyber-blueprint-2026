import re
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import argparse

# Config (make these variables for eas tweaking)
LOG_FILE = 'fake_auth.log'
ALERTS_FILE  = 'alerts.json'
EMAIL_FROM = 'suleephraim1@gmail.com'
EMAIL_TO = 'cyberlootkeeper@gmail.cm'
EMAIL_PASSWORD = 'uwijddtfwdtmmony'
THRESHOLD = 5
WINDOW_MINUTES = 15 

def parse_line(line):
    """Parse a single log line for timestamp, IP, and event. Returns dict or None if invalid."""
    # Regex from Day 2 (Ch.9, pp. 185-200): Matches timestamp, IP, user, port
    pattern = r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+\S+\s+sshd$$ \d+ $$:\s+(Failed password for \S+ from )(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port \d+ ssh2'
    match = re.search(pattern, line.strip())
    if match:
        ts_str, _, ip = match.group()
        # Parse timestamp to datetime object
        ts = datetime.strptime(ts_str, '%b %d %H:%M:%S')
        ts = ts.replace(year=datetime.now().year) # Assume current year
        return {'timestamp': ts, 'ip': ip, 'event': 'failed_login'}
    return None

def detect_anomalies(log_file, threshold=THRESHOLD, window_minutes=WINDOW_MINUTES):
    """Scan log for anomalies in sliding time window. Returns list of alert dicts."""
    alerts = []
    fails_by_ip = {}  # Dict: IP -> list of timestamps
    cutoff = datetime.now() - timedelta(minutes=window_minutes)

    with open(log_file, 'r') as f:
        for line in f:
            parsed = parse_line(line)
            if parsed and parsed['timestamp'] > cutoff:
                ip = parsed['ip']
                if ip not in fails_by_ip:
                    fails_by_ip[ip] = []
                fails_by_ip[ip].append(parsed['timestamp'])
    
    # Check thresholds
    for ip, timestamps in fails_by_ip.items():
        if len(timestamps) >= threshold:
            alerts.append({
                'ip':ip,
                'count':len(timestamps),
                'first_seen':min(timestamps),
                'last_seen': max(timestamps),
                'severity': "HIGH" if len(timestamps) > 10 else "MEDIUM"
            })
    return alerts

def export_alerts(alerts, file=ALERTS_FILE):
    """Export alerts to JSON (from Day 4, Ch.18 pp. 439-450)."""
    with open(file, 'w') as f:  
        json.dump(alerts, f, default=str, indent=4) # default=str for datetime serialization

def send_email(alerts, from_email=EMAIL_FROM, to_email=EMAIL_TO, password=EMAIL_PASSWORD):
    """Send email alert via Gmail SMTP (from Day 5, Ch.20 pp. 481-490). Returns True if sent."""
    if not alerts:
        return False
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f'SOC Alert: {len(alerts)} Brute Force Attempts Detected'

    body = 'High-severity alerts:\n\n'
    for alert in alerts:
        body += f"- IP {alert['ip']}: {alert['count']} fails from {alert['first_seen']} to {alert['last_seen']} (Severity: {alert['severity']})\n"
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            print(f"Email sent for {len(alerts)}")
            return True
        except Exception as e:
            print(f"Email failed: {e}")
            return False

# Main execution (CLI preview: python detector.py --threshold 5)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Detect log anomalies.")
    parser.add_argument('--threshld', type=int, default=THRESHOLD, help="Fail threshold")
    parser.add_argument('--window', type=int, default=WINDOW_MINUTES, help="Time window mins")
    args = parser.parse_args()

    alerts = detect_anomalies(LOG_FILE, args.threshold, args.window)
    if alerts:
        export_alerts(alerts)
        send_email(alerts)
        print(f"Dectected {len(alerts)} anomalies.")
    else:
        print("No anomalies detected.")