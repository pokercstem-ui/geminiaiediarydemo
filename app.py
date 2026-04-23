import streamlit as st
import math
import json
import os
from datetime import datetime
import openai

# --- PAGE SETUP ---
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

st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        padding-top: 0.25rem;
        border-bottom: 1px solid rgba(49, 51, 63, 0.12);
    }

    .stTabs [data-baseweb="tab"] {
        background: #f6f8fb;
        border: 1px solid #dbe3ee;
        border-bottom: none;
        padding: 0.45rem 0.9rem;
        border-radius: 999px 999px 0 0;
        font-weight: 600;
        color: #4a5568;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: white;
        color: #2563eb;
        border-color: #93c5fd;
        box-shadow: 0 -2px 10px rgba(37, 99, 235, 0.08);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: #eef4ff;
        color: #1d4ed8;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

DATA_FILE = "logs.json"
TRACKED_COMPONENTS = ['Capsaicin', 'Fat', 'Flavonoids', 'omega-6']

SYMPTOM_OPTIONS = [
    "Itching", "Redness", "Dryness", "Cracking", "Oozing",
    "Burning", "Swelling", "Pain", "Sleep disturbance"
]

AFFECTED_AREA_OPTIONS = [
    "Face", "Eyelids", "Neck", "Chest", "Back", "Arms", "Elbows",
    "Hands", "Fingers", "Stomach", "Legs", "Knees", "Feet", "Other"
]

TREATMENT_OPTIONS = [
    "Moisturizer", "Topical steroid", "Topical calcineurin inhibitor",
    "Antihistamine", "Wet wrap", "Cool compress", "None"
]

# --- SECRETS ---
API_KEY = st.secrets.get("LLM7_API_KEY", "")
if not API_KEY:
    st.warning("Add `LLM7_API_KEY` to `.streamlit/secrets.toml`.")

# --- AI PARSING ---
def get_components_from_ai(text):
    if not API_KEY:
        return []

    prompt = (
        f"Analyze this meal: '{text}'. Which of these components does it contain: "
        f"Capsaicin, Fat, Flavonoids, omega-6, or none? Only flag them when they are in large amounts. "
        f"Return ONLY a JSON object like this: {{\"components\": [\"Capsaicin\", \"omega-6\"]}}"
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
        data = json.loads(clean_text)
        components = data.get("components", [])
        return [c for c in components if c in TRACKED_COMPONENTS]

    except Exception:
        st.sidebar.error("AI Error: Could not analyze meal components.")
        return []

# --- ANALYSIS LOGIC ---
def calculate_weights(delta_hours):
    if delta_hours < 0:
        return 0, 0, 0
    w_fast = 1.0 * math.exp(-0.5 * delta_hours)
    w_slow = 0.8 * math.exp(-((delta_hours - 36) ** 2) / (2 * 6 ** 2))
    return w_fast + w_slow, w_fast, w_slow

def flare_feature_score(flare):
    severity = flare.get("severity", 5)
    itch = flare.get("itch", 0)
    sleep = flare.get("sleep_disturbance", 0)
    area_count = len(flare.get("affected_areas", []))
    symptom_count = len(flare.get("symptoms", []))

    return (
        severity * 1.0 +
        itch * 1.2 +
        sleep * 1.0 +
        min(area_count, 6) * 0.8 +
        min(symptom_count, 6) * 0.4
    )

def run_analysis(logs):
    stats = {c: 0.0 for c in TRACKED_COMPONENTS}
    counts = {c: 0 for c in TRACKED_COMPONENTS}

    meals = [l for l in logs if l["type"] == "meal"]
    flares = [l for l in logs if l["type"] == "flareup"]

    for meal in meals:
        m_time = datetime.fromisoformat(meal["timestamp"])
        for comp in meal.get("components", []):
            if comp in stats:
                counts[comp] += 1
                for f in flares:
                    f_time = datetime.fromisoformat(f["timestamp"])
                    delta = (f_time - m_time).total_seconds() / 3600.0
                    if 0 <= delta <= 72:
                        weight, _, _ = calculate_weights(delta)
                        stats[comp] += flare_feature_score(f) * weight

    results = []
    for c in TRACKED_COMPONENTS:
        if counts[c] > 0:
            score = min(int((stats[c] / counts[c]) * 4), 100)
            results.append({"component": c, "score": score})

    return sorted(results, key=lambda x: x["score"], reverse=True)

# --- LOAD DATA ---
if "logs" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.logs = json.load(f)
    else:
        st.session_state.logs = []

logs = st.session_state.logs
meal_count = sum(1 for l in logs if l["type"] == "meal")
flare_count = sum(1 for l in logs if l["type"] == "flareup")
latest_flare = next((l for l in logs if l["type"] == "flareup"), None)

# --- HEADER ---
st.markdown('<div class="big-title">🧩 GutPattern</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Track meals, eczema flares, and trigger patterns with a friendlier, more visual dashboard.</div>',
    unsafe_allow_html=True
)

# --- SIDEBAR ---

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
                    with st.spinner("AI is analyzing components..."):
                        comps = get_components_from_ai(meal_txt)
                        st.session_state.logs.insert(0, {
                            "type": "meal",
                            "content": meal_txt,
                            "components": comps,
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
                itch = st.slider("Itch severity", 0, 10, 5)
                sleep_disturbance = st.slider("Sleep disturbance", 0, 10, 0)
                symptoms = st.multiselect("What symptoms did you have?", SYMPTOM_OPTIONS)
                affected_areas = st.multiselect("What areas were affected?", AFFECTED_AREA_OPTIONS)
                other_area = st.text_input("Other affected area (optional)")
                treatment_used = st.multiselect("What did you use?", TREATMENT_OPTIONS)
                notes = st.text_area("Extra notes", placeholder="e.g. worse after sweating, new soap, stressed at work")
                save_flare = st.form_submit_button("Save Flare-up")

                if save_flare:
                    areas = affected_areas + ([other_area] if other_area.strip() else [])
                    st.session_state.logs.insert(0, {
                        "type": "flareup",
                        "severity": sev,
                        "itch": itch,
                        "sleep_disturbance": sleep_disturbance,
                        "symptoms": symptoms,
                        "affected_areas": areas,
                        "treatment_used": treatment_used,
                        "notes": notes,
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
            comp_list = l.get("components", [])
            labels = " ".join([f"`{c}`" for c in comp_list]) if comp_list else "*No tracked components*"
            st.info(f"🍴 **{l['content']}**  \n{labels}  \n*{t}*")
        else:
            symptoms = ", ".join(l.get("symptoms", [])) or "Not specified"
            areas = ", ".join(l.get("affected_areas", [])) or "Not specified"
            treatments = ", ".join(l.get("treatment_used", [])) or "None"
            notes = l.get("notes", "").strip() or "None"

            st.error(
                f"🚨 **Flare-up**: Severity {l.get('severity', 0)}  \n"
                f"**Itch:** {l.get('itch', 0)}/10  \n"
                f"**Sleep disturbance:** {l.get('sleep_disturbance', 0)}/10  \n"
                f"**Symptoms:** {symptoms}  \n"
                f"**Affected areas:** {areas}  \n"
                f"**Treatment used:** {treatments}  \n"
                f"**Notes:** {notes}  \n"
                f"*{t}*"
            )

with tab3:
    st.subheader("Analysis")
    scores = run_analysis(logs)

    if not scores:
        st.write("Keep logging! Patterns appear once you have meals and flare-ups recorded.")
    else:
        for s in scores:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{s['component']}**")
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
            comps = get_components_from_ai(predict_txt)
            analysis_scores = {s["component"]: s["score"] for s in run_analysis(logs)}

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
                    st.error("### High Risk Detected\nYour history suggests this meal might lead to a strong reaction.")
                elif max_risk > 40:
                    st.warning("### Caution\nThere is a moderate historical correlation with flare-ups.")
                else:
                    st.success("### Likely Low Risk\nNo strong patterns found for these ingredients.")
