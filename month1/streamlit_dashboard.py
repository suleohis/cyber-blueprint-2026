#! /usr/bin/env python3
import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cyber Blueprint SIEM", layout="wide")
st.title("Cyber Blueprint 2026 - Mini-SIEM")
st.sidebar.header("Controls")

if st.sidebar.button("Run Detection Now"):
    from detector import detect_anomalies, export_alerts, send_email
    alerts = detect_anomalies('month1/fake_auth.log')
    export_alerts(alerts, "month1/alerts.json")
    if alerts:
        send_email(alerts)
    st.success(f"Detection complete – {len(alerts)} alerts")

# Load alerts
try:
    with open("month1/alerts.json") as f:
        alerts = json.load(f)
    df = pd.DataFrame(alerts)
except:
    df = pd.DataFrame()

if not df.empty:
    st.subheader(f"Active Alerts ({len(df)})")
    st.dataframe(df[["source_ip", "attempts", "severity", "first_seen", "last_seen"]], use_container_width=True)

    st.bar_chart(df["severity"].value_counts())
    st.line_chart(df.groupby("source_ip")["attempts"].sum().sort_values(ascending=False).head(10))
else:
    st.info("No active alerts – all clear")

st.caption("Built by suleohis – Cyber Blueprint 2026")
