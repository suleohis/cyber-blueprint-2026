# month1/generate_logs.py – INJECT 5 FAILS IN 12 MINS
import random
from datetime import datetime, timedelta

log_lines = []
start_time = datetime(2025, 11, 1, 9, 0, 0)

# === FORCE BRUTE-FORCE: 5 FAILED LOGINS IN 12 MINS ===
brute_ip = "203.0.113.27"
brute_user = "charlie"
times = [0, 3, 6, 9, 12]  # minutes
for m in times:
    t = start_time + timedelta(minutes=m)
    log_lines.append(
        f"{t.strftime('%m/%d/%Y %I:%M:%S %p')} - "
        f"EventID: 4625 - Account: {brute_user} - Workstation: WKSTN-01 - "
        f"Source IP: {brute_ip} - failed to log on"
    )

# === ADD 10 NORMAL LOGS ===
for _ in range(10):
    t = start_time + timedelta(minutes=random.randint(15, 180))
    event = random.choice([4624, 4634])
    user = random.choice(["alice", "bob", "dave"])
    ip = f"192.168.1.{random.randint(10, 50)}"
    desc = "logged on" if event == 4624 else "logged off"
    log_lines.append(
        f"{t.strftime('%m/%d/%Y %I:%M:%S %p')} - "
        f"EventID: {event} - Account: {user} - Workstation: LAPTOP-03 - "
        f"Source IP: {ip} - {desc}"
    )

# Write
random.shuffle(log_lines)
with open('month1/fake_auth.log', 'w') as f:
    f.write("# Fake Auth Logs - BRUTE FORCE INJECTED (Day 9)\n")
    f.write("# 5 failed logins from 203.0.113.27 in 12 mins\n\n")
    for line in log_lines:
        f.write(line + "\n")

print("Injected brute-force → fake_auth.log")