import streamlit as st
import joblib
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Suspicious Login Pattern Detector",
    page_icon="🛡️",
    layout="wide"
)

# 2. Data Mapping
# This handles the logic for dependent dropdowns
location_data = {
    "India": ["Jio", "Airtel", "Vodafone-Idea", "Unknown/VPN"],
    "Romania (High Risk)": ["DIGI RO (High Risk)", "Orange Romania", "Telekom RO", "Unknown/VPN"],
    "United States": ["AT&T", "Verizon", "Comcast", "Unknown/VPN"],
    "Brazil": ["Vivo", "Claro", "TIM Brasil", "Unknown/VPN"]
}

# 3. Load the "Brain"
@st.cache_resource
def load_model_assets():
    model = joblib.load('models/account_takeover_detector.joblib')
    features = joblib.load('models/model_features.joblib')
    return model, features

try:
    model, model_features = load_model_assets()
except Exception as e:
    st.error(f"Error loading model: {e}. Check your /models folder.")
    st.stop()

# 4. Sidebar Inputs
st.sidebar.header("🛡️ Login Simulation")
st.sidebar.write("Adjust parameters to test the AI's detection capability.")

selected_country = st.sidebar.selectbox("Select Origin Country", list(location_data.keys()))
available_isps = location_data[selected_country]
selected_isp = st.sidebar.selectbox("Select ISP Provider", available_isps)

browser = st.sidebar.selectbox(
    "Browser Fingerprint", 
    ["Chrome 122 (Modern)", "Chrome 79.0.3945 (Bot Signature)", "Firefox 115 (Stable)"]
)
time_of_day = st.sidebar.slider("Login Hour (24h format)", 0, 23, 14)
device = st.sidebar.radio("Device Type", ["Desktop", "Mobile", "Tablet"])

# 5. Main Dashboard Area
st.title("🛡️ Suspicious Login Pattern Detector")
st.markdown(f"**Current Monitor:** Analyzing traffic from **{selected_country}** via **{selected_isp}**")
st.markdown("---")

# 6. Transformation Logic
is_ro = 1 if "Romania" in selected_country else 0
is_bot = 1 if "Bot Signature" in browser else 0
is_dirty_asn = 1 if "High Risk" in selected_isp or "VPN" in selected_isp else 0
is_night = 1 if (time_of_day >= 23 or time_of_day <= 5) else 0

is_desktop = 1 if device == "Desktop" else 0
is_mobile = 1 if device == "Mobile" else 0

input_data = {
    'is_high_risk_country': is_ro,
    'is_night_login': is_night,
    'is_bot_browser': is_bot,
    'is_attack_asn': is_dirty_asn,
    'Device Type_desktop': is_desktop,
    'Device Type_mobile': is_mobile
}

# Ensure final format matches model expectations
input_df = pd.DataFrame([input_data]).reindex(columns=model_features, fill_value=0)

# 7. Execution and Display
if st.button("🚀 Execute Threat Analysis"):
    probs = model.predict_proba(input_df)[0]
    threat_prob = probs[1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Threat Probability Score", f"{threat_prob*100:.2f}%")
        st.progress(threat_prob)
        
    with col2:
        if threat_prob > 0.5:
            st.error("⚠️ HIGH RISK DETECTED: ACCESS DENIED")
            st.warning("Action: Pattern matches known botnet fingerprints.")
        else:
            st.success("✅ LOW RISK: ACCESS GRANTED")
            st.info("Action: Routine login behavior detected.")
            
    st.markdown("### 📊 AI Reasoning Analysis")
    st.write(f"The model analyzed **{len(model_features)}** features. It assigned the highest weight to the **{browser}** signal.")