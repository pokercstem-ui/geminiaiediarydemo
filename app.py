import streamlit as st
import json
import os
from datetime import datetime
import openai
from PIL import Image

# --- NEW: Import the presets from the separate file ---
from presets import get_preset_logs

# --- PAGE SETUP ---
# Load the uploaded image for the app icon
try:
    icon = Image.open("ed01.jpg")
except FileNotFoundError:
    icon = "🧩" # Fallback if image isn't found during testing

st.set_page_config(page_title="E-diary", page_icon=icon)
st.markdown("# E-Diary")
st.caption("Track meals, eczema flares, and trigger patterns in one clean place.")

st.markdown(
    """
    <style>
    .big-title {font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem;}
    .subtitle {font-size: 1rem; opacity: 0.8; margin-bottom: 1rem;}
    /* Made buttons standard alignment so the 🔍 centers nicely */
    .stButton>button {padding: 0.2rem 0.5rem;} 
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

# --- SECRETS & CLIENT INITIALIZATION ---
API_KEY = st.secrets.get("LLM7_API_KEY", "")
if not API_KEY:
    st.warning("Add `LLM7_API_KEY` to `.streamlit/secrets.toml`.")

@st.cache_resource
def get_ai_client():
    """Caches the AI client so it doesn't re-initialize on every rerun."""
    if not API_KEY:
        return None
    return openai.OpenAI(base_url="https://api.llm7.io/v1", api_key=API_KEY)

client = get_ai_client()

# --- DATA LOADING ---
@st.cache_data
def load_data(filepath):
    """Loads data and ensures presets are included only once."""
    # Always grab the presets first
    presets = get_preset_logs()
    
    # Try to load existing user data
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                existing_logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_logs = []
    else:
        existing_logs = []

    # Use timestamp as unique key to prevent duplicates
    log_dict = {}

    # First add presets (with lower priority)
    for log in presets:
        log_dict[log["timestamp"]] = log

    # Then add user logs (they will overwrite presets if timestamp matches)
    for log in existing_logs:
        log_dict[log["timestamp"]] = log

    # Convert back to list and sort by timestamp (newest first)
    final_logs = sorted(list(log_dict.values()), key=lambda x: x["timestamp"], reverse=True)

    # Save cleaned data back to file
    with open(filepath, "w") as f:
        json.dump(final_logs, f, indent=2)

    return final_logs

# --- AI PARSING & INFO ---
@st.cache_data(show_spinner=False)
def analyze_meal_with_ai(text):
    """Caches meal analysis so identical meals process instantly."""
    if not client:
        st.sidebar.error("API Key is missing!")
        return {"ingredients": [], "chemical_composition": {}}

    prompt = (
        f"Analyze this meal: '{text}'. Provide the following:\n"
        f"1. 'ingredients': A list of the main base ingredients.\n"
        f"2. 'chemical_composition': A dictionary mapping ingredients to a LIST of specific, granular chemical compounds and molecular triggers known to cause inflammation, intolerances, or allergic reactions.\n\n"
        f"CRITICAL INSTRUCTION: Go in-depth to the molecular level. Do NOT use broad, generic categories like 'Gluten', 'Dairy', 'Nightshades', 'Shellfish', 'Amines', or 'FODMAPs'.\n"
        f"- Instead of 'Gluten', list specific proteins (e.g., 'Gliadin', 'Glutenin').\n"
        f"- Instead of 'Dairy', list specific proteins/sugars (e.g., 'Casein', 'Beta-lactoglobulin', 'Lactose').\n"
        f"- Instead of 'Amines', list the specific biogenic amines (e.g., 'Tyramine', 'Putrescine', 'Cadaverine', 'Histamine').\n"
        f"- Instead of 'Nightshades', list the specific alkaloids (e.g., 'Solanine', 'Tomatine', 'Capsaicin').\n"
        f"- Identify specific allergenic proteins where applicable (e.g., 'Tropomyosin' in shellfish, 'Ovalbumin' in egg).\n"
        f"- Identify specific additives/preservatives (e.g., 'Sodium Nitrite', 'Sodium Benzoate', 'Monosodium Glutamate', 'Tartrazine', 'Sulfites').\n"
        f"- Identify specific carbohydrates/sugars if they act as triggers (e.g., 'Fructans', 'Galacto-oligosaccharides', 'Fructose').\n\n"
        f"Do NOT include generic macro/micronutrients like 'Calories', 'Protein', 'Vitamins', 'Manganese', 'Antioxidants', or 'Fat' unless they are specific known triggers.\n"
        f"Make it concise, don't add if-cases, think about the general case. \n"
        f"Return ONLY a valid JSON object matching this structure: "
        f'{{"ingredients": ["Tomato"], "chemical_composition": {{"Tomato": ["Solanine", "Tomatine", "Histamine", "Salicylic Acid"]}}}}'
    )

    try:
        response = client.chat.completions.create(
            model="default",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
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

@st.cache_data(show_spinner=False)
def get_chemical_info_from_ai(chemical_name):
    """Fetches descriptive information about a specific chemical component."""
    if not client:
        return "API Key missing. Cannot fetch details."
        
    prompt = f"""
    Briefly explain what '{chemical_name}' is in the context of food. 
    1. Where is it commonly found?
    3. How is it related to eczema flare-ups?
    Format the response clearly using markdown bullet points or short paragraphs. Keep it concise but informative.
    """
    
    try:
        response = client.chat.completions.create(
            model="default",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error fetching information: {str(e)}"

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

# --- POP-UP DIALOG FUNCTION ---
@st.dialog("🔬 Chemical Profile")
def show_chemical_profile(chemical_name, occurrences, hit_rate, score):
    st.markdown(f"### {chemical_name}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Times Logged", occurrences)
    col2.metric("Flare Correlation", f"{hit_rate}%")
    col3.metric("Risk Score", f"{score}/100")
    
    st.divider()
    
    with st.spinner("Fetching data..."):
        info = get_chemical_info_from_ai(chemical_name)
        
    st.markdown(info)

# --- AI REVIEW FUNCTIONS ---
def build_evidence_summary(logs, scores, max_items=8):
    # Get the top chemical triggers to actively look for in the history
    top_chemicals = [s["component"] for s in scores[:3]]
    
    meals = [l for l in logs if l["type"] == "meal"]
    flares = [l for l in logs if l["type"] == "flareup"]

    # Prioritize meals that contain the top suspected triggers
    relevant_meals = []
    for m in meals:
        m_chems = extract_chemicals_from_meal(m)
        if any(c in m_chems for c in top_chemicals):
            relevant_meals.append(m)
            
    # If we don't have enough relevant meals, pad with recent ones
    if len(relevant_meals) < max_items:
        remaining_meals = [m for m in meals if m not in relevant_meals]
        relevant_meals.extend(remaining_meals[:max_items - len(relevant_meals)])
    
    # Trim to max_items
    relevant_meals = relevant_meals[:max_items]

    meal_summary = []
    for m in relevant_meals:
        meal_summary.append({
            "content": m.get("content", ""),
            "ingredients": m.get("ingredients", []),
            "chemicals": extract_chemicals_from_meal(m),
            "timestamp": m.get("timestamp", "")
        })

    flare_summary = []
    for f in flares[:max_items]:
        flare_summary.append({
            "severity": f.get("severity", 0),
            "symptoms": f.get("symptoms", []),
            "affected_areas": f.get("affected_areas", []),
            "timestamp": f.get("timestamp", "")
        })

    return {
        "top_suspects_stats": [
            {
                "chemical": s["component"], 
                "times_eaten": s["occurrences"], 
                "flare_correlation": f"{s['hit_rate']}%"
            } for s in scores[:5]
        ],
        "relevant_evidence_meals": meal_summary,
        "recent_flares": flare_summary,
        "total_meals_logged": len(meals),
        "total_flares_logged": len(flares)
    }

@st.cache_data(show_spinner=False)
def ai_review_analysis(logs, scores):
    """Caches the AI review so it doesn't re-run unless the logs/scores change."""
    if not client:
        return {"agreement": "unknown", "reason": "Missing API key.", "confidence": 0}

    evidence = build_evidence_summary(logs, scores)

    prompt = f"""
You are reviewing a dietary trigger analysis for eczema patterns.
The mathematical model ranked these chemicals as triggers based on timing and frequency.

Task:
1. Decide whether you agree with the mathematical judgement based on the provided evidence and stats.
2. Return only JSON.
3. Be objective. Acknowledge that the dataset might be small, but evaluate the mathematical logic based strictly on the provided stats and evidence meals.

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
        response = client.chat.completions.create(
            model="default",
            messages=[
                {"role": "system", "content": "You are a cautious medical-pattern review assistant. Do not claim absolute causation. Focus on whether the statistical pattern makes sense given the data. If the dataset is small, evaluate the existing data at face value while noting the sample size as a minor concern, not a dealbreaker."},
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

    SMOOTHING_WEIGHT = 2.8
    results = []
    
    for c, data in chem_stats.items():
        eats = data["eats"]
        hits = data["hits"]
        smoothed_rate = (hits + (global_rate * SMOOTHING_WEIGHT)) / (eats + SMOOTHING_WEIGHT)
        risk_multiplier = smoothed_rate / max(global_rate, 0.05) 
        
        if risk_multiplier > 1.09:
            avg_sev = (data["severity_sum"] / hits) if hits > 0 else 0
            sev_multiplier = 1.0 + (avg_sev / 20.0) 
            raw_score = (risk_multiplier - 1.0) * 35 * sev_multiplier 
            final_score = min(int(raw_score), 100)
            
            if final_score > 4.8:
                results.append({
                        "component": c, 
                        "score": final_score, 
                        "occurrences": eats,
                        "hit_rate": int((hits/eats)*100) if eats > 0 else 0
                    })
                
    return sorted(results, key=lambda x: x["score"], reverse=True)

# --- LOAD DATA TO SESSION ---
if "logs" not in st.session_state:
    st.session_state.logs = load_data(DATA_FILE)
else:
    # Refresh from file in case it was updated elsewhere
    st.session_state.logs = load_data(DATA_FILE)

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
                col_date1, col_time1 = st.columns(2)
                with col_date1:
                    meal_date = st.date_input("Meal date", value=datetime.now().date())
                with col_time1:
                    meal_time = st.time_input("Meal time", value=datetime.now().time())
                meal_datetime = datetime.combine(meal_date, meal_time)
                
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
                            "timestamp": meal_datetime.isoformat()
                        })
                    with open(DATA_FILE, "w") as f:
                        json.dump(st.session_state.logs, f)
                    
                    st.cache_data.clear() # Clear cache so data updates correctly
                    st.success(f"Meal logged at {meal_datetime.strftime('%Y-%m-%d %H:%M')}!")
                    st.rerun()

    with right:
        with st.container(border=True):
            st.markdown("### 🚨 Log a Flare-up")
            with st.form("flare_form", clear_on_submit=True):
                col_date2, col_time2 = st.columns(2)
                with col_date2:
                    flare_date = st.date_input("Flare date", value=datetime.now().date())
                with col_time2:
                    flare_time = st.time_input("Flare time", value=datetime.now().time())
                flare_datetime = datetime.combine(flare_date, flare_time)
                
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
                        "timestamp": flare_datetime.isoformat()
                    })
                    with open(DATA_FILE, "w") as f:
                        json.dump(st.session_state.logs, f)
                    
                    st.cache_data.clear() # Clear cache so data updates correctly
                    st.success(f"Flare-up logged at {flare_datetime.strftime('%Y-%m-%d %H:%M')}.")
                    st.rerun()
with tab2:
    st.subheader("History")
    if st.button("🗑️ Clear All History"):
        st.session_state.logs = []
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        st.cache_data.clear()
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
    
    # Check data maturity
    total_days = len(set([l["timestamp"][:10] for l in logs]))
    if total_days < 30:
        st.info(f"📊 **Data Maturity: Learning Phase ({total_days}/30 days)**. Patterns are emerging, but keep logging to increase confidence and filter out coincidences.")

    scores = run_analysis(logs)

    if not scores:
        st.write("Keep logging! Patterns appear once you have enough meals and safe days recorded.")
    else:
        st.caption("Chemical constituents ranked by how much they exceed your normal flare baseline.")
        
        for s in scores:
            col1, col2 = st.columns([3, 1])
            with col1:
                # Layout the text and button side-by-side using inner columns
                text_col, btn_col = st.columns([0.85, 0.15], vertical_alignment="center")
                with text_col:
                    st.markdown(f"**{s['component']}**")
                with btn_col:
                    if st.button("🔍", key=f"btn_{s['component']}", help=f"Learn more about {s['component']}"):
                        show_chemical_profile(s['component'], s['occurrences'], s['hit_rate'], s["score"])
                
                st.caption(f"Eaten {s['occurrences']} times | Triggered flare {s['hit_rate']}% of the time")
                st.progress(s["score"] / 100)
            with col2:
                st.metric("Score", f"{s['score']}/100")

        st.divider()
        st.subheader("🤖 AI Review")
        
        if st.button("Generate AI Review"):
            with st.spinner("Getting AI's second opinion on the mathematical analysis..."):
                ai_review = ai_review_analysis(logs, scores)

            col1, col2 = st.columns([2, 1])
            with col1:
                st.metric("AI Agreement", ai_review['agreement'].title())
                st.metric("AI Confidence", f"{ai_review['confidence']}%")
            with col2:
                st.write(f"**Reason:**\n{ai_review['reason']}")

            if ai_review.get("notable_support"):
                st.success("**Supporting evidence:**")
                for item in ai_review["notable_support"]:
                    st.write(f"• {item}")

            if ai_review.get("notable_concerns"):
                st.warning("**Areas of uncertainty:**")
                for item in ai_review["notable_concerns"]:
                    st.write(f"• {item}")

with tab4:
    st.subheader("🔮 Risk Forecast")
    st.write("Predict potential triggers before you eat. Now more sensitive to foods with risk.")

    with st.form("predict_form"):
        predict_txt = st.text_input("Enter a meal to check:", 
                                   placeholder="e.g. Tomato pasta with cheese and basil")
        check_btn = st.form_submit_button("🔍 Check Pattern Risk")

    if check_btn and predict_txt:
        with st.spinner("Analyzing meal against your history..."):
            analysis_data = analyze_meal_with_ai(predict_txt)
            comps = extract_chemicals_from_meal(analysis_data)
            analysis_scores = {s["component"]: s["score"] for s in run_analysis(logs)}

            if not comps:
                st.warning("No tracked chemicals found in that meal.")
            else:
                st.markdown(f"**Extracted chemicals:** {len(comps)} components")

                # Calculate max risk for overall assessment
                max_risk = 0
                for c in comps:
                    score = analysis_scores.get(c, 0)
                    max_risk = max(max_risk, score)

                # === MORE SENSITIVE OVERALL RISK ASSESSMENT ===
                if max_risk >= 50:
                    st.error("### ⚠️ HIGH RISK\nThis meal contains chemicals that frequently correlate with your flare-ups.")
                elif max_risk >= 25:
                    st.warning("### ⚡ Moderate Risk\nSome chemicals show notable correlation with your flares.")
                elif max_risk >= 10:
                    st.info("### Low but Notable Risk\nMinor patterns detected in your history.")
                else:
                    st.success("### Likely Low Risk\nNo significant risk patterns found based on your logs.")

                st.divider()

                # === CHEMICALS LISTED INDIVIDUALLY (Like Before) ===
                st.subheader("Chemical Risk Breakdown")
                
                risk_found = False
                for c in sorted(comps, key=lambda x: analysis_scores.get(x, 0), reverse=True):
                    score = analysis_scores.get(c, 0)
                    
                    if score > 0:
                        risk_found = True
                    
                    # Risk level label
                    if score >= 50:
                        level = "🔴 High Risk"
                    elif score >= 25:
                        level = "🟠 Moderate Risk"
                    elif score >= 10:
                        level = "🟡 Low Risk"
                    else:
                        level = "🟢 Minimal Risk"

                    st.write(f"**{c}**: {level} — **{score}/100**")
                    st.progress(score / 100)

                if not risk_found and comps:
                    st.caption("All detected chemicals have very low or no risk correlation in your current data.")

                st.divider()

                # Final Recommendation
                if max_risk >= 40:
                    st.markdown("**💡 Recommendation:** Consider avoiding or eating this meal cautiously and monitor for symptoms within 48 hours.")
                elif max_risk >= 15:
                    st.markdown("**💡 Recommendation:** Moderate caution. Log any symptoms if you try this meal.")
                else:
                    st.markdown("**💡 Recommendation:** This meal appears relatively safe based on your current patterns.")
