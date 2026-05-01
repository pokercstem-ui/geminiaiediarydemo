from datetime import datetime, timedelta
import random

def get_preset_logs():
    """Generates 3 full weeks of granular HK diet logs with Vitamin E foods showing PROTECTIVE effect."""
    now = datetime.now()
    base_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    logs = []

    def add_meal(days_ago, hour, content, ingredients, chem_comp):
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
    # Standard Week (Mixed - some triggers with partial Vitamin E protection)
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
        add_flare(d+3, 23, 6, ["Itching", "Dryness"], ["Arms", "Elbows"])   # Reduced severity due to Vitamin E
        
        # Day 5 (Safe + Vitamin E)
        add_meal(d+4, random.randint(7,9), "Avocado Smoothie Bowl with Sunflower Seeds", 
                ["Avocado", "Banana", "Sunflower Seeds", "Oats"], 
                {"Avocado": ["Vitamin E"], "Sunflower Seeds": ["Vitamin E"]})
        add_meal(d+4, random.randint(12,14), "Grilled Fish with Spinach Salad", 
                ["Grass Carp", "Spinach", "Pine Nuts"], 
                {"Grass Carp": ["Parvalbumin"], "Spinach": ["Vitamin E"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+4, 16, "Almonds & Pear (Snack)", ["Almonds", "Pear"], {"Almonds": ["Vitamin E"]})
        add_meal(d+4, 19, "Chicken Stir-fry with Choy Sum & Avocado", 
                ["Chicken", "Choy Sum", "Avocado", "Rice"], 
                {"Chicken": ["Tyramine"], "Choy Sum": ["Salicylic Acid"], "Avocado": ["Vitamin E"]})
        
        # Day 6 (Mild trigger with strong Vitamin E protection)
        add_meal(d+5, 8, "Cheese Toast with Almond Butter", ["Bread", "Cheese", "Almond Butter"], {"Bread": ["Gliadin"], "Almond Butter": ["Vitamin E"]})
        add_meal(d+5, 13, "Beef Fried Rice with Extra Spinach", ["Beef", "Rice", "Spinach", "Pine Nuts"], {"Beef": ["Histamine"], "Spinach": ["Vitamin E"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+5, 16, "Large Handful Sunflower Seeds", ["Sunflower Seeds"], {"Sunflower Seeds": ["Vitamin E"]})
        add_meal(d+5, 19, "Salmon with Swiss Chard & Pine Nuts", ["Salmon", "Swiss Chard", "Pine Nuts"], {"Swiss Chard": ["Vitamin E"], "Pine Nuts": ["Vitamin E"]})
        
        # Day 7 (Safe + Heavy Vitamin E)
        add_meal(d+6, random.randint(7,9), "Oatmeal with Almonds & Kiwi", ["Oats", "Almonds", "Kiwi"], {"Almonds": ["Vitamin E"]})
        add_meal(d+6, random.randint(12,14), "Tofu Vegetable Stir-fry with Avocado", ["Tofu", "Choy Sum", "Spinach", "Avocado"], {"Spinach": ["Vitamin E"], "Avocado": ["Vitamin E"]})
        add_meal(d+6, 16, "Pine Nuts & Apple (Snack)", ["Pine Nuts", "Apple"], {"Pine Nuts": ["Vitamin E"]})
        add_meal(d+6, 19, "Steamed Fish with Asparagus & Sunflower Seeds", ["Grass Carp", "Asparagus", "Sunflower Seeds"], {"Sunflower Seeds": ["Vitamin E"]})

    # ==========================================
    # Heavy Vitamin E Protective Week (Minimal/No flares)
    # ==========================================
    def generate_vitamin_e_week(start_day_offset):
        d = start_day_offset
        
        # Day 1 (Heavy Vitamin E)
        add_meal(d+0, random.randint(7,9), "Avocado Toast with Sunflower Seeds", ["Avocado", "Whole Wheat Bread", "Sunflower Seeds"], {"Avocado": ["Vitamin E"], "Sunflower Seeds": ["Vitamin E"]})
        add_meal(d+0, random.randint(12,14), "Spinach & Pine Nut Stir-fry with Rice", ["Spinach", "Pine Nuts", "Rice"], {"Spinach": ["Vitamin E"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+0, 16, "Almonds + Kiwi (Snack)", ["Almonds", "Kiwi"], {"Almonds": ["Vitamin E"]})
        add_meal(d+0, 19, "Grilled Salmon with Swiss Chard", ["Salmon", "Swiss Chard"], {"Swiss Chard": ["Vitamin E"]})
        
        # Day 2 (Trigger foods but Vitamin E PROTECTS → NO FLARE)
        add_meal(d+1, 8, "Satay Beef Noodles + Avocado Side", ["Beef", "Wheat Noodles", "Satay Sauce", "Avocado"], {"Beef": ["Histamine"], "Avocado": ["Vitamin E"]})
        add_meal(d+1, 13, "Baked Pork Chop Rice with Tomato + Pine Nuts", ["Pork Chop", "Tomato", "Rice", "Pine Nuts"], {"Pork Chop": ["Tyramine"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+1, 16, "Large Handful Almonds (Snack)", ["Almonds"], {"Almonds": ["Vitamin E"]})
        add_meal(d+1, 19, "Mapo Tofu with Extra Spinach & Avocado", ["Tofu", "Minced Pork", "Chili Bean Paste", "Spinach", "Avocado"], {"Minced Pork": ["Tyramine"], "Spinach": ["Vitamin E"], "Avocado": ["Vitamin E"]})
        
        # Day 3 (Safe + Very Heavy Vitamin E)
        add_meal(d+2, random.randint(7,9), "Almond Butter Overnight Oats with Sunflower Seeds", ["Oats", "Almond Butter", "Sunflower Seeds"], {"Almond Butter": ["Vitamin E"], "Sunflower Seeds": ["Vitamin E"]})
        add_meal(d+2, random.randint(12,14), "Salmon Salad with Spinach, Avocado & Pine Nuts", ["Salmon", "Spinach", "Avocado", "Pine Nuts"], {"Spinach": ["Vitamin E"], "Avocado": ["Vitamin E"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+2, 16, "Mixed Nuts (Almonds + Pine Nuts)", ["Almonds", "Pine Nuts"], {"Almonds": ["Vitamin E"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+2, 19, "Steamed Chicken with Choy Sum & Swiss Chard", ["Chicken", "Choy Sum", "Swiss Chard"], {"Swiss Chard": ["Vitamin E"]})

        # Day 4 (Trigger with strong protection)
        add_meal(d+3, 8, "Pineapple Bun with Almond Butter", ["Wheat Flour", "Butter", "Almond Butter"], {"Wheat Flour": ["Gliadin"], "Almond Butter": ["Vitamin E"]})
        add_meal(d+3, 13, "Char Siu Rice with Large Avocado Side", ["Pork", "Char Siu Sauce", "Rice", "Avocado"], {"Pork": ["Tyramine"], "Avocado": ["Vitamin E"]})
        add_meal(d+3, 16, "Sunflower Seeds & Kiwi", ["Sunflower Seeds", "Kiwi"], {"Sunflower Seeds": ["Vitamin E"]})
        add_meal(d+3, 19, "Pork Ribs with Black Bean Sauce + Extra Spinach", ["Pork Ribs", "Black Bean Sauce", "Rice", "Spinach"], {"Pork Ribs": ["Tyramine"], "Black Bean Sauce": ["Tyramine"], "Spinach": ["Vitamin E"]})

        # Day 5
        add_meal(d+4, random.randint(7,9), "Avocado & Almond Smoothie", ["Avocado", "Almond Milk", "Spinach"], {"Avocado": ["Vitamin E"], "Spinach": ["Vitamin E"]})
        add_meal(d+4, random.randint(12,14), "Fish with Asparagus & Pine Nuts", ["Grass Carp", "Asparagus", "Pine Nuts"], {"Pine Nuts": ["Vitamin E"]})
        add_meal(d+4, 16, "Handful of Almonds", ["Almonds"], {"Almonds": ["Vitamin E"]})
        add_meal(d+4, 19, "Vegetable Stir-fry with Swiss Chard & Sunflower Seeds", ["Choy Sum", "Swiss Chard", "Sunflower Seeds"], {"Swiss Chard": ["Vitamin E"], "Sunflower Seeds": ["Vitamin E"]})

        # Day 6 (Trigger attempt but protected)
        add_meal(d+5, 8, "Shrimp Dumplings with Avocado", ["Shrimp", "Wheat Wrapper", "Avocado"], {"Shrimp": ["Tropomyosin", "Histamine"], "Avocado": ["Vitamin E"]})
        add_meal(d+5, 13, "Beef Noodles + Large Spinach Portion", ["Beef", "Wheat Noodles", "Spinach"], {"Beef": ["Histamine"], "Spinach": ["Vitamin E"]})
        add_meal(d+5, 16, "Pine Nuts Snack", ["Pine Nuts"], {"Pine Nuts": ["Vitamin E"]})
        add_meal(d+5, 19, "Salmon Bowl with Avocado & Sunflower Seeds", ["Salmon", "Avocado", "Sunflower Seeds"], {"Avocado": ["Vitamin E"], "Sunflower Seeds": ["Vitamin E"]})

        # Day 7 (Safe + Vitamin E recovery)
        add_meal(d+6, random.randint(7,9), "Oatmeal with Almond Butter & Kiwi", ["Oats", "Almond Butter", "Kiwi"], {"Almond Butter": ["Vitamin E"]})
        add_meal(d+6, random.randint(12,14), "Tofu & Vegetable Medley with Pine Nuts", ["Tofu", "Spinach", "Swiss Chard", "Pine Nuts"], {"Spinach": ["Vitamin E"], "Swiss Chard": ["Vitamin E"], "Pine Nuts": ["Vitamin E"]})
        add_meal(d+6, 16, "Almonds & Apple", ["Almonds", "Apple"], {"Almonds": ["Vitamin E"]})
        add_meal(d+6, 19, "Steamed Fish with Choy Sum & Avocado", ["Grass Carp", "Choy Sum", "Avocado"], {"Avocado": ["Vitamin E"]})

    # ==========================================
    # Generate 3 weeks (most recent first)
    # ==========================================
    generate_standard_week(0)      # Week 1 - Most recent
    generate_vitamin_e_week(7)     # Week 2 - Heavy Vitamin E protection
    generate_standard_week(14)     # Week 3 - Older baseline

    # Return sorted by timestamp (newest first)
    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)

