import re
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import argparse
import os

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
            alert = {
                'id': f"alert-{datetime.now().strftime('%Y%m%d%H%M%S')}-{ip.replace('.', '')}",
                "timestamp": datetime.now().isoformat(),
                "source_ip": ip,
                "attempts": len(timestamps),
                "first_seen": min(timestamps).isoformat(),
                "last_seen": max(timestamps).isoforma(),
                "severity": "CRITICAL" if len(timestamps) > 20 else "HIGH" if len(timestamps) > 10 else "MEDIUM",
                "detection_rule": "SSH Brute Force (15-min window)",
                "status": "new",
                "tags": ["bruteforce", "ssh", "auth"]
            }
            alerts.append(alert)
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

def load_blocked_ips():
    """Helper function – reads blocked_ips.txt (used by --block flag)"""
    blocked = []
    if os.path.exists('month1/blocked_ips.txt'):
        with open('month1/blocked_ips.txt', 'r') as f:
            blocked = [line.strip() for line in f if line.strip()]
    return blocked

# Main execution (CLI preview: python detector.py --threshold 5)
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="SSH Brute-Force Detecor - Cyber Blueprint 2026",
        epilog="Example: python3 detector.py --threshold  --window 15 --email"
    )
    parser.add_argument('--threshold', type=int, default=5, 
                        help="Miniumn failed attempts to trigger alert (default: 5)")
    parser.add_argument('--window', type=int, default=15, 
                        help="Time window minutes (default: 15)")
    parser.add_argument('--log', type=str, default='month1/fake_auth.log',
                        help='Path to auth log (default: month1/fake_auth.log)')
    parser.add_argument('--email', action='store_true',
                        help="Send email alert if threats detected")
    parser.add_argument('--block', action='store_true',
                        help='Auto-block worst offender in blocked_ips.txt')
    parser.add_argument('--dry-run', action='store_true',
                        help="Show alerts but do NOT write files or send email")
    args = parser.parse_args()

    print(f"[+] Scanning {args.log} | Threshold: {args.threshold} in {args.window}min")
    alerts = detect_anomalies(args.log, args.threshold, args.window)

    if alerts:
        print(f"[!!!] {len(alerts)} BRUTE-FORCE ATTACK(S) DETECTED")
        for a in alerts:
            print(f" → {a['source_ip']:15} | {a['attempts']:2} attempts | Severity: {a['severity']}")
        
        if not args.dry_run:
            export_alerts(alerts, 'month1/alerts.json')
            if args.email:
                send_email(alerts)
            if args.block:
                worst_ip = max(alerts, key=lambda x: x['attempts'])['source_ip']
                blocked = load_blocked_ips()
                if worst_ip not in blocked:
                    with open('month1/blocked_ips.txt', 'a') as f:
                        f.write(worst_ip + '\n')
                    print(f"[BLOCKED] {worst_ip} → added to blocked_ips.txt")
                else: 
                    print(f"[INFO] {worst_ip} already blocked")
    else:
        print("[+] All clear - no threats")

    if args.dry_run:
        print("[DRY-RUN] No changes made to disk or email")
        