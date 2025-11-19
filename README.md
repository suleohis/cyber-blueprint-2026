# Nigeria's First Autonomous SOC – Built in 30 Days 🇳🇬

A fully automated brute-force detection + response system:
- Parses SSH logs
- Detects attacks in real time
- Sends email alerts
- Live Flask dashboard with auto-refresh
- Auto-blocks IPs
- Archives history
- Runs 24/7 via cron
- One-click start

**Live Demo**: http://127.0.0.1:5000 (after you run it)

## Quick Start (60 seconds)

```bash
git clone https://github.com/suleohis/cyber-blueprint-2026.git
cd cyber-blueprint-2026
chmod +x start_soc.sh

# Option A: Full autonomous mode (recommended)
./start_soc.sh
# → Dashboard opens at http://127.0.0.1:5000
# → Detection runs every 5 minutes automatically

# Option B: Manual mode (no cron)
python3 month1/app.py

# This command auto-detects your username and python path
(crontab -l 2>/dev/null; echo "*/5 * * * * cd $(pwd) && $(which python3) month1/run_detector.py >> month1/cron.log 2>&1") | crontab -
