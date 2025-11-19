#!/bin/bash

echo "🚀 Starting Nigeria's First Autonomous SOC..."
echo "🇳🇬 Built by suleohis"

# 1. Create folders
mkdir -p month1 screenshots templates

# 2. Setup cron automatically (idempotent - safe to run multiple times)
echo "[+] Setting up 24/7 detection (every 5 mins)..."
CURRENT_DIR=$(pwd)
CRON_CMD="*/5 * * * * cd \"$CURRENT_DIR\" && $(which python3) month1/run_detector.py >> month1/cron.log 2>&1"

# Add cron job if it doesn't exist
if ! crontab -l 2>/dev/null | grep -q "run_detector.py"; then
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✅ Cron installed - detection runs every 5 mins forever"
else
    echo "✅ Cron already installed"
fi

# 3. Run first detection
echo "[+] Running first detection cycle..."
python3 month1/run_detector.py || echo "⚠️ Detection failed (normal on first run)"

# 4. Start dashboard
echo "[+] Starting live dashboard..."
echo "📊 Open: http://127.0.0.1:5000"
python3 month1/app.py &

# 5. Success message
echo ""
echo "🎉 SOC IS LIVE!"
echo "📊 Dashboard: http://127.0.0.1:5000"
echo "🔄 Auto-detection: Every 5 mins"
echo "📧 Email alerts: Enabled"
echo "🚫 Auto-blocking: Enabled"
echo "📜 Logs: month1/cron.log"
echo ""
echo "Made in Nigeria 🇳🇬 by suleohis"
echo "Press Ctrl+C to stop dashboard"