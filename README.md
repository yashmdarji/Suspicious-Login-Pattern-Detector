# AI-Powered Account Takeover Detection

### The Challenge
How do you identify 141 malicious logins hidden among 94,000 legitimate sessions? In this project, I processed a 9 GB cybersecurity dataset to build a real-time threat detection system.

### Key Discoveries
- **The Romanian Botnet:** EDA revealed that 56% of successful takeovers originated from Romania (Country Code: RO).
- **Browser Fingerprinting:** A specific, outdated version of Chrome (79.0.3945.192.218) was used in 60% of all attacks.
- **Infrastructure:** Attacks were clustered within specific ASNs (ISPs) often associated with VPS/VPN services.

### The Solution
I engineered 4 custom behavioral features:
1. `is_high_risk_country`
2. `is_bot_browser`
3. `is_night_login`
4. `is_attack_asn`

I trained a **Random Forest Classifier** that achieved **95% Precision** and a solid recall for detecting successful account takeovers.

### How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the real-time detector: `python predict_threat.py`