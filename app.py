import streamlit as st
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
        f"2. 'chemical_composition': A dictionary mapping ingredients to a LIST of their potential dietary triggers (e.g., 'Histamine', 'Salicylates', 'Gluten', 'FODMAPs', 'Capsaicin', 'Lactose', 'Sulfites', 'Nightshades', 'Amines').\n"
        f"CRITICAL: Do NOT include generic nutrients like 'Calories', 'Protein', 'Vitamins', 'Manganese', 'Antioxidants', or 'Fat' unless they are specific allergens.\n"
        f"Return ONLY a valid JSON object matching this structure: "
        f"{{\"ingredients\": [\"Tomato\"], \"chemical_composition\": {{\"Tomato\": [\"Salicylates\", \"Histamine\", \"Nightshades\"]}}}}"
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


# --- BAYESIAN ANALYSIS LOGIC ---
def run_analysis(logs):
    meals = [l for l in logs if l["type"] == "meal"]
    flares = [l for l in logs if l["type"] == "flareup"]

    if not meals:
        return []

    meal_records = []
    global_hits = 0

    # 1. Determine if each meal was a "Trigger Meal"
    for meal in meals:
        m_time = datetime.fromisoformat(meal["timestamp"])
        chemicals = extract_chemicals_from_meal(meal)
        
        is_hit = False
        flare_severity = 0
        
        # Check if a flare happened within 48 hours after this meal
        for f in flares:
            f_time = datetime.fromisoformat(f["timestamp"])
            delta = (f_time - m_time).total_seconds() / 3600.0
            if 0 <= delta <= 48:
                is_hit = True
                flare_severity = max(flare_severity, f.get("severity", 5))
                
        if is_hit:
            global_hits += 1
            
        meal_records.append({
            "chemicals": chemicals,
            "is_hit": is_hit,
            "severity": flare_severity
        })

    # Global Baseline: What % of ALL meals result in a flare?
    global_rate = global_hits / len(meals) if meals else 0
    
    # 2. Tally individual chemicals
    chem_stats = {}
    for mr in meal_records:
        for c in mr["chemicals"]:
            if c not in chem_stats:
                chem_stats[c] = {"eats": 0, "hits": 0, "severity_sum": 0}
            chem_stats[c]["eats"] += 1
            if mr["is_hit"]:
                chem_stats[c]["hits"] += 1
                chem_stats[c]["severity_sum"] += mr["severity"]

    # 3. Apply Bayesian Smoothing
    SMOOTHING_WEIGHT = 3.0 # Adds 3 'average' phantom meals to stop 100% jumps
    results = []
    
    for c, data in chem_stats.items():
        eats = data["eats"]
        hits = data["hits"]
        
        # Pulls low-data items toward the global average
        smoothed_rate = (hits + (global_rate * SMOOTHING_WEIGHT)) / (eats + SMOOTHING_WEIGHT)
        
        # Risk Multiplier: Is this chemical WORSE than your normal baseline?
        # A multiplier of 1.0 means it's totally neutral/safe.
        risk_multiplier = smoothed_rate / max(global_rate, 0.05) 
        
        if risk_multiplier > 1.1: # Only score it if it's at least 10% riskier than average
            avg_sev = (data["severity_sum"] / hits) if hits > 0 else 0
            sev_multiplier = 1.0 + (avg_sev / 20.0) # Boost if flares are severe
            
            # Map the multiplier to a 0-100 scale
            raw_score = (risk_multiplier - 1.0) * 35 * sev_multiplier 
            final_score = min(int(raw_score), 100)
            
            if final_score > 5:
                results.append({
                    "component": c, 
                    "score": final_score, 
                    "occurrences": eats,
                    "hit_rate": int((hits/eats)*100) if eats > 0 else 0
                })
                
    return sorted(results, key=lambda x: x["score"], reverse=True)


# --- LOAD DATA ---
if "logs" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.logs = json.load(f)
    else:
        st.session_state.logs = []

logs = st.session_state.logs

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
            
            st.info(f"🍴 **{l['content']}** \n*{t}*")
            
            if ingredients or chem_comp:
                with st.expander("View Breakdown"):
                    for ing in ingredients:
                        chems = chem_comp.get(ing, [])
                        composition = ", ".join(chems) if isinstance(chems, list) else chems
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
        st.write("Keep logging! Patterns appear once you have enough meals and safe days recorded.")
    else:
        st.caption("Chemical constituents ranked by how much they exceed your normal flare baseline.")
        for s in scores:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{s['component']}** *(Eaten {s['occurrences']} times | Triggered flare {s['hit_rate']}% of the time)*")
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
