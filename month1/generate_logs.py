#! /usr/bin/env python3
"""
Windows Failed Logon (EventID 4625) Generator – Cyber Blueprint 2026
Now with full CLI arguments – safe upgrade for Month 1

Usage:
    python generate_logs.py                 → 1 brute-force burst (your original)
    python generate_logs.py 5               → 5 separate brute-force attacks
    python generate_logs.py 10 --normal 20  → 10 attacks + 20 normal logons
"""

import random
from datetime import datetime, timedelta
import argparse
import os

def generate_brute_force_burst(start_time, ip="203.0.113.27", user="charlie"):
    """Generate exactly 5 failed logons in 12 minutes (your original pattern)"""
    lines = []
    times = [0, 3, 6, 9, 12]
    for m in times:
        t = start_time + timedelta(minutes=m)
        line = (
            f"{t.strftime('%m/%d/%Y %I:%M:%S %p')} -"
            f"EventID: 4625 - Account: {user} - Workstation: WKSTN-01 -"
            f"Source IP: {ip} - failed to log on"
        )
        lines.append(line)
    return lines

def generate_normal_logons(count=10, start_time=None):
    """Generate random successful logons/logoffs"""
    if start_time is None:
        start_time = datetime.now()
    lines = []
    for _ in range(count):
        t = start_time + timedelta(minutes=random.randint(15, 100))
        event = random.choice([4624, 4634]) # 4624 = logon, 4632  logoff
        user = random.choice(["alice", "bob", "dave", "john", "sarah"])
        ip = f"192.168.1.{random.randint(10, 50)}"
        desc = "logged on" if event == 4624 else "logged off"
        line = (
            f"{t.strftime('%m/%d/%Y %I:%M:%S %p')} - "
            f"EventID: {event} - Account: {user} - Workstation: LAPTOP-03 - "
            f"Source IP: {ip} - {desc}"
        )
        lines.append(line)
    return lines

def main():
    parser = argparse.ArgumentParser(
        description="Generate Windows Event Log 4625 brute-force attacks",
        epilog="Example: python generate_logs.py 8 --normal 30"
    )
    parser.add_argument(
        "bursts", nargs="?",  type=int, default=1,
        help="Number of brute-force bursts to generate (default: 1)"
    )
    parser.add_argument(
        "--normal", type=int, default=10,
        help="Number of nomral (non-attack) logon/logoff events (default: 10)"
    )
    parser.add_argument(
        "--ip", type=str, default="203.0.113.27",
        help="Attacker IP for brute-force (default: 203.0.113.27)"
    )
    parser.add_argument(
        "--user", type=str, default="charlie",
        help="Target username for attack (default: charlie)"
    )
    args = parser.parse_args()

    # Ensure month1 folder exists
    os.makedirs("month1", exist_ok=True)

    all_lines = []
    base_time = datetime(2025, 11, 1, 9, 0, 0)

    # Generate requested number of brute-force bursts
    for i in range(args.bursts):
        offset = 1 * 30 # space them 30 minuttes apart
        burst_time = base_time + timedelta(minutes=offset)
        all_lines.extend(generate_brute_force_burst(burst_time, args.ip, args.user))

    # Add normal background noise
    all_lines.extend(generate_normal_logons(args.normal, base_time))

    # Shuffe so attacks aren't perfectly sequential
    random.shuffle(all_lines)

    # Write to file
    log_path = "month1/fake_auth.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("# Fake Windows Auth Logs - BRUTE FORCE INJECTED\n")
        f.write(f"# Generated: {args.bursts} attack burst(s) + {args.normal} normal events\n")
        f.write(f"# Attacker: {args.ip} targeting user '{args.user}'\n\n")
        for line in all_lines:
            f.write(line + "\n")
    
    print(f"Generated {len(all_lines)} log lines → {log_path}")
    print(f"    {args.bursts} brute-force burst(s) from {args.ip}")
    print(f"    {args.normal} normal background events")


if __name__ == "__main__":
    main()
