# SSH Brute-Force Regex Cheat Sheet – Cyber Blueprint 2026
**Author:** suleohis | **Last updated:** 2025-11-24

### 1. Basic Failed Login (most common)
```regex
Failed password for .* from (\d+\.\d+\.\d+\.\d+) port

Failed password for invalid user .* from (\d+\.\d+\.\d+\.\d+)

Accepted password for .* from (\d+\.\d+\.\d+\.\d+) port

Failed password for root from (\d+\.\d+\.\d+\.\d+)

^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*sshd.*Failed password for\s+(?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)

→ Group 1 = timestamp
→ Group 2 = username
→ Group 3 = source IP

Did not receive identification string from (\d+\.\d+\.\d+\.\d+)

pam_unix$$ sshd:auth $$: authentication failure;.*rhost=(\d+\.\d+\.\d+\.\d+)

Quick bash one-liner to find top attackers
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' fake_auth.log | sort | uniq -c | sort -nr

pattern = r'Failed password for .* from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port'
ip = re.search(pattern, line).group(1)

pattern = r'Failed password for .* from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port'
ip = re.search(pattern, line).group(1)
```