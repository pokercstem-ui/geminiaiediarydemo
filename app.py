import streamlit as st
import json
import os
import re
from datetime import datetime
import openai
from PIL import Image

# --- NEW: Import the presets from the separate file ---
from presets import get_preset_logs

# --- PAGE SETUP ---
try:
    icon = Image.open("ed01.jpg")
except FileNotFoundError:
    icon = "🧩" 

st.set_page_config(page_title="E-diary", page_icon=icon)

# ==========================================
# 🍎 HIGH-END iOS AESTHETIC CSS INJECTION
# ==========================================
st.markdown(
    """
    <style>
    /* 1. San Francisco System Font Stack */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* 2. Vibrant Mesh Gradient Background */
    .stApp {
        background-color: var(--background-color);
        background-image: 
            radial-gradient(at 0% 0%, rgba(52, 199, 89, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(255, 59, 48, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(0, 122, 255, 0.08) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(255, 149, 0, 0.08) 0px, transparent 50%);
        background-attachment: fixed;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 120px !important; 
    }
    
    /* 3. Glassmorphism Bottom Nav (Frosted Glass) */
    div[data-testid="stTabs"] > div > div:first-of-type {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background-color: rgba(128, 128, 128, 0.05) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        z-index: 999999 !important;
        border-top: 1px solid rgba(128,128,128,0.15) !important;
        padding-bottom: max(env(safe-area-inset-bottom), 15px) !important;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        display: flex !important;
        width: 100% !important;
        justify-content: space-around !important;
        gap: 0 !important;
    }

    /* 4. Tab Button Formatting (Stacked Icons) - Now handles 5 tabs smoothly */
    div[data-testid="stTabs"] [role="tablist"] > button p {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 4px !important;
        font-size: 0.80rem !important; 
        font-weight: 600 !important;
        margin: 0 !important;
        line-height: 1 !important;
    }
    
    div[data-testid="stTabs"] [role="tablist"] > button[aria-selected="true"] {
        opacity: 1 !important;
        background-color: rgba(128, 128, 128, 0.05) !important; 
    }

    /* Stack the Material icon on top of the text */
    div[data-testid="stTabs"] [role="tablist"] > button p {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 4px !important;
        font-size: 0.70rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        line-height: 1 !important;
    }

    /* Increase the icon size */
    div[data-testid="stTabs"] [role="tablist"] > button span.material-symbols-rounded {
        font-size: 1.5rem !important;
        margin: 0 !important;
    }

    /* 5. Themed Icon Colors (Added Purple for Forum) */
    div[data-testid="stTabs"] [role="tablist"] > button:nth-child(1) span.material-symbols-rounded { color: #007AFF !important; } /* Blue */
    div[data-testid="stTabs"] [role="tablist"] > button:nth-child(2) span.material-symbols-rounded { color: #34C759 !important; } /* Green */
    div[data-testid="stTabs"] [role="tablist"] > button:nth-child(3) span.material-symbols-rounded { color: #5856D6 !important; } /* Indigo */
    div[data-testid="stTabs"] [role="tablist"] > button:nth-child(4) span.material-symbols-rounded { color: #FF9500 !important; } /* Orange */
    div[data-testid="stTabs"] [role="tablist"] > button:nth-child(5) span.material-symbols-rounded { color: #AF52DE !important; } /* Purple */

    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        top: 0 !important;
        bottom: auto !important;
        background-color: var(--primary-color) !important;
        border-radius: 0 0 4px 4px !important;
        height: 3px !important;
    }

    /* 6. Tactile Buttons (Squircle + Springy Scale) */
    .stButton > button, .stDownloadButton > button {
        border-radius: 24px !important;
        border: 1px solid rgba(128,128,128,0.2) !important;
        background: rgba(128,128,128,0.05) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275), background 0.2s !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:active, .stDownloadButton > button:active {
        transform: scale(0.96) !important; 
        background: rgba(128,128,128,0.15) !important;
    }

    .stSlider > div > div > div > div {
        border-radius: 12px !important;
    }

    .stButton>button {padding: 0.3rem 0.6rem;} 

    /* FORUM IOS TOOLTIPS */
    .ios-tooltip-trigger {
        position: relative;
        color: #007AFF;
        font-weight: 600;
        cursor: pointer;
        text-decoration: underline;
        text-decoration-style: dotted;
        text-underline-offset: 4px;
        transition: color 0.2s;
    }
    
    .ios-tooltip-trigger:active, .ios-tooltip-trigger:focus {
        outline: none;
        color: #0056b3;
    }

    .ios-tooltip {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        bottom: 130%;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        width: max-content;
        max-width: 250px;
        background: rgba(30, 30, 30, 0.85); 
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        color: #ffffff;
        text-align: center;
        padding: 12px 14px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 500;
        line-height: 1.4;
        z-index: 1000;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        pointer-events: none;
    }

    .ios-tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -6px;
        border-width: 6px;
        border-style: solid;
        border-color: rgba(30, 30, 30, 0.85) transparent transparent transparent;
    }

    .ios-tooltip-trigger:hover .ios-tooltip,
    .ios-tooltip-trigger:active .ios-tooltip,
    .ios-tooltip-trigger:focus .ios-tooltip {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
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
    if not API_KEY:
        return None
    return openai.OpenAI(base_url="https://api.llm7.io/v1", api_key=API_KEY)

client = get_ai_client()

# --- DATA LOADING ---
@st.cache_data
def load_data(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                existing_logs = json.load(f)
                if isinstance(existing_logs, list):
                    return sorted(existing_logs, key=lambda x: x["timestamp"], reverse=True)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    presets = get_preset_logs()
    final_logs = sorted(presets, key=lambda x: x["timestamp"], reverse=True)

    with open(filepath, "w") as f:
        json.dump(final_logs, f, indent=2)

    return final_logs

# --- AI PARSING & INFO ---
@st.cache_data(show_spinner=False)
def analyze_meal_with_ai(text):
    if not client:
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
        f"Make it concise, don't add if-cases, think about the general case. You should select at most 4 chemicals for each ingredient according to those which are more abundant or cause more serious reactions. \n"
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
        return {"ingredients": [], "chemical_composition": {}}

@st.cache_data(show_spinner=False)
def get_chemical_info_from_ai(chemical_name):
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

def enforce_chemical_consistency(analysis_data, logs):
    master_dict = {}
    for l in reversed(logs):
        if l["type"] == "meal":
            for ing, chems in l.get("chemical_composition", {}).items():
                master_dict[ing.strip().title()] = chems
                
    final_composition = {}
    final_ingredients = []
    
    for ing in analysis_data.get("ingredients", []):
        final_ingredients.append(ing.strip().title())
        
    for ing, chems in analysis_data.get("chemical_composition", {}).items():
        standard_ing = ing.strip().title()
        if standard_ing in master_dict:
            final_composition[standard_ing] = master_dict[standard_ing]
        else:
            final_composition[standard_ing] = chems
            
    return {
        "ingredients": final_ingredients,
        "chemical_composition": final_composition
    }

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

    SMOOTHING_WEIGHT = 3
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


# ==========================================
# 🔮 REUSABLE RISK FORECAST ENGINE
# ==========================================
def get_risk_forecast(meal_txt, logs):
    """Encapsulates the mathematical risk logic to be used anywhere."""
    analysis_data = analyze_meal_with_ai(meal_txt)
    analysis_data = enforce_chemical_consistency(analysis_data, logs)
    
    comps = extract_chemicals_from_meal(analysis_data)
    analysis_scores = {s["component"]: s["score"] for s in run_analysis(logs)}

    if not comps:
        return {"risk": 0, "comps": [], "scores": analysis_scores}
    
    trigger_scores = [analysis_scores.get(c, 0) for c in comps]
    if trigger_scores:
        max_score = max(trigger_scores)
        avg_score = sum(trigger_scores) / len(trigger_scores)
        final_risk = int(max_score * 0.7 + avg_score * 0.3)
        final_risk = min(final_risk, 100)
    else:
        final_risk = 0
    
    return {"risk": final_risk, "comps": comps, "scores": analysis_scores}


# ==========================================
# 🌐 COMMUNITY FORUM LOGIC & MOCK DATA
# ==========================================
FORUM_DICTIONARY = {
    "ceramides": "Lipids (fats) found naturally in high concentrations in the uppermost layers of the skin. Eczema-prone skin often lacks ceramides, leading to a compromised barrier.",
    "topical steroids": "Anti-inflammatory creams or ointments prescribed to reduce severe eczema redness and swelling during flare-ups.",
    "histamine": "A chemical produced by your body during an allergic reaction. It binds to receptors and causes the intense itching associated with hives and eczema.",
    "tsw": "Topical Steroid Withdrawal. A severe skin reaction that can happen when discontinuing moderate to high-potency topical steroids after prolonged use.",
    "wet wrap therapy": "An intense treatment involving applying wet bandages over a layer of thick moisturizer or medication, then covering it with a dry layer to trap moisture.",
    "probiotics": "Live bacteria and yeasts (often found in yogurt or supplements) that support gut health, which some studies link to improved immune and skin responses.",
    "patch testing": "A dermatological method used to determine whether a specific substance causes allergic inflammation on a patient's skin."
}

def highlight_keywords(text):
    highlighted_text = text
    for kw, definition in FORUM_DICTIONARY.items():
        pattern = re.compile(rf'\b({kw})\b', re.IGNORECASE)
        replacement = f'<span class="ios-tooltip-trigger" tabindex="0">\\1<span class="ios-tooltip">{definition}</span></span>'
        highlighted_text = pattern.sub(replacement, highlighted_text)
    return highlighted_text

# Initialize mock forum posts in session state (Now with Likes and Comments!)
if "forum_posts" not in st.session_state:
    st.session_state.forum_posts = [
        {
            "id": 1,
            "author": "HealingJourney22",
            "category": "Skincare",
            "timestamp": "15 mins ago",
            "content": "Currently going through TSW and the flaking is unbelievable. Finding a moisturizer that doesn't burn is so hard right now. Does anyone have recommendations for gentle ointments rich in ceramides?",
            "likes": 14,
            "comments": [
                {"author": "ItchyMom", "timestamp": "10 mins ago", "content": "Aquaphor was the only thing that didn't sting for us during the worst of it!"},
                {"author": "PatchTester", "timestamp": "5 mins ago", "content": "Make sure you check the ingredients for preservatives if you are highly sensitive right now."}
            ]
        },
        {
            "id": 2,
            "author": "GutHealthGuru",
            "category": "Recipes",
            "timestamp": "1 hour ago",
            "content": "Here is my go-to anti-inflammatory breakfast smoothie! 1/2 cup frozen blueberries, 1 handful fresh kale, 1 scoop hemp seeds, and 1/2 cup coconut yogurt packed with probiotics. It's very low histamine and helps cool down my skin from the inside out.",
            "likes": 32,
            "comments": [
                {"author": "ChefSafe", "timestamp": "30 mins ago", "content": "I make almost the exact same thing but I add half an avocado for extra healthy fats. It makes it so creamy!"}
            ]
        },
        {
            "id": 3,
            "author": "ChefSafe",
            "category": "Recipes",
            "timestamp": "3 hours ago",
            "content": "Just made the most amazing low-histamine chicken broth! The trick is to pressure cook it for only 45 minutes instead of a slow simmer. It totally prevents the histamine buildup that usually causes my flare-ups.",
            "likes": 45,
            "comments": []
        },
        {
            "id": 4,
            "author": "AllergyClinic",
            "category": "Workshops",
            "timestamp": "1 day ago",
            "content": "Reminder: We are hosting a free webinar this Friday on identifying hidden contact allergens. If you've hit a plateau in your healing, proper patch testing might be the key to figuring out what is holding you back!",
            "likes": 88,
            "comments": [
                {"author": "DocDerma", "timestamp": "12 hours ago", "content": "Highly recommend this workshop to all my patients."}
            ]
        }
    ]

# State tracker for our "Screen Push" navigation
if "selected_post_id" not in st.session_state:
    st.session_state.selected_post_id = None


# --- LOAD DATA TO SESSION ---
st.session_state.logs = load_data(DATA_FILE)
logs = st.session_state.logs

# --- SIDEBAR & TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    ":material/edit_square: Input", 
    ":material/history: History", 
    ":material/analytics: Analysis", 
    ":material/online_prediction: Forecast",
    ":material/forum: Community"
])

with tab1:
    st.markdown("### :material/edit_square: Log Activity")
    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("""
                <div style="background: rgba(128,128,128,0.05); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); padding: 12px 16px; border-radius: 20px; border: 1px solid rgba(128,128,128,0.15); margin-bottom: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                    <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700;">🍎 Log a Meal</h3>
                </div>
            """, unsafe_allow_html=True)
            with st.form("meal_form", clear_on_submit=True):
                col_date1, col_time1 = st.columns(2)
                with st.form("meal_form", clear_on_submit=True):
                col_date1, col_time1 = st.columns(2)
                with col_date1:
                    meal_date = st.date_input("Meal date") 
                with col_time1:
                    meal_time = st.time_input("Meal time") 
                meal_datetime = datetime.combine(meal_date, meal_time)
                
                meal_txt = st.text_input("What did you eat?", placeholder="e.g. French fries and spicy dipping sauce")
                save_meal = st.form_submit_button("Save Meal")
                
                if save_meal and meal_txt:
                    with st.spinner("AI is extracting chemical composition..."):
                        analysis_data = analyze_meal_with_ai(meal_txt)
                        analysis_data = enforce_chemical_consistency(analysis_data, st.session_state.logs)
                        
                    st.session_state.logs.insert(0, {
                            "type": "meal",
                            "content": meal_txt,
                            "ingredients": analysis_data["ingredients"],
                            "chemical_composition": analysis_data["chemical_composition"],
                            "timestamp": meal_datetime.isoformat()
                        })
                    with open(DATA_FILE, "w") as f:
                        json.dump(st.session_state.logs, f, indent=2)
                    
                    st.cache_data.clear() 
                    st.success(f"Meal logged at {meal_datetime.strftime('%Y-%m-%d %H:%M')}!")
                    st.rerun()

    with right:
        with st.container(border=True):
            st.markdown("""
                <div style="background: rgba(255, 59, 48, 0.05); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); padding: 12px 16px; border-radius: 20px; border: 1px solid rgba(255, 59, 48, 0.2); margin-bottom: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                    <h3 style="margin: 0; color: #FF3B30; font-size: 1.1rem; font-weight: 700;">🚨 Log a Flare-up</h3>
                </div>
            """, unsafe_allow_html=True)
            with st.form("flare_form", clear_on_submit=True):
                col_date2, col_time2 = st.columns(2)
                with col_date2:
                    # Removed the datetime.now() value override
                    flare_date = st.date_input("Flare date")
                with col_time2:
                    # Removed the datetime.now() value override
                    flare_time = st.time_input("Flare time")
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
                        json.dump(st.session_state.logs, f, indent=2)
                    
                    st.cache_data.clear() 
                    st.success(f"Flare-up logged at {flare_datetime.strftime('%Y-%m-%d %H:%M')}.")
                    st.rerun()

with tab2:
    st.markdown("### :material/history: History")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.logs = []
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        st.cache_data.clear()
        st.rerun()
    st.write("")

    for l in logs:
        t = datetime.fromisoformat(l["timestamp"]).strftime("%b %d, %H:%M")
        
        if l["type"] == "meal":
            ingredients = l.get("ingredients", [])
            chem_comp = l.get("chemical_composition", {})
            
            st.markdown(f"""
            <div style="background: rgba(128,128,128,0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(128,128,128,0.15); border-left: 4px solid #34C759; border-radius: 24px; padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                <div style="font-weight: 600; font-size: 1.05rem;">🍴 {l['content']}</div>
                <div style="font-size: 0.85rem; opacity: 0.6;">{t}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if ingredients or chem_comp:
                with st.expander("View Breakdown"):
                    for ing in ingredients:
                        chems = chem_comp.get(ing, [])
                        composition = ", ".join(chems) if isinstance(chems, list) else chems
                        st.markdown(f"- **{ing}**: {composition}")
                        
        else:
            symptoms = ", ".join(l.get("symptoms", [])) or "Not specified"
            areas = ", ".join(l.get("affected_areas", [])) or "Not specified"

            st.markdown(f"""
            <div style="background: rgba(255, 59, 48, 0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 59, 48, 0.15); border-left: 4px solid #FF3B30; border-radius: 24px; padding: 16px; margin-bottom: 12px; display: flex; flex-direction: column; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div style="font-weight: 700; color: #FF3B30; font-size: 1.05rem;">🚨 Flare-up (Severity {l.get('severity', 0)})</div>
                    <div style="font-size: 0.85rem; opacity: 0.6;">{t}</div>
                </div>
                <div style="font-size: 0.9rem; opacity: 0.8;"><b>Symptoms:</b> {symptoms}</div>
                <div style="font-size: 0.9rem; opacity: 0.8;"><b>Areas:</b> {areas}</div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("### :material/analytics: Analysis")
    
    total_days = len(set([l["timestamp"][:10] for l in logs]))
    if total_days < 30:
        st.markdown(f"""
        <div style="background: rgba(52, 199, 89, 0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(52, 199, 89, 0.2); border-radius: 24px; padding: 16px; margin-bottom: 20px; border-left: 4px solid #34C759; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
            <div style="font-weight: 600; font-size: 1rem;">📊 Data Maturity: Learning Phase ({total_days}/30 days)</div>
            <div style="font-size: 0.85rem; opacity: 0.8; margin-top: 6px;">Patterns are emerging, but keep logging to increase confidence and filter out coincidences.</div>
        </div>
        """, unsafe_allow_html=True)

    scores = run_analysis(logs)

    if not scores:
        st.write("Keep logging! Patterns appear once you have enough meals and safe days recorded.")
    else:
        st.caption("Chemical constituents ranked by how much they exceed your normal flare baseline.")
        
        for s in scores:
            score_val = s["score"]
            if score_val >= 60:
                bar_color = "#FF3B30"
                level = "High"
            elif score_val >= 45:
                bar_color = "#FF9500"
                level = "Moderate"
            elif score_val >= 25:
                bar_color = "#F5AD27"
                level = "Low"
            else:
                bar_color = "#34C759"
                level = "Minimal"

            col_html, col_btn = st.columns([0.88, 0.12], vertical_alignment="center")
            
            with col_html:
                st.markdown(f"""
                <div style="background: rgba(128,128,128,0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(128,128,128,0.15); border-radius: 24px; padding: 12px 16px; margin-bottom: 10px; border-left: 4px solid {bar_color}; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <div style="font-weight: 700; font-size: 1rem;">{s['component']}</div>
                            <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 4px;">
                                Eaten {s['occurrences']}x • {s['hit_rate']}% Flare Rate
                            </div>
                        </div>
                        <div style="text-align: right; min-width: 60px;">
                            <span style="font-size: 1.2rem; font-weight: 700; color: {bar_color};">{score_val}</span>
                            <span style="font-size: 0.8rem; opacity: 0.6;">/100</span>
                        </div>
                    </div>
                    <div style="margin-top: 10px; height: 4px; background: rgba(128, 128, 128, 0.15); border-radius: 10px; overflow: hidden;">
                        <div style="width: {score_val}%; height: 100%; background: {bar_color}; border-radius: 10px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_btn:
                if st.button("🔍", key=f"btn_{s['component']}", help=f"Learn more about {s['component']}", use_container_width=True):
                    show_chemical_profile(s['component'], s['occurrences'], s['hit_rate'], s["score"])

with tab4:
    st.markdown("### :material/online_prediction: Risk Forecast")
    st.markdown("**Check your meal before eating**")

    with st.form("predict_form"):
        predict_txt = st.text_input(
            "Meal to check", 
            placeholder="e.g. Shrimp wonton noodle soup with avocado",
            label_visibility="collapsed"
        )
        check_btn = st.form_submit_button("Check Risk", use_container_width=True)

    if check_btn and predict_txt:
        with st.spinner("Analyzing against your history..."):
            
            # Using our new reusable engine
            forecast = get_risk_forecast(predict_txt, logs)
            final_risk = forecast["risk"]
            comps = forecast["comps"]
            analysis_scores = forecast["scores"]

            if not comps:
                st.warning("No tracked chemicals found in that meal.")
            else:
                if final_risk >= 70:
                    color = "rgba(255, 59, 48,"
                    status = "HIGH RISK"
                elif final_risk >= 45:
                    color = "rgba(255, 149, 0,"
                    status = "MODERATE RISK"
                elif final_risk >= 20:
                    color = "rgba(245, 173, 39,"
                    status = "LOW RISK"
                else:
                    color = "rgba(52, 199, 89,"
                    status = "LIKELY SAFE"

                st.markdown(f"""
                <div style="background: {color} 0.1); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border: 1px solid {color} 0.3); border-radius: 24px; padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; margin: 12px 0 20px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.05);">
                    <h2 style="margin: 0; color: {color} 1); font-weight: 800; font-size: 1.3rem; letter-spacing: -0.5px;">
                        {status}
                    </h2>
                    <p style="font-size: 1.8rem; font-weight: 800; margin: 0; color: {color} 1);">
                        {final_risk}<span style="font-size: 1rem; opacity: 0.6; font-weight: 600;">/100</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Chemical Breakdown**")

                sorted_comps = sorted(comps, key=lambda x: analysis_scores.get(x, 0), reverse=True)
                top_5_comps = sorted_comps[:5]
                other_comps = sorted_comps[5:]

                def render_chemical_bar(c):
                    score = analysis_scores.get(c, 0)
                    if score >= 60:
                        bar_color = "#FF3B30"
                        level = "High"
                    elif score >= 45:
                        bar_color = "#FF9500"
                        level = "Moderate"
                    elif score >= 25:
                        bar_color = "#F5AD27"
                        level = "Low"
                    else:
                        bar_color = "#34C759"
                        level = "Minimal"

                    st.markdown(f"""
                    <div style="background: rgba(128,128,128,0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(128,128,128,0.15); border-radius: 20px; padding: 12px 16px; margin-bottom: 10px; border-left: 4px solid {bar_color}; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex: 1;">
                                <div style="font-weight: 700; font-size: 1rem;">{c}</div>
                                <div style="font-size: 0.8rem; opacity: 0.6; font-weight: 500; margin-top: 4px;">{level} Risk</div>
                            </div>
                            <div style="text-align: right; min-width: 60px;">
                                <span style="font-size: 1.2rem; font-weight: 700; color: {bar_color};">{score}</span>
                                <span style="font-size: 0.8rem; opacity: 0.6;">/100</span>
                            </div>
                        </div>
                        <div style="margin-top: 10px; height: 4px; background: rgba(128, 128, 128, 0.15); border-radius: 10px; overflow: hidden;">
                            <div style="width: {score}%; height: 100%; background: {bar_color}; border-radius: 10px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                for c in top_5_comps:
                    render_chemical_bar(c)

                if other_comps:
                    with st.expander(f"🧪 View {len(other_comps)} other chemicals"):
                        for c in other_comps:
                            render_chemical_bar(c)

                st.markdown("<hr style='margin: 20px 0; border-color: rgba(128,128,128,0.2);'/>", unsafe_allow_html=True)
                if final_risk >= 60:
                    st.error("**High caution** — Consider avoiding this meal.")
                elif final_risk >= 40:
                    st.warning("**Moderate caution** — Monitor symptoms if you eat it.")
                else:
                    st.success("**Looks safe** — This meal appears relatively low risk.")

# ==========================================
# 🌐 TAB 5: COMMUNITY FORUM
# ==========================================
with tab5:
    # ---------------------------------------------------------
    # VIEW: SINGLE POST (Comments & Likes "Screen Push")
    # ---------------------------------------------------------
    if st.session_state.selected_post_id is not None:
        if st.button("Back to Community", use_container_width=True):
            st.session_state.selected_post_id = None
            st.rerun()
            
        # Find the specific post
        active_post = next((p for p in st.session_state.forum_posts if p["id"] == st.session_state.selected_post_id), None)
        
        if active_post:
            st.markdown(f"### Post by {active_post['author']}")
            
            # Styling colors
            if active_post["category"] == "Food": cat_color = "#FF9500" 
            elif active_post["category"] == "Recipes": cat_color = "#FF2D55" 
            elif active_post["category"] == "Skincare": cat_color = "#AF52DE" 
            else: cat_color = "#5856D6" 

            processed_content = highlight_keywords(active_post["content"])

            st.markdown(f"""
            <div style="background: rgba(128,128,128,0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(128,128,128,0.15); border-radius: 24px; padding: 18px; margin-bottom: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div>
                        <div style="font-weight: 700; font-size: 1.05rem;">{active_post['author']}</div>
                        <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 2px;">{active_post['timestamp']}</div>
                    </div>
                    <div style="background: {cat_color}20; color: {cat_color}; border: 1px solid {cat_color}40; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">
                        {active_post['category']}
                    </div>
                </div>
                <div style="font-size: 1rem; line-height: 1.5; opacity: 0.9;">
                    {processed_content}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Interactive Like Button
            if st.button(f"❤️ Like ({active_post['likes']})", key=f"like_detail_{active_post['id']}"):
                active_post['likes'] += 1
                st.rerun()

            st.markdown("<hr style='margin: 20px 0; border-color: rgba(128,128,128,0.2);'/>", unsafe_allow_html=True)
            st.markdown("#### Comments")
            
            # Display existing comments
            for c in active_post["comments"]:
                st.markdown(f"""
                <div style="background: rgba(128,128,128,0.03); border-radius: 16px; padding: 12px 16px; margin-bottom: 8px;">
                    <span style="font-weight: 700; font-size: 0.9rem;">{c['author']}</span>
                    <span style="font-size: 0.75rem; opacity: 0.6; margin-left: 8px;">{c['timestamp']}</span>
                    <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 4px;">{c['content']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Add new comment
            with st.form("new_comment_form", clear_on_submit=True):
                new_com = st.text_input("Add a comment...", placeholder="Type your thoughts here...")
                if st.form_submit_button("Post Comment") and new_com:
                    active_post["comments"].append({
                        "author": "You", 
                        "timestamp": "Just now", 
                        "content": new_com
                    })
                    st.rerun()

    # ---------------------------------------------------------
    # VIEW: MAIN COMMUNITY FEED
    # ---------------------------------------------------------
    else:
        st.markdown("### :material/forum: Community Forum")
        
        category_filter = st.radio(
            "Filter by category",
            ["All", "Food", "Recipes", "Skincare", "Workshops"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.write("") 
        
        with st.expander("✏️ Write a new post..."):
            with st.form("new_post_form", clear_on_submit=True):
                new_cat = st.selectbox("Category", ["Food", "Recipes", "Skincare", "Workshops"])
                new_content = st.text_area("What's on your mind?", height=100)
                submit_post = st.form_submit_button("Post to Community")
                
                if submit_post and new_content:
                    st.session_state.forum_posts.insert(0, {
                        "id": len(st.session_state.forum_posts) + 1,
                        "author": "You",
                        "category": new_cat,
                        "timestamp": "Just now",
                        "content": new_content,
                        "likes": 0,
                        "comments": []
                    })
                    st.rerun()

        st.markdown("<hr style='margin: 16px 0; border-color: rgba(128,128,128,0.2);'/>", unsafe_allow_html=True)

        for post in st.session_state.forum_posts:
            if category_filter == "All" or post["category"] == category_filter:
                
                if post["category"] == "Food": cat_color = "#FF9500" 
                elif post["category"] == "Recipes": cat_color = "#FF2D55" 
                elif post["category"] == "Skincare": cat_color = "#AF52DE" 
                else: cat_color = "#5856D6" 
                    
                processed_content = highlight_keywords(post["content"])

                # Post HTML Card
                st.markdown(f"""
                <div style="background: rgba(128,128,128,0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(128,128,128,0.15); border-radius: 24px; padding: 18px; margin-bottom: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                        <div>
                            <div style="font-weight: 700; font-size: 1.05rem;">{post['author']}</div>
                            <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 2px;">{post['timestamp']}</div>
                        </div>
                        <div style="background: {cat_color}20; color: {cat_color}; border: 1px solid {cat_color}40; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">
                            {post['category']}
                        </div>
                    </div>
                    <div style="font-size: 1rem; line-height: 1.5; opacity: 0.9;">
                        {processed_content}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # RECIPE ON-DEMAND RISK SCANNER
                if post["category"] == "Recipes":
                    risk_state_key = f"risk_result_{post['id']}"
                    
                    if risk_state_key not in st.session_state:
                        if st.button("🪄 Check My Risk for this Recipe", key=f"risk_btn_{post['id']}", use_container_width=True):
                            with st.spinner("Analyzing against your diary..."):
                                st.session_state[risk_state_key] = get_risk_forecast(post["content"], logs)
                                st.rerun()
                                
                    if risk_state_key in st.session_state:
                        res = st.session_state[risk_state_key]
                        frisk = res["risk"]
                        
                        if frisk >= 70: r_color, status = "rgba(255, 59, 48,", "HIGH RISK"
                        elif frisk >= 45: r_color, status = "rgba(255, 149, 0,", "MODERATE RISK"
                        elif frisk >= 20: r_color, status = "rgba(245, 173, 39,", "LOW RISK"
                        else: r_color, status = "rgba(52, 199, 89,", "LIKELY SAFE"
                        
                        st.markdown(f"""
                        <div style="background: {r_color} 0.1); border: 1px solid {r_color} 0.3); border-radius: 16px; padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-weight: 700; color: {r_color} 1); font-size: 0.9rem;">Your Risk: {status}</span>
                            <span style="font-weight: 800; color: {r_color} 1);">{frisk}/100</span>
                        </div>
                        """, unsafe_allow_html=True)

                # Post Actions Bar (Likes and View Discussion)
                c1, c2 = st.columns([0.3, 0.7])
                with c1:
                    if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}", use_container_width=True):
                        post['likes'] += 1
                        st.rerun()
                with c2:
                    if st.button(f"💬 View Discussion ({len(post['comments'])})", key=f"view_{post['id']}", use_container_width=True):
                        st.session_state.selected_post_id = post["id"]
                        st.rerun()
                
                st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
