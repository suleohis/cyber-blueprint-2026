#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime

st.set_page_config(page_title="Cyber Blueprint SIEM", layout="wide")
st.title("Cyber Blueprint 2026 – Real-Time SIEM")
st.markdown("**Windows EventID 4625 Brute-Force Detection** | Built by suleohis")

# ——— RUN DETECTION BUTTON ———
if st.sidebar.button("Run Detection Now", type="primary", use_container_width=True):
    with st.spinner("Running detection engine..."):
        try:
            from detector import detect_anomalies, export_alerts, send_email

            alerts = detect_anomalies("month1/fake_auth.log", threshold=3, window_minutes=60)
            export_alerts(alerts, "month1/alerts.json")

            if alerts:
                send_email(alerts)
                st.success(f"ALERT: {len(alerts)} brute-force attack(s) detected & email sent!")
            else:
                st.success("Scan complete – no threats found")
        except Exception as e:
            st.error(f"Error: {e}")

# ——— LOAD ALERTS SAFELY ———
alerts_file = "month1/alerts.json"
df = pd.DataFrame()

if os.path.exists(alerts_file):
    try:
        with open(alerts_file, "r") as f:
            data = json.load(f)
        if data:
            df = pd.DataFrame(data)
            # Ensure required columns exist
            required = ["source_ip", "attempts", "severity", "first_seen", "last_seen"]
            for col in required:
                if col not in df.columns:
                    df[col] = "N/A"
        else:
            st.info("No alerts recorded yet.")
    except Exception as e:
        st.error(f"Failed to load alerts: {e}")
else:
    st.info("No alerts.json found – click **Run Detection Now**")

# ——— DISPLAY ———
if not df.empty:
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"Active Alerts ({len(df)})")
        display_cols = ["source_ip", "attempts", "severity", "first_seen", "last_seen"]
        st.dataframe(
            df[display_cols].sort_values("attempts", ascending=False),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.metric("Total Alerts", len(df))
        blocked_file = "month1/blocked_ips.txt"
        blocked_count = len([l for l in open(blocked_file) if l.strip()]) if os.path.exists(blocked_file) else 0
        st.metric("IPs Blocked", blocked_count)
        st.metric("Threat Level", df["severity"].iloc[0] if len(df) > 0 else "LOW")

    # ——— ATTACKS PER HOUR CHART ———
    try:
        df['hour'] = pd.to_datetime(df['first_seen']).dt.floor('h')
        chart_data = df.groupby('hour').size()

        fig, ax = plt.subplots(figsize=(10, 6))
        chart_data.plot(kind='bar', ax=ax, color='#ff4444', edgecolor='black')
        ax.set_title("Brute-Force Attacks Per Hour", fontsize=16, fontweight='bold')
        ax.set_ylabel("Number of Attacks")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    except:
        st.warning("Not enough data for timeline chart yet.")

else:
    st.success("All clear – no active threats detected")
    st.balloons()

st.caption("Run `./start_soc.sh` · Refresh page · Real-time SOC in Python")