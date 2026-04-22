import streamlit as st
import math
import json
import os
from datetime import datetime, timedelta
import openai

# --- CONFIGURATION ---
DATA_FILE = "logs.json"
TRACKED_COMPONENTS = ['Capsaicin', 'Fat', 'Flavonoids', 'omega-6']

# --- AI PARSING (OPENAI SDK FOR POE) ---
def get_components_from_ai(text):
    # REPLACE WITH YOUR ACTUAL POE API KEY
    api_key = "sk-poe-XrNh8ZHroZJGv0E-iBfS198UEfI2HY-lVO5KDALUihs"
    
    prompt = f'Analyze the meal: "{text}". Which of these components does it contain: Capsaicin, Fat, Flavonoids, omega-6? Return ONLY JSON: {{"components": ["comp1", "comp2"]}}'

    print(f"\n[AI DEBUG] 🚀 Starting API call for: '{text}'")
    
    try:
        client = openai.OpenAI(api_key=api_key, base_url="https://api.poe.com/v1")
        
        # Corrected method: chat.completions.create
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Corrected response field: choices[0].message.content
        result_text = response.choices[0].message.content
        print(f"[AI DEBUG] ✅ Raw Response Received: {result_text.strip()}")
        
        clean_text = result_text.replace('```json', '').replace('```', '').strip()
        components = json.loads(clean_text).get("components", [])
        
        print(f"[AI DEBUG] 📦 Parsed Components: {components}")
        return components

    except Exception as e:
        print(f"[AI DEBUG] ❌ API CALL FAILED: {str(e)}")
        st.sidebar.error(f"AI Error: {e}")
        return []

# --- MATH LOGIC ---
def calculate_weights(delta_hours):
    if delta_hours < 0: return 0, 0, 0
    # Immediate weight (Exponential)
    w_fast = 1.0 * math.exp(-0.5 * delta_hours)
    # Delayed weight (Gaussian centered at 36h)
    w_slow = 0.8 * math.exp(-((delta_hours - 36)**2) / (2 * 6**2))
    return w_fast + w_slow, w_fast, w_slow

def run_analysis(logs):
    stats = {c: 0.0 for c in TRACKED_COMPONENTS}
    counts = {c: 0 for c in TRACKED_COMPONENTS}
    
    meals = [l for l in logs if l['type'] == 'meal']
    flares = [l for l in logs if l['type'] == 'flareup']
    
    for meal in meals:
        m_time = datetime.fromisoformat(meal['timestamp'])
        for comp in meal.get('components', []):
            if comp in stats:
                counts[comp] += 1
                for f in flares:
                    f_time = datetime.fromisoformat(f['timestamp'])
                    delta = (f_time - m_time).total_seconds() / 3600.0
                    if 0 <= delta <= 72:
                        weight, _, _ = calculate_weights(delta)
                        stats[comp] += (f['severity'] * weight)
    
    results = []
    for c in TRACKED_COMPONENTS:
        if counts[c] > 0:
            # Scale score for visibility (0-100)
            score = min(int((stats[c] / counts[c]) * 10), 100)
            results.append({"component": c, "score": score})
    return sorted(results, key=lambda x: x['score'], reverse=True)

# --- STREAMLIT UI ---
st.set_page_config(page_title="GutPattern", page_icon="🧩")
st.title("🧩 GutPattern")

if 'logs' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: st.session_state.logs = json.load(f)
    else: st.session_state.logs = []

tab1, tab2, tab3, tab4 = st.tabs(["📝 Input", "📋 History", "📊 Analysis", "🔮 Forecast"])

with tab1:
    st.header("Log Activity")
    with st.expander("🍎 Log a Meal", expanded=True):
        with st.form("meal_form", clear_on_submit=True):
            meal_txt = st.text_input("What did you eat?")
            if st.form_submit_button("Save Meal") and meal_txt:
                with st.spinner("Analyzing..."):
                    comps = get_components_from_ai(meal_txt)
                    st.session_state.logs.insert(0, {"type": "meal", "content": meal_txt, "components": comps, "timestamp": datetime.now().isoformat()})
                    with open(DATA_FILE, "w") as f: json.dump(st.session_state.logs, f)
                    st.success("Logged!")
                    st.rerun()

    with st.expander("🚨 Log a Flare-up"):
        with st.form("flare_form", clear_on_submit=True):
            sev = st.slider("Severity", 1, 10, 5)
            if st.form_submit_button("Save Flare-up"):
                st.session_state.logs.insert(0, {"type": "flareup", "severity": sev, "timestamp": datetime.now().isoformat()})
                with open(DATA_FILE, "w") as f: json.dump(st.session_state.logs, f)
                st.success("Logged!")
                st.rerun()

with tab2:
    st.header("History")
    if st.button("🗑️ Clear All"):
        st.session_state.logs = []; os.remove(DATA_FILE) if os.path.exists(DATA_FILE) else None; st.rerun()
    for l in st.session_state.logs:
        t = datetime.fromisoformat(l['timestamp']).strftime("%b %d, %H:%M")
        if l['type'] == 'meal':
            st.info(f"🍴 {l['content']} ({', '.join(l['components'])}) \n*{t}*")
        else:
            st.error(f"🚨 Flare-up: Severity {l['severity']} \n*{t}*")

with tab3:
    st.header("Analysis")
    scores = run_analysis(st.session_state.logs)
    if not scores:
        st.write("Not enough data yet. Log some meals and flare-ups!")
    else:
        for s in scores:
            st.write(f"**{s['component']}**")
            st.progress(s['score'] / 100)
            st.caption(f"Risk Score: {s['score']}/100")

with tab4:
    st.header("Risk Forecast")
    st.write("Check if a future meal might be a trigger based on your patterns.")
    
    with st.form("predict_form"):
        predict_txt = st.text_input("Enter a potential meal:")
        check_btn = st.form_submit_button("Check Risk")
        
    if check_btn and predict_txt:
        with st.spinner("Checking your history..."):
            comps = get_components_from_ai(predict_txt)
            analysis_scores = {s['component']: s['score'] for s in run_analysis(st.session_state.logs)}
            
            if not comps:
                st.warning("No tracked components identified in this meal.")
            else:
                max_risk = 0
                st.subheader("Detected Components:")
                for c in comps:
                    score = analysis_scores.get(c, 0)
                    max_risk = max(max_risk, score)
                    col1, col2 = st.columns([3, 1])
                    col1.write(f"**{c}**")
                    col2.write(f"{score}/100")
                
                st.divider()
                if max_risk > 70:
                    st.error(f"### ⚠️ High Risk ({max_risk}/100)\nThis meal contains components that frequently correlate with severe flare-ups for you.")
                elif max_risk > 40:
                    st.warning(f"### ⚠️ Caution ({max_risk}/100)\nThis meal has a moderate risk of causing a reaction.")
                else:
                    st.success(f"### ✅ Likely Safe ({max_risk}/100)\nBased on your history, this meal appears to be low risk.")
