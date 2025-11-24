# Day 22 – Dictionaries & Rich Alert Objects  
**Date:** 2025-11-24  
**Focus:** Chapter 7 – Dictionaries and Structuring Data (pp. 139–158)  
**⏱ Time spent:** 30 minutes  
**✅ Resource:** Automate the Boring Stuff 3rd Edition – Ch.7  

### What I Did  
- Refactored alert creation inside `detector.py`  
- Switched from flat lists to **rich dictionary objects** with consistent schema  
- Added unique alert IDs, ISO timestamps, severity tiers, detection rule name, status, and MITRE-style tags  

### Key Code Change (detect_anomalies())
```python
alert = {
    "id": f"alert-{datetime.now():%Y%m%d%H%M%S}-{ip.replace('.', '')}",
    "timestamp": datetime.now().isoformat(),
    "source_ip": ip,
    "attempts": len(timestamps),
    "first_seen": min(timestamps).isoformat(),
    "last_seen": max(timestamps).isoformat(),
    "severity": "CRITICAL" if len(timestamps)>20 else "HIGH" if len(timestamps)>10 else "MEDIUM",
    "detection_rule": "SSH Brute Force (15-min window)",
    "status": "new",
    "tags": ["bruteforce", "ssh", "auth"]
}