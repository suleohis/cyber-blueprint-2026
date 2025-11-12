from datetime import datetime, timedelta
from collections import defaultdict

print("=== 15-MIN BRUTE-FORCE WINDOW DETECOR v0.1 ===")

# Store: IP - list of (timestamp, line_number)
attempts = defaultdict(list)

# Parse timestamp format: "11/01/2025 09:45:00 AM"
TIME_FORMAT = '%m/%d/%Y %I:%M:%S %p'

with open('month1/fake_auth.log', 'r') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if line.startswith('#') or not line or '4625' not in line:
            continue
        
        # Extract timestamp
        time_str = line.split(' - ')[0]
        try:
            timestamp = datetime.strptime(time_str, TIME_FORMAT)
        except ValueError:
            continue

        # Extract IP
        ip_start = line.find('Source IP: ') + 11
        ip_end = line.find(' ', ip_start)
        ip = line[ip_start:ip_end] if ip_end != -1 else line[ip_start]

        attempts[ip].append((timestamp, line_num))

# Check 15-min window
alerts = 0
print("BRUTE-FORCE IN 15-MIN WINDOW (Threshold: >3):\n")

for ip, events in sorted(attempts.items(), key=lambda x: len(x[1]), reverse=True):
    events.sort(key=lambda x: x[0]) # Sort by time
    window_start = 0
    for i in range(2, len(events)): # Need at least 3
        if events[i][0] - events[window_start][0] <= timedelta(minutes=15):
            if i - window_start + i > 3:
                alerts += 1
                lines = ", ".join(str(e[1]) for  e in events[window_start:i+1])
                duration = events[i][0] - events[window_start][0]
                print(f"  [CRITICAL] IP: {ip}")
                print(f"      Attempts: {i - window_start + 1} in {duration}")
                print(f"      Lines: {lines}\n")
                break
        else: 
            window_start += 1

if alerts == 0:
    print("No brute-force detected in 15-minute window.")

print(f"Scanned {sum(len(e) for e in attempts.values())} failed login attempts.")