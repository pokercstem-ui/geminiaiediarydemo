import streamlit as st
import math
import json
import os
from datetime import datetime
import openai

# --- PAGE SETUP ---
st.set_page_config(page_title="GutPattern", page_icon="🧩")
st.markdown("# 🧩 GutPattern")
st.caption("Track meals, eczema flares, and trigger patterns in one clean place.")

st.markdown(
    """
    <style>
    .big-title {font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem;}
    .subtitle {font-size: 1rem; opacity: 0.8; margin-bottom: 1rem;}
    </style>
    """,
    unsafe_allow_html=True
)

DATA_FILE = "logs.json"

SYMPTOM_OPTIONS = [
    "Itching", "Redness", "Dryness", "Cracking", "Oozing",
    "Burning", "Swelling", "Pain", "Sleep disturbance"
]

AFFECTED_AREA_OPTIONS = [
    "Face", "Eyelids", "Neck", "Chest", "Back", "Arms", "Elbows",
    "Hands", "Fingers", "Stomach", "Legs", "Knees", "Feet", "Other"
]

# --- SECRETS ---
API_KEY = st.secrets.get("LLM7_API_KEY", "")
if not API_KEY:
    st.warning("Add `LLM7_API_KEY` to `.streamlit/secrets.toml`.")

# --- AI PARSING ---
def analyze_meal_with_ai(text):
    if not API_KEY:
        st.sidebar.error("API Key is missing!")
        return {"ingredients": [], "chemical_composition": {}}

    prompt = (
        f"Analyze this meal: '{text}'. Provide the following:\n"
        f"1. 'ingredients': A list of the main base ingredients.\n"
        f"2. 'chemical_composition': A dictionary where keys are the ingredients, and values are LISTS of their main chemical/nutritional constituents (e.g., 'Histamine', 'Salicylates', 'Gluten', 'Capsaicin', 'Vitamin C', 'Saturated Fat'). Focus heavily on potential dietary triggers, macro/micronutrients, and natural chemicals.\n"
        f"Return ONLY a valid JSON object matching this structure: "
        f"{{\"ingredients\": [\"Tomato\"], \"chemical_composition\": {{\"Tomato\": [\"Salicylates\", \"Lycopene\", \"Histamine\", \"Vitamin C\"]}}}}"
    )

    try:
        client = openai.OpenAI(
            base_url="https://api.llm7.io/v1",
            api_key=API_KEY,
        )

        response = client.chat.completions.create(
            model="default",
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.choices[0].message.content
        clean_text = result_text.replace("```json", "").replace("```", "").strip()
        
        if clean_text.find('{') != -1:
            clean_text = clean_text[clean_text.find('{'):clean_text.rfind('}')+1]

        data = json.loads(clean_text)
        
        return {
            "ingredients": data.get("ingredients", []),
            "chemical_composition": data.get("chemical_composition", {})
        }

    except Exception as e:
        print(f"AI ERROR DETAILS: {str(e)}") 
        st.sidebar.error(f"AI Error: {str(e)}")
        return {"ingredients": [], "chemical_composition": {}}

# --- HELPER LOGIC ---
def extract_chemicals_from_meal(meal):
    chemicals = set()
    chem_comp = meal.get("chemical_composition", {})
    for chem_list in chem_comp.values():
        if isinstance(chem_list, list):
            for c in chem_list:
                chemicals.add(c.strip().title())
        elif isinstance(chem_list, str):
            for c in chem_list.split(','):
                chemicals.add(c.strip().title())
    return list(chemicals)

# --- ANALYSIS LOGIC ---
def calculate_weights(delta_hours):
    if delta_hours < 0:
        return 0, 0, 0
    w_fast = 1.0 * math.exp(-0.5 * delta_hours)
    w_slow = 0.8 * math.exp(-((delta_hours - 36) ** 2) / (2 * 6 ** 2))
    return w_fast + w_slow, w_fast, w_slow

def flare_feature_score(flare):
    severity = flare.get("severity", 5)
    area_count = len(flare.get("affected_areas", []))
    symptom_count = len(flare.get("symptoms", []))

    return (
        severity * 1.0 +
        min(area_count, 6) * 0.8 +
        min(symptom_count, 6) * 0.4
    )

def run_analysis(logs):
    stats = {}
    counts = {}

    meals = [l for l in logs if l["type"] == "meal"]
    flares = [l for l in logs if l["type"] == "flareup"]

    for meal in meals:
        m_time = datetime.fromisoformat(meal["timestamp"])
        chemicals = extract_chemicals_from_meal(meal)
        
        for comp in chemicals:
            if comp not in stats:
                stats[comp] = 0.0
                counts[comp] = 0
            
            counts[comp] += 1
            
            for f in flares:
                f_time = datetime.fromisoformat(f["timestamp"])
                delta = (f_time - m_time).total_seconds() / 3600.0
                if 0 <= delta <= 72:
                    weight, _, _ = calculate_weights(delta)
                    stats[comp] += flare_feature_score(f) * weight

    results = []
    for c in stats:
        if counts[c] > 0:
            score = min(int((stats[c] / counts[c]) * 4), 100)
            if score > 0: 
                results.append({"component": c, "score": score, "occurrences": counts[c]})

    return sorted(results, key=lambda x: x["score"], reverse=True)

# --- LOAD DATA ---
if "logs" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.logs = json.load(f)
    else:
        st.session_state.logs = []

logs = st.session_state.logs

# --- HEADER ---
st.markdown(
    '<div class="subtitle">Track meals, eczema flares, and trigger patterns with a friendlier, more visual dashboard.</div>',
    unsafe_allow_html=True
)

# --- SIDEBAR & TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📝 Input", "📋 History", "📊 Analysis", "🔮 Forecast"])

with tab1:
    st.subheader("Log Activity")
    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("### 🍎 Log a Meal")
            with st.form("meal_form", clear_on_submit=True):
                meal_txt = st.text_input("What did you eat?", placeholder="e.g. French fries and spicy dipping sauce")
                save_meal = st.form_submit_button("Save Meal")
                
                if save_meal and meal_txt:
                    with st.spinner("AI is extracting chemical composition..."):
                        analysis_data = analyze_meal_with_ai(meal_txt)
                        
                        st.session_state.logs.insert(0, {
                            "type": "meal",
                            "content": meal_txt,
                            "ingredients": analysis_data["ingredients"],
                            "chemical_composition": analysis_data["chemical_composition"],
                            "timestamp": datetime.now().isoformat()
                        })
                        with open(DATA_FILE, "w") as f:
                            json.dump(st.session_state.logs, f)
                        st.success("Meal logged successfully!")
                        st.rerun()

    with right:
        with st.container(border=True):
            st.markdown("### 🚨 Log a Flare-up")
            with st.form("flare_form", clear_on_submit=True):
                sev = st.slider("Overall severity", 1, 10, 5)
                symptoms = st.multiselect("What symptoms did you have?", SYMPTOM_OPTIONS)
                affected_areas = st.multiselect("What areas were affected?", AFFECTED_AREA_OPTIONS)
                save_flare = st.form_submit_button("Save Flare-up")

                if save_flare:
                    st.session_state.logs.insert(0, {
                        "type": "flareup",
                        "severity": sev,
                        "symptoms": symptoms,
                        "affected_areas": affected_areas,
                        "timestamp": datetime.now().isoformat()
                    })
                    with open(DATA_FILE, "w") as f:
                        json.dump(st.session_state.logs, f)
                    st.success("Flare-up logged.")
                    st.rerun()

with tab2:
    st.subheader("History")
    if st.button("🗑️ Clear All History"):
        st.session_state.logs = []
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.rerun()

    for l in logs:
        t = datetime.fromisoformat(l["timestamp"]).strftime("%b %d, %H:%M")
        
        if l["type"] == "meal":
            ingredients = l.get("ingredients", [])
            chem_comp = l.get("chemical_composition", {})
            
            # Removed the raw labels from the info box for a cleaner look
            st.info(f"🍴 **{l['content']}** \n*{t}*")
            
            if ingredients or chem_comp:
                with st.expander("View Breakdown"):
                    for ing in ingredients:
                        chems = chem_comp.get(ing, [])
                        if isinstance(chems, list):
                            composition = ", ".join(chems)
                        else:
                            composition = chems # fallback
                        st.markdown(f"- **{ing}**: {composition}")
                        
        else:
            symptoms = ", ".join(l.get("symptoms", [])) or "Not specified"
            areas = ", ".join(l.get("affected_areas", [])) or "Not specified"

            st.error(
                f"🚨 **Flare-up**: Severity {l.get('severity', 0)}  \n"
                f"**Symptoms:** {symptoms}  \n"
                f"**Affected areas:** {areas}  \n"
                f"*{t}*"
            )

with tab3:
    st.subheader("Analysis")
    scores = run_analysis(logs)

    if not scores:
        st.write("Keep logging! Patterns appear once you have meals and flare-ups recorded.")
    else:
        st.caption("Showing chemical constituents ranked by correlation to your flare-ups.")
        for s in scores:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{s['component']}** *(Logged {s['occurrences']} times)*")
                st.progress(s["score"] / 100)
            with col2:
                st.metric("Score", f"{s['score']}/100")

with tab4:
    st.subheader("Risk Forecast")
    st.write("Predict potential triggers before you eat.")

    with st.form("predict_form"):
        predict_txt = st.text_input("Enter a meal to check:")
        check_btn = st.form_submit_button("Check Pattern Risk")

    if check_btn and predict_txt:
        with st.spinner("Checking your history..."):
            analysis_data = analyze_meal_with_ai(predict_txt)
            comps = extract_chemicals_from_meal(analysis_data)
            analysis_scores = {s["component"]: s["score"] for s in run_analysis(logs)}

            if not comps:
                st.warning("No tracked chemicals found in that meal.")
            else:
                max_risk = 0
                for c in comps:
                    score = analysis_scores.get(c, 0)
                    max_risk = max(max_risk, score)
                    st.write(f"Found `{c}`: Risk Score {score}/100")

                st.divider()
                if max_risk > 70:
                    st.error("### High Risk Detected\nYour history suggests this meal contains chemicals that frequently correlate with your flare-ups.")
                elif max_risk > 40:
                    st.warning("### Caution\nThere is a moderate historical correlation with your flare-ups.")
                else:
                    st.success("### Likely Low Risk\nNo strong patterns found for these chemical constituents.")
