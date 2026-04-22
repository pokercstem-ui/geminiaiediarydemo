import streamlit as st
import math
import json
import os
from datetime import datetime, timedelta
import openai

# --- CONFIGURATION ---
DATA_FILE = "logs.json"
TRACKED_COMPONENTS = ['Capsaicin', 'Fat', 'Flavonoids', 'omega-6']

# --- AI PARSING (POE SDK) ---
def get_components_from_ai(text):
    # Replace with your actual Poe API key
    api_key = "YOUR_POE_API_KEY"
    
    prompt = f'Analyze the meal: "{text}". Which of these components does it contain: Capsaicin, Fat, Flavonoids, omega-6? Return ONLY JSON: {{"components": ["comp1", "comp2"]}}'

    try:
        client = openai.OpenAI(api_key=api_key, base_url="https://api.poe.com/v1")
        response = client.responses.create(
            model="gemini-2.0-flash-lite",
            input=prompt
        )
        result_text = response.output_text
        clean_text = result_text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text).get("components", [])
    except Exception as e:
        st.sidebar.error(f"AI Error: {e}")
        return []

# --- MATH LOGIC ---
def calculate_weights(delta_hours):
    if delta_hours < 0: return 0, 0, 0
    w_fast = 1.0 * math.exp(-0.5 * delta_hours)
    w_slow = 0.8 * math.exp(-((delta_hours - 36)**2) / (2 * 6**2))
    return w_fast + w_slow, w_fast, w_slow

# --- STREAMLIT UI ---
st.set_page_config(page_title="GutPattern", page_icon="🧩")
st.title("🧩 GutPattern")
st.caption("Bi-Modal Dietary Trigger Tracker")

if 'logs' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: st.session_state.logs = json.load(f)
    else: st.session_state.logs = []

tab1, tab2 = st.tabs(["📖 Journal", "📊 Analysis"])

with tab1:
    with st.form("meal_form"):
        meal_txt = st.text_input("What did you eat?")
        if st.form_submit_button("Log Meal") and meal_txt:
            comps = get_components_from_ai(meal_txt)
            st.session_state.logs.insert(0, {"type": "meal", "content": meal_txt, "components": comps, "timestamp": datetime.now().isoformat()})
            with open(DATA_FILE, "w") as f: json.dump(st.session_state.logs, f)
            st.rerun()

    with st.form("flare_form"):
        sev = st.slider("Flare-up Severity", 1, 10, 5)
        if st.form_submit_button("Log Flare-up"):
            st.session_state.logs.insert(0, {"type": "flareup", "severity": sev, "timestamp": datetime.now().isoformat()})
            with open(DATA_FILE, "w") as f: json.dump(st.session_state.logs, f)
            st.rerun()

    for l in st.session_state.logs[:5]:
        st.write(f"**{l['type'].upper()}** - {l.get('content', f'Severity {l.get('severity', 0)}')} ({l['timestamp'][:16]})")
        
with tab2:
    st.header("Pattern Analysis")
    # Analysis logic would iterate through logs and apply calculate_weights here
    st.info("Log more data to see mathematical correlations.")
