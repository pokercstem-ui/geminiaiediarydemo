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
    api_key = "sk-poe-XrNh8ZHroZJGv0E-iBfS198UEfI2HY-lVO5KDALUihs"
    
    prompt = f'Analyze the meal: "{text}". Which of these components does it contain: Capsaicin, Fat, Flavonoids, omega-6? Return ONLY JSON: {{"components": ["comp1", "comp2"]}}'

    print(f"\n[AI DEBUG] 🚀 Starting API call for: '{text}'")
    
    try:
        client = openai.OpenAI(api_key=api_key, base_url="https://api.poe.com/v1")
        
        # Log that we are sending the request
        print(f"[AI DEBUG] Sending request to Poe (gemini-3-flash)...")
        
        response = client.responses.create(
            model="gemini-3-flash",
            input=prompt
        )
        
        result_text = response.output_text
        
        # Log the raw response from the AI
        print(f"[AI DEBUG] ✅ Raw Response Received: {result_text.strip()}")
        
        # Clean markdown if present
        clean_text = result_text.replace('```json', '').replace('```', '').strip()
        components = json.loads(clean_text).get("components", [])
        
        print(f"[AI DEBUG] 📦 Parsed Components: {components}")
        return components

    except Exception as e:
        # Log the full error to your terminal
        print(f"[AI DEBUG] ❌ API CALL FAILED")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        
        # Visual error for the user in the app
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

# Load Data
if 'logs' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: 
            st.session_state.logs = json.load(f)
    else: 
        st.session_state.logs = []

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📝 Input", "📋 History", "📊 Analysis"])

# --- TAB 1: INPUT ---
with tab1:
    st.header("Log Activity")
    with st.expander("🍎 Log a Meal", expanded=True):
        with st.form("meal_form", clear_on_submit=True):
            meal_txt = st.text_input("What did you eat?")
            if st.form_submit_button("Save Meal") and meal_txt:
                with st.spinner("AI is analyzing ingredients..."):
                    comps = get_components_from_ai(meal_txt)
                    st.session_state.logs.insert(0, {
                        "type": "meal", 
                        "content": meal_txt, 
                        "components": comps, 
                        "timestamp": datetime.now().isoformat()
                    })
                    with open(DATA_FILE, "w") as f: 
                        json.dump(st.session_state.logs, f)
                    st.success("Meal logged!")
                    st.rerun()

    with st.expander("🚨 Log a Flare-up"):
        with st.form("flare_form", clear_on_submit=True):
            sev = st.slider("Severity (1-10)", 1, 10, 5)
            if st.form_submit_button("Save Flare-up"):
                st.session_state.logs.insert(0, {
                    "type": "flareup", 
                    "severity": sev, 
                    "timestamp": datetime.now().isoformat()
                })
                with open(DATA_FILE, "w") as f: 
                    json.dump(st.session_state.logs, f)
                st.success("Symptom logged!")
                st.rerun()

# --- TAB 2: HISTORY (ALL LOGS) ---
with tab2:
    st.header("Complete History")
    if not st.session_state.logs:
        st.write("No logs found yet. Start by logging a meal!")
    else:
        if st.button("🗑️ Clear All History"):
            st.session_state.logs = []
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            st.rerun()

        for l in st.session_state.logs:
            # Format time for readability
            time_str = datetime.fromisoformat(l['timestamp']).strftime("%b %d, %I:%M %p")
            
            if l['type'] == 'meal':
                st.info(f"🍴 **MEAL**: {l.get('content')}  \n**Components**: {', '.join(l.get('components', [])) or 'None detected'}  \n*{time_str}*")
            else:
                st.error(f"🚨 **FLARE-UP**: Severity {l.get('severity')}  \n*{time_str}*")

# --- TAB 3: ANALYSIS ---
with tab3:
    st.header("Pattern Analysis")
    st.info("Log at least 3-5 days of data to see mathematical correlations.")
    # Mathematical analysis visualization would go here
