# run_detector.py - runs full pipeline automatically
import os
import subprocess
import json
from datetime import datetime

# 1. Run detection
subprocess.run(["python3", "month1/detect_and_export.py"])

# 2. Run email if alerts exist
if os.path.exists('month1/alerts.json'):
    with open('month1/alerts.json') as f:
        if json.load(f): # if not empty
            subprocess.run(["python3", "month1/email_alerts.py"])

print(f"[{datetime.now()}] Detection cycle complete")