from datetime import datetime, timedelta
import random

def get_preset_logs():
    """Generates 3 full weeks of granular HK diet logs with a unique Week 2."""
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
    # WEEK 1 & 3: The Standard Baseline Pattern
    # ==========================================
    def generate_standard_week(start_day_offset):
        d = start_day_offset
        # Day 1 (Safe)
        add_meal(d+0, random.randint(6,8), "Plain Century Egg Congee", ["Rice", "Century Egg", "Pork"], {"Century Egg": ["Tyramine", "Hydrogen Sulfide"], "Pork": ["Tyramine"]})
        add_meal(d+0, random.randint(12,13), "Sliced Fish Rice Noodle Soup", ["Grass Carp", "Rice Noodles", "Ginger"], {"Grass Carp": ["Parvalbumin"], "Ginger": ["Salicylic Acid", "Gingerol"]})
        add_meal(d+0, random.randint(14,18), "Fuji Apple (Snack)", ["Apple"], {"Apple": ["Salicylic Acid", "Fructose"]})
        add_meal(d+0, 19, "Steamed Chicken with Choy Sum", ["Chicken", "Choy Sum", "White Rice"], {"Chicken": ["Tyramine"], "Choy Sum": ["Salicylic Acid"]})
        
        # Day 2 (Trigger: Shellfish)
        add_meal(d+1, 8, "Macaroni in Soup with Spam", ["Macaroni", "Spam", "Broth"], {"Macaroni": ["Gliadin", "Glutenin"], "Spam": ["Sodium Nitrite", "Tyramine"]})
        add_meal(d+1, 13, "Dim Sum: Har Gow & Siu Mai", ["Shrimp", "Pork", "Wheat Wrapper"], {"Shrimp": ["Tropomyosin", "Arginine Kinase", "Histamine"], "Wheat Wrapper": ["Gliadin"]})
        add_meal(d+1, 16, "Hot Milk Tea (Snack)", ["Black Tea", "Evaporated Milk"], {"Black Tea": ["Tannic Acid"], "Evaporated Milk": ["Casein", "Lactose"]})
        add_meal(d+1, 19, "Shrimp Wonton Noodle Soup", ["Shrimp", "Pork", "Wheat Noodles", "Broth"], {"Shrimp": ["Tropomyosin", "Arginine Kinase", "Histamine"], "Wheat Noodles": ["Gliadin"]})
        add_flare(d+1, 22, 7, ["Itching", "Redness", "Swelling"], ["Face", "Neck", "Arms"])
        
        # Day 3 (Safe)
        add_meal(d+2, 8, "Plain Oatmeal with Soy Milk", ["Rolled Oats", "Soy Milk"], {"Rolled Oats": ["Avenin"], "Soy Milk": ["Isoflavones"]})
        add_meal(d+2, 13, "Vegetarian Fried Rice", ["Rice", "Choy Sum", "Egg"], {"Choy Sum": ["Salicylic Acid"], "Egg": ["Ovalbumin", "Ovomucoid"]})
        add_meal(d+2, 16, "Fresh Mango (Snack)", ["Mango"], {"Mango": ["Urushiol-related compounds", "Fructose"]})
        add_meal(d+2, 19, "Pan-fried Salmon with Asparagus", ["Salmon", "Asparagus"], {"Salmon": ["Parvalbumin"], "Asparagus": ["Fructans"]})
        
        # Day 4 (Trigger: Amines)
        add_meal(d+3, 8, "Pineapple Bun & Milk Tea", ["Wheat Flour", "Butter", "Black Tea", "Milk"], {"Wheat Flour": ["Gliadin"], "Butter": ["Casein"], "Black Tea": ["Tannic Acid"]})
        add_meal(d+3, 13, "Char Siu Rice with Fried Egg", ["Pork", "Char Siu Sauce", "Egg", "Rice"], {"Pork": ["Tyramine"], "Char Siu Sauce": ["Monosodium Glutamate", "Salicylic Acid", "Tartrazine"], "Egg": ["Ovalbumin"]})
        add_meal(d+3, 16, "Shredded Dried Squid (Snack)", ["Squid", "Sugar", "Salt"], {"Squid": ["Tropomyosin", "Histamine", "Tyramine"]})
        add_meal(d+3, 19, "Pork Ribs with Black Bean Sauce", ["Pork Ribs", "Black Bean Sauce", "Rice"], {"Pork Ribs": ["Tyramine"], "Black Bean Sauce": ["Tyramine", "Monosodium Glutamate", "Putrescine"]})
        add_flare(d+3, 23, 8, ["Oozing", "Sleep disturbance", "Itching"], ["Arms", "Elbows", "Back"])
        
        # Day 5 (Safe)
        add_meal(d+4, 8, "Boiled Eggs and Whole Wheat Toast", ["Egg", "Whole Wheat Bread"], {"Egg": ["Ovalbumin"], "Whole Wheat Bread": ["Gliadin", "Fructans"]})
        add_meal(d+4, 13, "Minced Pork with Preserved Egg", ["Pork", "Salted Duck Egg", "Rice"], {"Pork": ["Tyramine"], "Salted Duck Egg": ["Ovalbumin", "Tyramine"]})
        add_meal(d+4, 16, "Tofu Fa (Snack)", ["Soybeans", "Ginger"], {"Soybeans": ["Isoflavones"], "Ginger": ["Salicylic Acid", "Gingerol"]})
        add_meal(d+4, 19, "Stir-fried Beef with Broccoli", ["Beef", "Broccoli", "Garlic"], {"Beef": ["Tyramine"], "Broccoli": ["Salicylic Acid"], "Garlic": ["Fructans"]})
        
        # Day 6 (Trigger: Shellfish & Spices)
        add_meal(d+5, 8, "Rice Noodle Roll (Cheong Fun)", ["Rice Flour", "Sweet Soy Sauce"], {"Sweet Soy Sauce": ["Tyramine", "Monosodium Glutamate", "Histamine", "Gliadin"]})
        add_meal(d+5, 13, "Spicy Crab with Garlic", ["Crab", "Garlic", "Chili"], {"Crab": ["Tropomyosin", "Arginine Kinase"], "Garlic": ["Fructans"], "Chili": ["Capsaicin"]})
        add_meal(d+5, 16, "Shrimp Crackers (Snack)", ["Shrimp Paste", "Tapioca Flour"], {"Shrimp Paste": ["Tropomyosin", "Monosodium Glutamate"]})
        add_meal(d+5, 19, "Tom Yum Goong", ["Shrimp", "Chili", "Lime", "Broth"], {"Shrimp": ["Tropomyosin", "Arginine Kinase", "Histamine"], "Chili": ["Capsaicin"], "Lime": ["Citric Acid"]})
        add_flare(d+5, 23, 9, ["Cracking", "Pain", "Severe Redness", "Swelling"], ["Hands", "Fingers", "Eyelids"])
        
        # Day 7 (Recovery)
        add_meal(d+6, 8, "Plain Congee with Youtiao", ["Rice", "Wheat Flour", "Oil"], {"Wheat Flour": ["Gliadin", "Glutenin"]})
        add_meal(d+6, 13, "Hainanese Chicken Rice", ["Chicken", "Rice", "Ginger Scallion Oil"], {"Chicken": ["Tyramine"], "Ginger Scallion Oil": ["Salicylic Acid", "Gingerol", "Allicin"]})
        add_meal(d+6, 16, "Banana (Snack)", ["Banana"], {"Banana": ["Amylase", "Chitinase"]})
        add_meal(d+6, 19, "Tomato and Egg Stir-fry", ["Tomato", "Egg", "Rice"], {"Tomato": ["Tomatine", "Histamine", "Salicylic Acid"], "Egg": ["Ovalbumin"]})

    # ==========================================
    # WEEK 2: Unique Hardcoded Snippet
    # ==========================================
    def generate_unique_week_2(start_day_offset):
        d = start_day_offset
        # Day 8 (Safe)
        add_meal(d+0, 8, "Rice Vermicelli with Fish Slices", ["Rice Vermicelli", "Grass Carp", "Broth"], {"Grass Carp": ["Parvalbumin"]})
        add_meal(d+0, 13, "Steamed Pork Patty with Water Chestnut", ["Pork", "Water Chestnut", "Rice"], {"Pork": ["Tyramine"]})
        add_meal(d+0, 16, "Dragon Fruit (Snack)", ["Dragon Fruit"], {"Dragon Fruit": ["Oligosaccharides"]})
        add_meal(d+0, 19, "Winter Melon Soup with Lean Pork", ["Winter Melon", "Pork", "Broth"], {"Pork": ["Tyramine"]})
        
        # Day 9 (Trigger: Nightshades & Heavy Amines)
        add_meal(d+1, 8, "Satay Beef Noodles", ["Beef", "Wheat Noodles", "Satay Sauce"], {"Beef": ["Histamine"], "Wheat Noodles": ["Gliadin"], "Satay Sauce": ["Ara h 1", "Histamine", "Capsaicin"]})
        add_meal(d+1, 13, "Baked Pork Chop Rice with Tomato Sauce", ["Pork Chop", "Tomato", "Cheese", "Rice"], {"Pork Chop": ["Tyramine"], "Tomato": ["Tomatine", "Histamine", "Salicylic Acid"], "Cheese": ["Casein", "Tyramine"]})
        add_meal(d+1, 16, "Hong Kong Style Egg Tart (Snack)", ["Egg", "Wheat Flour", "Butter"], {"Egg": ["Ovalbumin"], "Wheat Flour": ["Gliadin"], "Butter": ["Casein"]})
        add_meal(d+1, 19, "Mapo Tofu with Rice", ["Tofu", "Minced Pork", "Chili Bean Paste", "Sichuan Peppercorn"], {"Tofu": ["Isoflavones"], "Minced Pork": ["Tyramine"], "Chili Bean Paste": ["Capsaicin", "Monosodium Glutamate", "Tyramine"], "Sichuan Peppercorn": ["Hydroxy-alpha sanshool"]})
        add_flare(d+1, 22, 6, ["Redness", "Burning"], ["Face", "Chest"])

        # Day 10 (Safe / Recovery)
        add_meal(d+2, 8, "Plain Udon in Kelp Broth", ["Udon", "Kelp", "Broth"], {"Udon": ["Gliadin"], "Kelp": ["Iodine", "Monosodium Glutamate"]})
        add_meal(d+2, 13, "Steamed Egg with Rice", ["Egg", "Rice", "Soy Sauce"], {"Egg": ["Ovalbumin"], "Soy Sauce": ["Tyramine", "Monosodium Glutamate"]})
        add_meal(d+2, 16, "Asian Pear (Snack)", ["Pear"], {"Pear": ["Fructose", "Sorbitol"]})
        add_meal(d+2, 19, "Steamed Chicken with Wood Ear Mushroom", ["Chicken", "Wood Ear Mushroom", "Rice"], {"Chicken": ["Tyramine"]})

        # Day 11 (Trigger: Heavy Shellfish & Soy)
        add_meal(d+3, 8, "Cheong Fun with Peanut Sauce", ["Rice Flour", "Peanut Butter", "Hoisin Sauce"], {"Peanut Butter": ["Ara h 1", "Ara h 2", "Aflatoxin"], "Hoisin Sauce": ["Monosodium Glutamate", "Tyramine"]})
        add_meal(d+3, 13, "Seafood Pan-fried Noodles", ["Shrimp", "Squid", "Scallop", "Wheat Noodles"], {"Shrimp": ["Tropomyosin"], "Squid": ["Tropomyosin"], "Scallop": ["Tropomyosin"], "Wheat Noodles": ["Gliadin"]})
        add_meal(d+3, 16, "Vitasoy Soy Milk (Snack)", ["Soybeans", "Sugar"], {"Soybeans": ["Isoflavones", "Phytic Acid"]})
        add_meal(d+3, 19, "Stir-fried Clams with Black Bean Sauce", ["Clams", "Black Bean Sauce", "Garlic", "Chili"], {"Clams": ["Tropomyosin", "Histamine"], "Black Bean Sauce": ["Tyramine", "Putrescine"], "Garlic": ["Fructans"], "Chili": ["Capsaicin"]})
        add_flare(d+3, 23, 8, ["Severe Itching", "Swelling", "Oozing"], ["Eyelids", "Neck", "Arms"])

        # Day 12 (Safe)
        add_meal(d+4, 8, "Congee with Lean Pork", ["Rice", "Pork"], {"Pork": ["Tyramine"]})
        add_meal(d+4, 13, "Zucchini and Pork Stir-fry", ["Zucchini", "Pork", "Rice"], {"Pork": ["Tyramine"]})
        add_meal(d+4, 16, "Papaya (Snack)", ["Papaya"], {"Papaya": ["Papain", "Chitinase"]})
        add_meal(d+4, 19, "Steamed Tofu with Minced Pork", ["Tofu", "Pork", "Rice"], {"Tofu": ["Isoflavones"], "Pork": ["Tyramine"]})

        # Day 13 (Trigger: Amines, Spices, Additives)
        add_meal(d+5, 8, "Spam and Egg Sandwich", ["Spam", "Egg", "White Bread"], {"Spam": ["Sodium Nitrite", "Tyramine"], "Egg": ["Ovalbumin"], "White Bread": ["Gliadin", "Glutenin"]})
        add_meal(d+5, 13, "Curry Beef Brisket Rice", ["Beef Brisket", "Curry Powder", "Potato", "Rice"], {"Beef Brisket": ["Histamine"], "Curry Powder": ["Capsaicin", "Salicylic Acid", "Curcumin"], "Potato": ["Solanine"]})
        add_meal(d+5, 16, "Street Food: Curry Fishballs (Snack)", ["Fish Paste", "Curry Sauce"], {"Fish Paste": ["Parvalbumin", "Monosodium Glutamate"], "Curry Sauce": ["Capsaicin", "Tartrazine"]})
        add_meal(d+5, 19, "Roast Duck with Rice", ["Duck", "Plum Sauce", "Rice"], {"Duck": ["Tyramine", "Histamine"], "Plum Sauce": ["Salicylic Acid", "Monosodium Glutamate"]})
        add_flare(d+5, 23, 7, ["Itching", "Dryness"], ["Stomach", "Legs"])

        # Day 14 (Safe)
        add_meal(d+6, 8, "Plain Rice Noodles in Broth", ["Rice Noodles", "Broth"], {})
        add_meal(d+6, 13, "Stir-fried Beef with Celery", ["Beef", "Celery", "Rice"], {"Beef": ["Tyramine"], "Celery": ["Apiin", "Mannitol"]})
        add_meal(d+6, 16, "Watermelon (Snack)", ["Watermelon"], {"Watermelon": ["Fructose", "Profilin"]})
        add_meal(d+6, 19, "Pan-fried Tofu with Soy Sauce", ["Tofu", "Soy Sauce", "Rice"], {"Tofu": ["Isoflavones"], "Soy Sauce": ["Tyramine", "Monosodium Glutamate"]})

    # ==========================================
    # Execute the Generators
    # ==========================================
    generate_standard_week(1)    # Week 1 (Days 1-7)
    generate_unique_week_2(8)    # Week 2 (Days 8-14)

    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)
