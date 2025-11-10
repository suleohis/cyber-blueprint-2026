# Day 6: Parse fake_auth.log -> Detect Failed Logins (EventID 4625)
print("=== FAILED LOGIN DETECTION v0.1 ===\n")

failed_logins = []
with open('month1/fake_auth.log', 'r') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        # Skip comments and empty lines
        if line.startswith('#') or not line:
            continue
        # Look for 4625
        if 'EventID: 4625' in line:
            # Extract IP
            ip_start = line.find('Source IP: ') + 11
            ip_end = line.find(' ', ip_start)
            ip = line[ip_start:ip_end] if ip_end != -1 else line[ip_start:]
            # Extract User
            user_start = line.find('Account: ') + 9
            user_end = line.find(' - ', user_start)
            user = line[user_start:user_end] if user_end != -1 else 'unkown'

            failed_logins.append((user, ip, line_num))

# Print report
if failed_logins:
    print(f"ALERT: {len(failed_logins)} FAILED LOGIN ATTEMPT(S) DETECTED!\n")
    for user, ip, line_num in failed_logins:
        print(f"  - User: {user} | From IP: {ip} | Log Line: {line_num}") 
else:
    print("No failed logins detected. System secure.")

print(f"\nScanned {line_num} total log lines.")           