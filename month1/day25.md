# Day 25 – Final Polish: One-Click Deploy + requirements.txt
**Date:** 2025-11-25  
**Focus:** Making the project instantly runnable by anyone  
**Time spent:** 35 minutes  

### What I Did
- Added `requirements.txt` (Flask + deps)
- Created `start_soc.sh v2` → **one command deploys full SIEM**
- Uses new `generate_logs.py` with CLI args
- **Zero setup** for recruiters

### One-Click Demo
```bash
git clone https://github.com/suleohis/cyber-blueprint-2026.git
cd cyber-blueprint-2026
./start_soc.sh