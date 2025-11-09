# Day 4: Lists + Loops - Dynamic Threat Alerts
print("=== SOC THREAT ALERT SYSTEM v0.1 ===\n")

# List of suspicious IPs (IOCs)
threat_ips = [
    '192.168.1.100', # Brute force
    '10.0.0.55',     # Port scan
    '203.0.113.27',  # Malware beaconing
    '198.51.100.5',  # C2 server
    '172.16.0.1'     # Data exfil
]

# Alert messages (parallel list)
alert_types = [
    'Brute force attempt',
    'Port scan detected',
    'Malware beaconing activity',
    'C2 communication active',
    'Data exfiltration in progress'
]

# Loop through IPs and print paired alerts
for i in range(len(threat_ips)):
    ip = threat_ips[i]
    alert = alert_types[i]
    print(f'ALERT: {alert} from IP {ip}')