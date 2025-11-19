#!/bin/bash
echo "Staring Nigeria's First Autonomous SOC..."

# 1. Create required folders
mkdir -p screenshots

# 2. Run dashboard in background
echo "[+] Starting Flask dashboard..."
python3 month1/app.py &

# 3. Run detection once to test
echo "[+] Runnig firs detection..."
python3 month1/run_detector.py

# 4. Final message
echo ""
echo "SOC IS LIVE!"
echo "Dashboard → http://127.0.0.1:5000"
echo "Auto-detection every 5 mins via cron"
echo "Made in Nigeria 🇳🇬 by suleohis"
echo "