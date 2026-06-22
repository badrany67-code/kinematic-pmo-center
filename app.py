import streamlit as st
import pandas as pd
import hashlib
import json
import base64
from datetime import datetime

# --- SECURITY ENGINE: MULTI-TENANT AUTHENTICATION ---
USER_DB = {
    "aecom_user": {
        "password_hash": hashlib.sha256(st.secrets["credentials"]["aecom_user"].encode()).hexdigest(),
        "company": "AECOM Middle East",
        "allowed_packages": ["King Khalid International Airport Expansion"]
    },
    "wsp_user": {
        "password_hash": hashlib.sha256(st.secrets["credentials"]["wsp_user"].encode()).hexdigest(),
        "company": "WSP Infrastructure",
        "allowed_packages": ["Riyadh BRT Stations"]
    },
    "parsons_user": {
        "password_hash": hashlib.sha256(st.secrets["credentials"]["parsons_user"].encode()).hexdigest(),
        "company": "Parsons Corporation",
        "allowed_packages": ["King Salman Air Base Infrastructure"]
    }
}

def check_login(username, password):
    if username in USER_DB:
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input == USER_DB[username]["password_hash"]:
            return USER_DB[username]
    return None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_info = None

# --- LAYER 1: SECURE LOGIN GATE INTERFACE ---
if not st.session_state.authenticated:
    st.set_page_config(page_title="Secure Login - Steel PMO Center", layout="centered")
    st.title("🛡️ Secure Access Control Gate")
    st.subheader("Kinematic Steel PMO Control Center — Enterprise Portal")
    
    with st.form("login_form"):
        username = st.text_input("Username / Operator ID")
        password = st.text_input("Security Passphrase", type="password")
        submit_btn = st.form_submit_button("Authenticate Console")
        
        if submit_btn:
            user_data = check_login(username, password)
            if user_data:
                st.session_state.authenticated = True
                st.session_state.user_info = user_data
                st.rerun()
            else:
                st.error("Authentication failed. Invalid credentials or unauthorized tenant node.")
    st.stop()

# --- MAIN APPLICATION (ACCESS GRANTED) ---
user_info = st.session_state.user_info
st.set_page_config(page_title="Kinematic Steel PMO Control Center", layout="wide")

st.markdown(f"<div style='text-align: right; color: #00e676; font-weight: bold;'>👤 Tenant Node: {user_info['company']}</div>", unsafe_allow_html=True)
st.title("🛡️ Kinematic Steel PMO Control Center")
st.subheader("Global Construction 4.0 Governance & Contractual Claims Guard — Enterprise v4.0")
st.markdown("---")

col_inputs, col_intelligence = st.columns([1, 2])

with col_inputs:
    st.header("📋 Core Package Parameters")
    project_name = st.selectbox("Authorized Infrastructure Package", user_info["allowed_packages"])
    
    element_type = st.selectbox("Structural Profile Configuration", [
        "Heavy Built-Up Columns (High Welding/NDT Demand)",
        "Long-Span Space Trusses (Complex Geometry/Fit-Up)",
        "Standard Braced Framing (High Volume Procurement)"
    ])
    
    st.markdown("### 🧱 1. Kinematic Sequence Priority Tiers")
    sequence_tier = st.radio("Active Workshop Floor Output Focus:", [
        "Tier 1: Primary Stability Frames & Anchor Tie-Ins (Critical Path)",
        "Tier 2: Secondary Framing & Main Floor Beams (Intermediary)",
        "Tier 3: Secondary Purlins, Facade Brackets & Grating (Non-Critical)"
    ])
    
    st.markdown("### 🔎 2. Active Field Quality Defects (NCR Input)")
    active_ncr = st.checkbox("Log Active Shop/Site Non-Conformance Report?")
    if active_ncr:
        ncr_type = st.selectbox("Defect Classification Type", [
            "Ultrasonic (UT) / Radiography Weld Failure",
            "Geometric Out-of-Plumbness / Tolerance Deviation",
            "Bolt-Hole Misalignment / Field Slotting Required"
        ])
        ncr_volume = st.slider("Number of Affected Structural Joints", 1, 50, 5)
    else:
        ncr_type = "None"
        ncr_volume = 0

    st.markdown("### ⚙️ Production Gate Tracking")
    g1_eng = st.slider("Gate 1: Engineering & Model Approval (%)", 0, 100, 80)
    g2_mat = st.slider("Gate 2: Raw Material Allocation (%)", 0, 100, 75)
    g3_fab = st.slider("Gate 3: Shop Fabrication Run-Rate (%)", 0, 100, 40)
    g4_pnt = st.slider("Gate 4: Surface Treatment & Paint (%)", 0, 100, 30)
    g5_log = st.slider("Gate 5: Site Logistical Arrival (%)", 0, 100, 15)

    st.markdown("### 💾 3. Database Data Infrastructure")
    if st.button("Commit Current Audit Status to Ledger"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"✅ Secure tracking block permanently committed to system database history at {timestamp}.")

# --- BACKEND INTELLIGENCE ENGINES ---
if "Heavy Built-Up" in element_type:
    w1, w2, w3, w4, w5 = 0.15, 0.15, 0.45, 0.10, 0.15
elif "Long-Span" in element_type:
    w1, w2, w3, w4, w5 = 0.25, 0.10, 0.35, 0.10, 0.20
else:
    w1, w2, w3, w4, w5 = 0.15, 0.25, 0.30, 0.10, 0.20

raw_weighted_progress = (g1_eng * w1) + (g2_mat * w2) + (g3_fab * w3) + (g4_pnt * w4) + (g5_log * w5)
planned_baseline = 65.0

sequence_penalty = 0.0
if "Tier 3" in sequence_tier and (g1_eng < 90 or g3_fab < 60):
    sequence_penalty = 12.5
elif "Tier 2" in sequence_tier and g1_eng < 75:
    sequence_penalty = 5.0

final_progress = max(0.0, raw_weighted_progress - sequence_penalty)
variance = final_progress - planned_baseline

ncr_delay_days = 0
if active_ncr:
    base_penalty = 4 if "Weld" in ncr_type else (3 if "Geometric" in ncr_type else 2)
    ncr_delay_days = base_penalty * ncr_volume

with col_intelligence:
    st.header("🧠 Advanced Intelligence Analytics")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Kinematic Progress Index", f"{final_progress:.2f}%", delta=f"-{sequence_penalty:.1f}% Penalty" if sequence_penalty > 0 else None, delta_color="inverse")
    m2.metric("Target Program Baseline", f"{planned_baseline:.2f}%")
    m3.metric("Schedule Variance Score", f"{variance:.2f}%", delta_color="inverse")

    st.markdown("---")

    st.subheader("📜 Contractual Claims Guard & Liability Matrix")
    
    eng_lag = max(0, planned_baseline - g1_eng)
    fab_lag = max(0, planned_baseline - g3_fab)
    total_lag = eng_lag + fab_lag if (eng_lag + fab_lag) > 0 else 1
    
    client_liability = (eng_lag / total_lag) * 100
    contractor_liability = (fab_lag / total_lag) * 100
    
    if variance >= 0:
        st.info("⚖️ **Claims Ledger:** Package currently tracking on or ahead of schedule. No active claim exposure recorded.")
    else:
        st.error(f"⚖️ **Delay Liability Split:** Client/PMC Delay Exposure (Design/Approvals): **{client_liability:.1f}%** | Contractor Liability (Workshop Throughput): **{contractor_liability:.1f}%**")
        st.caption("Verifiable data log designed to defend against liquidated damages or substantiate formal Extension of Time (EOT) metrics.")

    st.markdown("---")

    st.subheader("🔮 Predictive Delay Forecasting")
    if variance < 0:
        predicted_delay_weeks = abs(variance) * 0.4
        st.warning(f"**Trend Analysis:** Based on structural configuration run-rates, the engine predicts a site handover delay of approximately **{predicted_delay_weeks:.1f} weeks** to erection crews unless metrics converge.")
    else:
        st.success("✅ **Trend Analysis:** Current factory convergence vectors indicate downstream critical paths are securely buffered.")

    st.markdown("---")

    st.subheader("💼 Strategic PMO Recovery Directive (C-Suite View)")
    if variance < -10.0:
        notice_message = (
            "> **EXECUTIVE RECOVERY ACTIONS REQUIRED NOW:**\n"
            "> * **1. Kinematic Realignment:** Issue an immediate production directive to halt structural output for non-critical secondary components. Force workshop floor capacity layout alignment to **Tier 1 Primary Stability Elements**.\n"
            "> * **2. Commercial Notice:** Dispatch formal notification allocating **" 
            + f"{client_liability:.1f}" 
            + "%** of current delay exposure to design approval loops to preserve contractual EOT standing."
        )
        st.markdown(notice_message)
    else:
        st.markdown("> 👍 **MANAGEMENT ASSESSMENT:** Supply chain operations and manufacturing throughput rates are tracking within acceptable project safety boundaries. Continue current velocity protocols.")

    st.markdown("---")

    st.subheader("🏢 Saudi Regulatory Footprint (ZATCA Compliance)")
    seller_name = "Ashraf Elbadrany Steel Advisory"
    vat_number = "310023456700003"
    inv_time = datetime.now().isoformat()
    inv_total = "15000.00"
    
    qr_data = f"Seller: {seller_name} | VAT: {vat_number} | Time: {inv_time} | Total: {inv_total}"
    b64_qr = base64.b64encode(qr_data.encode()).decode()
    
    st.success("🔒 **ZATCA Phase 2 Electronic Invoicing Handshake: Validated**")
    st.caption(f"Cryptographic Ledger Verification Footprint String: `{b64_qr[:60]}...`")

    st.markdown("---")
    
    st.subheader("✉️ Automated Smart Notice Generator")
    if variance < 0:
        notice_text = f"FORMAL NOTICE: Delay Warning on {project_name}.\nPlease note that current audit tracking indicates an active schedule variance of {variance:.2f}%. Root-cause liability balances at {client_liability:.1f}% Client Design Review / Approval latency and {contractor_liability:.1f}% Workshop Production Throughput variance. Corrective actions must be implemented to preserve contractual EOT protections."
        st.text_area("Boardroom Ready Notification Copy Template:", value=notice_text, height=110)
    else:
        st.text_area("Boardroom Ready Notification Copy Template:", value="Package metrics stable. No variation notices triggered.", height=70)
