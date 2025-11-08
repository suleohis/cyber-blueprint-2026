ip_brute = '192.168.1.100'
ip_scan = '10.0.0.55'
ip_malware = '203.0.113.2'
ip_c2 = '198.51.100.5'
ip_exfil = '172.16.0.1'

print("ALERT: Brute force attempt from", ip_brute)
print("ALERT: Port scan detected from", ip_scan)
print("ALERT: Malware beaaconing to", ip_malware)
print("ALERT: C2 communication with", ip_c2)
print("ALERT: Data exfil to", ip_exfil)