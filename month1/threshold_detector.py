# Day 7: Brute-Force Threshold Detector
# Count failed logins (4625) per IP -> Alert if >3
print("=== BRUTE-FORCE THRESHOLD DETECTOR v0.1 ===\n")

from collections import defaultdict

failed_by_ip = defaultdict(int)
offending_lines = {}

with open('month1/fake_auth.log', 'r') as f:
    for line_num, line in enumerate(f,1):
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        if 'EventID: 4625' in line: 
            # Extract IP
            ip_start = line.find('Source IP: ') + 11
            ip_end = line.find(' ', ip_start)
            ip = line[ip_start:ip_end] if ip_end != -1 else line[ip_start:]

            failed_by_ip[ip] += 1
            if ip not in offending_lines:
                offending_lines[ip] = []
            offending_lines[ip].append(line_num)

# Threshold alerting
alerts = 0
print("BRUTE-FORCE ALERTS (Threshold: >3 failed loigns):\n")
for ip, count in sorted(failed_by_ip.items(), key=lambda x: x[1], reverse=True):
    if count > 3:
        alerts += 1
        lines = ', '.join(map(str, offending_lines[ip]))
        print(f"   [HIGH] IP: {ip} | Attempts: {count} | Log Lines: {lines}")        
    else:
        print(f"   [INFO] IP: {ip} | Attempts: {count}")

if alerts == 0:
    print("\nNo brute-force attempts detected.")
else:
    print(f"\n{alerts} IP(s) exceeded threshold. Recommend: BLOCK + INVESTIGATE.")

print(f"\nScanned 23 log lines. {len(failed_by_ip)} unique IPs attempted login.")