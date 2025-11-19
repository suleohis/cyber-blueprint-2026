# Day 10: Config-Driven Brute-Force Detector + JSON Export
import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import os

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

logging.info("=== BRUTE-FORCE DETECTOR STARTED ===")
logging.info(f'Config: {config}')

attempts = defaultdict(list)
TIME_FORMAT = "%m/%d/%Y %I:%M:%S %p"

try:
    with open(config['log_file'], 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line.startswith('#') or not line or '4625' not in line:
                continue
            time_str = line.split(' - ')[0]
            try:
                timestamp = datetime.strptime(time_str, TIME_FORMAT)
            except ValueError:
                logging.warning(f"Bad timestamp at line {line_num}: {time_str}")
                continue
            ip_start = line.find('Source IP: ') + 11
            ip_end = line.find(' ', ip_start)
            ip = line[ip_start:ip_end] if ip_end != -1 else line[ip_start:]
            attempts[ip].append((timestamp, line_num))
    logging.info(f"Parsed {sum(len(v) for v in attempts.values())} failed logins")
except FileNotFoundError:
    logging.error(f"Log file not found: {config['log_file']}")
    exit(1)

# Detect
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
                logging.warning(f"ALERT: {ip} → {count} attempts in window")
                break
        else:
            window_start += 1

# Export
os.makedirs(os.path.dirname(config['output_file']), exist_ok=True)
with open(config['output_file'], 'w') as f:
    json.dump(alerts, f, indent=2)

logging.info(f"Exported {len(alerts)} alert(s) to {config['output_file']}")
if alerts:
    logging.info(f"Sample: {json.dumps(alerts[0], indent=2)}")
else:
    logging.info("No alerts generated.")

# At the very end, after writing alerts.json
BLOCKED_IPS_FILE = 'month1/blocked_ips.txt'

with open(BLOCKED_IPS_FILE, 'a') as f:
    for alert in alerts:
        f.write(alert['ip'] + '\n')