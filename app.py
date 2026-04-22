import streamlit as st
import math
import json
import os
from datetime import datetime, timedelta
import openai

# --- CONFIGURATION ---
DATA_FILE = "logs.json"
TRACKED_COMPONENTS = ['Capsaicin', 'Fat', 'Flavonoids', 'omega-6']

# --- AI PARSING (LLM7 API) ---
def get_components_from_ai(text):
    # Get your free token at https://token.llm7.io/
    api_key = "ZxugNtluJ/d/+0SKz5W45sGjrfvAparfpj5lRoBaTqcomEUfQSVVHTHHIziryjwjFaHipl/jXzhng2BEgyBtQjpqkm8KUV7r2/asrD93Z68PaLQqilUvABGq/O2cgWkrO2uukw=="
    
    prompt = (
        f"Analyze this meal: '{text}'. Which of these components does it contain: You are to provide a JUST and fair feedback. If there are traces of it, it should be counted as none."
        f"Capsaicin, Fat, Flavonoids, omega-6 or none? "
        f"Return ONLY a JSON object like this: {{\"components\": [\"Fat\", \"omega-6\"]}}"
    )

    print(f"\n[AI DEBUG] 🚀 Starting LLM7 API call for: '{text}'")
    
    try:
        # LLM7 is OpenAI-compatible
        client = openai.OpenAI(
            base_url="https://api.llm7.io/v1",
            api_key=api_key,
        )
        
        response = client.chat.completions.create(
            model="default",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        result_text = response.choices[0].message.content
        print(f"[AI DEBUG] ✅ Raw Response Received: {result_text.strip()}")
        
        # Clean markdown formatting if present
        clean_text = result_text.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_text)
        components = data.get("components", [])
        
        # Filter to ensure only valid tracked components are returned
        valid_comps = [c for c in components if c in TRACKED_COMPONENTS]
        
        print(f"[AI DEBUG] 📦 Parsed Components: {valid_comps}")
        return valid_comps

    except Exception as e:
        print(f"[AI DEBUG] ❌ LLM7 API CALL FAILED: {str(e)}")
        st.sidebar.error(f"AI Error: Could not analyze meal components.")
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
            meal_txt = st.text_input("What did you eat?", placeholder="e.g. French fries and spicy dipping sauce")
            if st.form_submit_button("Save Meal") and meal_txt:
                with st.spinner("AI is analyzing components..."):
                    comps = get_components_from_ai(meal_txt)
                    st.session_state.logs.insert(0, {
                        "type": "meal", 
                        "content": meal_txt, 
                        "components": comps, 
                        "timestamp": datetime.now().isoformat()
                    })
                    with open(DATA_FILE, "w") as f: json.dump(st.session_state.logs, f)
                    st.success("Meal logged successfully!")
                    st.rerun()

    with st.expander("🚨 Log a Flare-up"):
        with st.form("flare_form", clear_on_submit=True):
            sev = st.slider("How severe is the reaction?", 1, 10, 5)
            if st.form_submit_button("Save Flare-up"):
                st.session_state.logs.insert(0, {
                    "type": "flareup", 
                    "severity": sev, 
                    "timestamp": datetime.now().isoformat()
                })
                with open(DATA_FILE, "w") as f: json.dump(st.session_state.logs, f)
                st.success("Symptom logged.")
                st.rerun()

with tab2:
    st.header("History")
    if st.button("🗑️ Clear All History"):
        st.session_state.logs = []
        if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
        st.rerun()
    
    for l in st.session_state.logs:
        t = datetime.fromisoformat(l['timestamp']).strftime("%b %d, %H:%M")
        if l['type'] == 'meal':
            comp_list = l.get('components', [])
            labels = " ".join([f"`{c}`" for c in comp_list]) if comp_list else "*No tracked components*"
            st.info(f"🍴 **{l['content']}** \n{labels}  \n*{t}*")
        else:
            st.error(f"🚨 **Flare-up**: Severity {l['severity']}  \n*{t}*")

with tab3:
    st.header("Analysis")
    scores = run_analysis(st.session_state.logs)
    if not scores:
        st.write("Keep logging! Patterns appear once you have meals and flare-ups recorded.")
    else:
        for s in scores:
            st.write(f"**{s['component']}**")
            st.progress(s['score'] / 100)
            st.caption(f"Correlation Score: {s['score']}/100")

with tab4:
    st.header("Risk Forecast")
    st.write("Predict potential triggers before you eat.")
    
    with st.form("predict_form"):
        predict_txt = st.text_input("Enter a meal to check:")
        check_btn = st.form_submit_button("Check Pattern Risk")
        
    if check_btn and predict_txt:
        with st.spinner("Checking your history..."):
            comps = get_components_from_ai(predict_txt)
            analysis_scores = {s['component']: s['score'] for s in run_analysis(st.session_state.logs)}
            
            if not comps:
                st.warning("No tracked components found in that meal.")
            else:
                max_risk = 0
                for c in comps:
                    score = analysis_scores.get(c, 0)
                    max_risk = max(max_risk, score)
                    st.write(f"Found `{c}`: Risk Score {score}/100")
                
                st.divider()
                if max_risk > 70:
                    st.error(f"### High Risk Detected\nYour history suggests this meal might lead to a strong reaction.")
                elif max_risk > 40:
                    st.warning(f"### Caution\nThere is a moderate historical correlation with flare-ups.")
                else:
                    st.success(f"### Likely Low Risk\nNo strong patterns found for these ingredients.")
