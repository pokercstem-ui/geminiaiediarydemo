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

# --- CACHE: CLIENT ---
@st.cache_resource
def get_client():
    if not API_KEY:
        return None
    return openai.OpenAI(
        base_url="https://api.llm7.io/v1",
        api_key=API_KEY,
    )

# --- CACHE: LOAD DATA ---
@st.cache_data(show_spinner=False)
def load_logs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_logs(logs):
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f)
    st.cache_data.clear()

# --- AI PARSING ---
def analyze_meal_with_ai(text):
    client = get_client()
    if client is None:
        st.sidebar.error("API Key is missing!")
        return {"ingredients": [], "chemical_composition": {}}

    prompt = (
        f"Analyze this meal: '{text}'. Provide the following:\n"
        f"1. 'ingredients': A list of the main base ingredients.\n"
        f"2. 'chemical_composition': A dictionary mapping ingredients to a LIST of their potential dietary triggers (e.g., 'Histamine', 'Salicylates', 'Gluten', 'FODMAPs', 'Capsaicin', 'Lactose', 'Sulfites', 'Nightshades', 'Amines').\n"
        f"CRITICAL: Do NOT include generic nutrients like 'Calories', 'Protein', 'Vitamins', 'Manganese', 'Antioxidants', or 'Fat' unless they are specific allergens.\n"
        f"Return ONLY a valid JSON object matching this structure: "
        f'{{"ingredients": ["Tomato"], "chemical_composition": {{"Tomato": ["Salicylates", "Histamine", "Nightshades"]}}}}'
    )

    try:
        response = client.chat.completions.create(
            model="default",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
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

    for meal in meals:
        m_time = datetime.fromisoformat(meal["timestamp"])
        chemicals = extract_chemicals_from_meal(meal)

        is_hit = False
        flare_severity = 0

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

    global_rate = global_hits / len(meals) if meals else 0

    chem_stats = {}
    for mr in meal_records:
        for c in mr["chemicals"]:
            if c not in chem_stats:
                chem_stats[c] = {"eats": 0, "hits": 0, "severity_sum": 0}
            chem_stats[c]["eats"] += 1
            if mr["is_hit"]:
                chem_stats[c]["hits"] += 1
                chem_stats[c]["severity_sum"] += mr["severity"]

    SMOOTHING_WEIGHT = 3.0
    results = []

    for c, data in chem_stats.items():
        eats = data["eats"]
        hits = data["hits"]
        smoothed_rate = (hits + (global_rate * SMOOTHING_WEIGHT)) / (eats + SMOOTHING_WEIGHT)
        risk_multiplier = smoothed_rate / max(global_rate, 0.05)

        if risk_multiplier > 1.1:
            avg_sev = (data["severity_sum"] / hits) if hits > 0 else 0
            sev_multiplier = 1.0 + (avg_sev / 20.0)
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

# --- NEW: AI REVIEW HELPERS ---
def build_evidence_summary(logs, scores, max_items=8):
    meals = [l for l in logs if l["type"] == "meal"][:max_items]
    flares = [l for l in logs if l["type"] == "flareup"][:max_items]

    return {
        "top_scores": scores[:5],
        "recent_meals": [
            {
                "content": m.get("content", ""),
                "ingredients": m.get("ingredients", []),
                "chemicals": extract_chemicals_from_meal(m),
                "timestamp": m.get("timestamp", "")
            }
            for m in meals
        ],
        "recent_flares": [
            {
                "severity": f.get("severity", 0),
                "symptoms": f.get("symptoms", []),
                "affected_areas": f.get("affected_areas", []),
                "timestamp": f.get("timestamp", "")
            }
            for f in flares
        ],
        "total_meals": len([l for l in logs if l["type"] == "meal"]),
        "total_flares": len([l for l in logs if l["type"] == "flareup"])
    }

@st.cache_data(show_spinner=False)
def ai_review_analysis_cached(logs_json, scores_json):
    if not API_KEY:
        return {"agreement": "unknown", "reason": "Missing API key.", "confidence": 0}

    logs = json.loads(logs_json)
    scores = json.loads(scores_json)
    evidence = build_evidence_summary(logs, scores)

    prompt = f"""
You are reviewing a dietary trigger analysis for eczema patterns.
The mathematical model ranked these chemicals as triggers based on timing and frequency.

Task:
1. Decide whether you agree with the mathematical judgement.
2. Return only JSON.
3. Be conservative. If evidence is weak, say partial or uncertain.

Return schema:
{{
  "agreement": "agree" | "partial" | "disagree",
  "confidence": 0-100,
  "reason": "short explanation",
  "notable_support": ["optional bullet-like strings"],
  "notable_concerns": ["optional bullet-like strings"]
}}

Evidence:
{json.dumps(evidence, ensure_ascii=False, indent=2)}
""".strip()

    try:
        client = get_client()
        response = client.chat.completions.create(
            model="default",
            messages=[
                {"role": "system", "content": "You are a cautious medical-pattern review assistant. Do not claim causation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )

        result_text = response.choices[0].message.content.strip()
        if result_text.find('{') != -1:
            result_text = result_text[result_text.find('{'):result_text.rfind('}')+1]
        data = json.loads(result_text)

        return {
            "agreement": data.get("agreement", "unknown"),
            "confidence": data.get("confidence", 0),
            "reason": data.get("reason", ""),
            "notable_support": data.get("notable_support", []),
            "notable_concerns": data.get("notable_concerns", [])
        }
    except Exception as e:
        return {
            "agreement": "unknown",
            "confidence": 0,
            "reason": f"AI review failed: {str(e)}",
            "notable_support": [],
            "notable_concerns": []
        }

# --- LOAD DATA ---
if "logs" not in st.session_state:
    st.session_state.logs = load_logs()

logs = st.session_state.logs
