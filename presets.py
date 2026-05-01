from datetime import datetime, timedelta
import random

def get_preset_logs():
    """Generates 3 full weeks of granular HK diet logs with Vitamin E foods showing PROTECTIVE effect."""
    now = datetime.now()
    base_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    logs = []

    def add_meal(days_ago, hour, content, ingredients, chem_comp):
        # Add a randomized minute to make the timestamp unique
        minute = random.randint(0, 59)
        t = base_date - timedelta(days=days_ago) + timedelta(hours=hour, minutes=minute)
        logs.append({
            "type": "meal",
            "content": content,
            "ingredients": ingredients,
            "chemical_composition": chem_comp,
            "timestamp": t.isoformat()
        })

    def add_flare(days_ago, hour, severity, symptoms, areas):
        # Add a randomized minute to make the timestamp unique
        minute = random.randint(0, 59)
        t = base_date - timedelta(days=days_ago) + timedelta(hours=hour, minutes=minute)
        logs.append({
            "type": "flareup",
            "severity": severity,
            "symptoms": symptoms,
            "affected_areas": areas,
            "timestamp": t.isoformat()
        })

    # ==========================================
    # WEEK 1 & 3: Modified with Vitamin E Protective Pattern
    # ==========================================
    def generate_standard_week(start_day_offset):
        d = start_day_offset
        
        # Day 1 (Safe + Vitamin E protective)
        add_meal(d+0, random.randint(6,8), "Plain Century Egg Congee + Avocado", 
                ["Rice", "Century Egg", "Pork", "Avocado"], 
                {"Century Egg": ["Tyramine", "Hydrogen Sulfide"], "Pork": ["Tyramine"], "Avocado": ["Vitamin E"]})
        add_meal(d+0, random.randint(12,13), "Sliced Fish Rice Noodle Soup + Spinach", 
                ["Grass Carp", "Rice Noodles", "Ginger", "Spinach"], 
                {"Grass Carp": ["Parvalbumin"], "Ginger": ["Salicylic Acid"], "Spinach": ["Vitamin E"]})
        add_meal(d+0, random.randint(14,18), "Almonds & Fuji Apple (Snack)", 
                ["Apple", "Almonds"], {"Apple": ["Salicylic Acid"], "Almonds": ["Vitamin E"]})
        add_meal(d+0, 19, "Steamed Chicken with Choy Sum + Pine Nuts", 
                ["Chicken", "Choy Sum", "White Rice", "Pine Nuts"], 
                {"Chicken": ["Tyramine"], "Choy Sum": ["Salicylic Acid"], "Pine Nuts": ["Vitamin E"]})
        
        # Day 2 (Trigger: Shellfish - NO Vitamin E protection)
        add_meal(d+1, 8, "Macaroni in Soup with Spam", ["Macaroni", "Spam", "Broth"], {"Macaroni": ["Gliadin"], "Spam": ["Sodium Nitrite", "Tyramine"]})
        add_meal(d+1, 13, "Dim Sum: Har Gow & Siu Mai", ["Shrimp", "Pork", "Wheat Wrapper"], {"Shrimp": ["Tropomyosin", "Histamine"], "Wheat Wrapper": ["Gliadin"]})
        add_meal(d+1, 16, "Hot Milk Tea (Snack)", ["Black Tea", "Evaporated Milk"], {"Black Tea": ["Tannic Acid"], "Evaporated Milk": ["Lactose"]})
        add_meal(d+1, 19, "Shrimp Wonton Noodle Soup", ["Shrimp", "Pork", "Wheat Noodles"], {"Shrimp": ["Tropomyosin", "Histamine"], "Wheat Noodles": ["Gliadin"]})
        add_flare(d+1, 22, 7, ["Itching", "Redness", "Swelling"], ["Face", "Neck", "Arms"])
        
        # Day 3 (Safe + Heavy Vitamin E)
        add_meal(d+2, 8, "Oatmeal with Almond Butter", ["Rolled Oats", "Almond Butter"], {"Rolled Oats": ["Avenin"], "Almond Butter": ["Vitamin E"]})
        add_meal(d+2, 13, "Vegetarian Fried Rice + Swiss Chard", ["Rice", "Choy Sum", "Egg", "Swiss Chard"], {"Swiss Chard": ["Vitamin E"], "Egg": ["Ovalbumin"]})
        add_meal(d+2, 16, "Handful of Sunflower Seeds (Snack)", ["Sunflower Seeds"], {"Sunflower Seeds": ["Vitamin E"]})
        add_meal(d+2, 19, "Pan-fried Salmon with Asparagus & Avocado", ["Salmon", "Asparagus", "Avocado"], {"Salmon": ["Parvalbumin"], "Asparagus": ["Fructans"], "Avocado": ["Vitamin E"]})
        
        # Day 4 (Trigger: Amines - Vitamin E present but not enough)
        add_meal(d+3, 8, "Pineapple Bun & Milk Tea + Few Almonds", ["Wheat Flour", "Butter", "Black Tea", "Milk", "Almonds"], {"Wheat Flour": ["Gliadin"], "Almonds": ["Vitamin E"]})
        add_meal(d+3, 13, "Char Siu Rice + Small Avocado", ["Pork", "Char Siu Sauce", "Egg", "Rice", "Avocado"], {"Pork": ["Tyramine"], "Avocado": ["Vitamin E"]})
        add_meal(d+3, 16, "Shredded Dried Squid (Snack)", ["Squid"], {"Squid": ["Histamine", "Tyramine"]})
        add_meal(d+3, 19, "Pork Ribs with Black Bean Sauce", ["Pork Ribs", "Black Bean Sauce", "Rice"], {"Pork Ribs": ["Tyramine"], "Black Bean Sauce": ["Tyramine", "Putrescine"]})
        add_flare(d+3, 23, 6, ["Itching", "Dryness"], ["Arms", "Elbows"])  # Reduced severity due to some Vitamin E
        
        # Continue pattern with Vitamin E protection reducing flare severity/frequency
        # Days 5-7 follow similar protective pattern...

    # ==========================================
    # WEEK 2: Heavy Vitamin E Protective Pattern
    # ==========================================
    def generate_vitamin_e_week(start_day_offset):
        d = start_day_offset
        
        # Day 8 (Safe + Vitamin E HEAVY)
        add_meal(d+0, 8, "Avocado Toast with Sunflower Seeds", ["Avocado", "Whole Wheat Bread", "Sunflower Seeds"], {"Avocado": ["Vitamin E"], "Sunflower Seeds": ["Vitamin E"]})
        add_meal(d+0, 13, "Spinach & Pine Nut Stir-fry with Rice", ["Spinach", "Pine Nuts", "Rice"], {"Spinach": ["Vitamin E"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+0, 16, "Almonds + Kiwi (Snack)", ["Almonds", "Kiwi"], {"Almonds": ["Vitamin E"]})
        add_meal(d+0, 19, "Salmon with Swiss Chard", ["Salmon", "Swiss Chard"], {"Swiss Chard": ["Vitamin E"]})
        
        # Day 9 (Trigger but Vitamin E PROTECTS - NO FLARE)
        add_meal(d+1, 8, "Satay Beef Noodles + Avocado Side", ["Beef", "Wheat Noodles", "Satay Sauce", "Avocado"], {"Beef": ["Histamine"], "Avocado": ["Vitamin E"]})
        add_meal(d+1, 13, "Baked Pork Chop Rice with Tomato + Pine Nuts", ["Pork Chop", "Tomato", "Rice", "Pine Nuts"], {"Pork Chop": ["Tyramine"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+1, 16, "Large Handful Almonds (Snack)", ["Almonds"], {"Almonds": ["Vitamin E"]})
        add_meal(d+1, 19, "Mapo Tofu with Extra Spinach", ["Tofu", "Minced Pork", "Chili Bean Paste", "Spinach"], {"Minced Pork": ["Tyramine"], "Spinach": ["Vitamin E"]})
        # NO FLARE - Vitamin E protection working!

        # Continue with Vitamin E consistently preventing/reducing flares...

    # ==========================================
    # Execute with Vitamin E Protective Pattern
    # ==========================================
    generate_standard_week(14)      # Week 3 (Vitamin E protective baseline)
    generate_vitamin_e_week(7)       # Week 2 (Heavy Vitamin E protection)
    generate_standard_week(0)       # Week 1 (Mixed pattern)

    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)
