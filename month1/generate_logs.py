# Day 5: Generate Fake Windows Auth Log
# Output: fake_auth.log with 20 realistic Windows

import random
from datetime import datetime, timedelta

# Sample data
users = ['alice', 'bob', 'charlie', 'dave', 'eve']
workstations = ['WKSTN-01', 'WKSTN-02', 'LAPTOP-03', 'SERVER-01']
ips = ['192.168.1.100', '10.0.0.55', '203.0.113.27', "198.51.100.5", '172.16.0.1']
event_ids = [4624, 4625, 4634] # Success, Failed, Logoff
event_desc = {
    4624: 'An account was successfully logged on.',
    4625: 'An account failed to log on.',
    4634: 'An account was logged off.'
}

# Generate 20 log lines
log_lines = []
start_time = datetime(2025, 11, 1, 8, 0, 0)

for i in range(20):
    timestamp = start_time + timedelta(minutes=random.randint(0, 120))
    event = random.choice(event_ids)
    user = random.choice(users)
    workstation = random.choice(workstations)
    ip = random.choice(ips) if event == 4625 else "192.168.1." + str(random.randint(10, 50))

    log_line = (
        f"{timestamp.strftime('%m/%d/%Y %I:%M:%S %p')} - "
        f"EventID: {event} - "
        f"Account: {user} - "
        f"Workstation: {workstation} - "
        f"Source IP: {ip} - "
        f"{{event_desc[event]}}"
    )
    log_lines.append(log_line)

# Write to file
with open('month1/fake_auth.log', 'w') as f:
    f.write("# Fake Windows Auth Logs - Generated Day 5\n")
    f.write('# Format: MM/DD/YYYY HH:MM:SS AM/PM - EventID: XXXX - Account: user - Workstation: XXX - Source IP: X.X.X.X - Description\n\n')
    for line in log_lines:
        f.write(line + '\n')

print("Generated 20 fake auth logs - month1/fake_auth.log")