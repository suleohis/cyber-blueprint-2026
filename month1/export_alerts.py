# Day 9: Export Brute-Force Alerts to JSON
import json
from datetime import datetime, timedelta
from collections import defaultdict

print("=== ALERT EXPORTER v0.1 ===\n")

attempts = defaultdict(list)
alerts = []

TIME_FORMAT = "%m/%d/%Y %I:%M:%S %p"

with open('month1/fake_auth.log', 'r') as f:
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

# Detect 15-min window
for ip, events in attempts.items():
    events.sort(key=lambda x: x[0])
    window_start = 0
    for i in range(2, len(events)):
        if events[i][0] - events[window_start][0] <= timedelta(minutes=15):
            if i - window_start + 1 > 3:
                alert = {
                    "alert_type": "BRUTE_FORCE_15MIN",
                    "ip": ip,
                    "attempt_count": i - window_start + 1,
                    "window_minutes": (events[i][0] - events[window_start][0]).seconds // 60,
                    "first_attempt": events[window_start][0].isoformat(),
                    "last_attempt": events[i][0].isoformat(),
                    "log_lines": [e[1] for e in events[window_start:i+1]],
                    "severity": "CRITICAL",
                    "recommendation": "BLOCK IP + INVESTIGATE"
                }
                alerts.append(alert)
                break
        else:
            window_start += 1

# Export to JSON
with open('month1/alerts.json', 'w') as f:
    json.dump(alerts, f, indent=2)

print(f"Exported {len(alerts)} CRITICAL alert(s) to month1/alerts.json")
if alerts:
    print("\nSample Alert:")
    print(json.dumps(alerts[0], indent=2))
else:
    print("No alerts generated.")