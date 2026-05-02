from datetime import datetime, timedelta
import random

def get_preset_logs():
    """Generates 3 full weeks of granular HK diet logs with rich chemical profiles (2-4 chemicals per ingredient)"""
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
    # Standard Week
    # ==========================================
    def generate_standard_week(start_day_offset):
        d = start_day_offset
        
        # Day 1
        add_meal(d+0, random.randint(6,8), "Plain Century Egg Congee + Avocado", 
                ["Rice", "Century Egg", "Pork", "Avocado"], 
                {
                    "Rice": ["Arsenic", "Phytic Acid"],
                    "Century Egg": ["Tyramine", "Hydrogen Sulfide", "Lead"],
                    "Pork": ["Tyramine", "Histamine", "Purines"],
                    "Avocado": ["Vitamin E", "Oleic Acid", "Salicylic Acid"]
                })

        add_meal(d+0, random.randint(12,13), "Sliced Fish Rice Noodle Soup + Spinach", 
                ["Grass Carp", "Rice Noodles", "Ginger", "Spinach"], 
                {
                    "Grass Carp": ["Parvalbumin", "Histamine"],
                    "Rice Noodles": ["Gliadin", "Arsenic"],
                    "Ginger": ["Salicylic Acid", "Gingerol"],
                    "Spinach": ["Vitamin E", "Oxalates", "Histamine"]
                })

        add_meal(d+0, random.randint(14,18), "Almonds & Fuji Apple (Snack)", 
                ["Apple", "Almonds"], 
                {
                    "Apple": ["Salicylic Acid", "Fructose", "Polyphenols"],
                    "Almonds": ["Vitamin E", "Oxalates", "Amygdalin"]
                })

        add_meal(d+0, 19, "Steamed Chicken with Choy Sum + Pine Nuts", 
                ["Chicken", "Choy Sum", "White Rice", "Pine Nuts"], 
                {
                    "Chicken": ["Tyramine", "Histamine", "Purines"],
                    "Choy Sum": ["Salicylic Acid", "Oxalates"],
                    "White Rice": ["Arsenic", "Phytic Acid"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]
                })

        # Day 2
        add_meal(d+1, 8, "Macaroni in Soup with Spam", ["Macaroni", "Spam", "Broth"], 
                {
                    "Macaroni": ["Gliadin", "FODMAPs"],
                    "Spam": ["Sodium Nitrite", "Tyramine", "Histamine"],
                    "Broth": ["Histamine", "Glutamate"]
                })

        add_meal(d+1, 13, "Dim Sum: Har Gow & Siu Mai", ["Shrimp", "Pork", "Wheat Wrapper"], 
                {
                    "Shrimp": ["Tropomyosin", "Histamine", "Putrescine"],
                    "Pork": ["Tyramine", "Histamine"],
                    "Wheat Wrapper": ["Gliadin", "Glutenin"]
                })

        add_meal(d+1, 16, "Hot Milk Tea (Snack)", ["Black Tea", "Evaporated Milk"], 
                {
                    "Black Tea": ["Tannic Acid", "Caffeine", "Theobromine"],
                    "Evaporated Milk": ["Lactose", "Casein", "Beta-lactoglobulin"]
                })

        add_meal(d+1, 19, "Shrimp Wonton Noodle Soup", ["Shrimp", "Pork", "Wheat Noodles"], 
                {
                    "Shrimp": ["Tropomyosin", "Histamine", "Putrescine"],
                    "Pork": ["Tyramine", "Histamine"],
                    "Wheat Noodles": ["Gliadin", "FODMAPs"]
                })
        add_flare(d+1, 22, 7, ["Itching", "Redness", "Swelling"], ["Face", "Neck", "Arms"])

        # Day 3
        add_meal(d+2, 8, "Oatmeal with Almond Butter", ["Rolled Oats", "Almond Butter"], 
                {
                    "Rolled Oats": ["Avenin", "Phytic Acid"],
                    "Almond Butter": ["Vitamin E", "Oxalates", "Amygdalin"]
                })

        add_meal(d+2, 13, "Vegetarian Fried Rice + Swiss Chard", ["Rice", "Choy Sum", "Egg", "Swiss Chard"], 
                {
                    "Rice": ["Arsenic", "Phytic Acid"],
                    "Choy Sum": ["Salicylic Acid", "Oxalates"],
                    "Egg": ["Ovalbumin", "Lysozyme"],
                    "Swiss Chard": ["Vitamin E", "Oxalates"]
                })

        add_meal(d+2, 16, "Handful of Sunflower Seeds (Snack)", ["Sunflower Seeds"], 
                {"Sunflower Seeds": ["Vitamin E", "Omega-6", "Phytic Acid"]})

        add_meal(d+2, 19, "Pan-fried Salmon with Asparagus & Avocado", ["Salmon", "Asparagus", "Avocado"], 
                {
                    "Salmon": ["Parvalbumin", "Omega-3", "Histamine"],
                    "Asparagus": ["Fructans", "Asparagine"],
                    "Avocado": ["Vitamin E", "Oleic Acid"]
                })

        # Day 4
        add_meal(d+3, 8, "Pineapple Bun & Milk Tea + Few Almonds", ["Wheat Flour", "Butter", "Black Tea", "Milk", "Almonds"], 
                {
                    "Wheat Flour": ["Gliadin", "Glutenin"],
                    "Butter": ["Casein", "Lactose"],
                    "Black Tea": ["Tannic Acid", "Caffeine"],
                    "Milk": ["Lactose", "Casein"],
                    "Almonds": ["Vitamin E", "Oxalates"]
                })

        add_meal(d+3, 13, "Char Siu Rice + Small Avocado", ["Pork", "Char Siu Sauce", "Egg", "Rice", "Avocado"], 
                {
                    "Pork": ["Tyramine", "Histamine", "Purines"],
                    "Char Siu Sauce": ["Sodium Nitrite", "Monosodium Glutamate"],
                    "Egg": ["Ovalbumin", "Lysozyme"],
                    "Rice": ["Arsenic", "Phytic Acid"],
                    "Avocado": ["Vitamin E", "Oleic Acid"]
                })

        add_meal(d+3, 16, "Shredded Dried Squid (Snack)", ["Squid"], 
                {"Squid": ["Histamine", "Tyramine", "Putrescine", "Cadaverine"]})

        add_meal(d+3, 19, "Pork Ribs with Black Bean Sauce", ["Pork Ribs", "Black Bean Sauce", "Rice"], 
                {
                    "Pork Ribs": ["Tyramine", "Histamine", "Purines"],
                    "Black Bean Sauce": ["Tyramine", "Putrescine", "Sodium Benzoate"],
                    "Rice": ["Arsenic", "Phytic Acid"]
                })
        add_flare(d+3, 23, 6, ["Itching", "Dryness"], ["Arms", "Elbows"])

        # Day 5
        add_meal(d+4, random.randint(7,9), "Avocado Smoothie Bowl with Sunflower Seeds", 
                ["Avocado", "Banana", "Sunflower Seeds", "Oats"], 
                {
                    "Avocado": ["Vitamin E", "Oleic Acid"],
                    "Banana": ["Fructose", "Tyramine"],
                    "Sunflower Seeds": ["Vitamin E", "Omega-6"],
                    "Oats": ["Avenin", "Phytic Acid"]
                })

        add_meal(d+4, random.randint(12,14), "Grilled Fish with Spinach Salad", 
                ["Grass Carp", "Spinach", "Pine Nuts"], 
                {
                    "Grass Carp": ["Parvalbumin", "Histamine"],
                    "Spinach": ["Vitamin E", "Oxalates"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]
                })

        add_meal(d+4, 16, "Almonds & Pear (Snack)", ["Almonds", "Pear"], 
                {"Almonds": ["Vitamin E", "Oxalates"], "Pear": ["Fructose", "Salicylic Acid"]})

        add_meal(d+4, 19, "Chicken Stir-fry with Choy Sum & Avocado", 
                ["Chicken", "Choy Sum", "Avocado", "Rice"], 
                {
                    "Chicken": ["Tyramine", "Histamine"],
                    "Choy Sum": ["Salicylic Acid", "Oxalates"],
                    "Avocado": ["Vitamin E", "Oleic Acid"],
                    "Rice": ["Arsenic", "Phytic Acid"]
                })

        # Day 6
        add_meal(d+5, 8, "Cheese Toast with Almond Butter", ["Bread", "Cheese", "Almond Butter"], 
                {
                    "Bread": ["Gliadin", "Glutenin"],
                    "Cheese": ["Casein", "Tyramine"],
                    "Almond Butter": ["Vitamin E", "Oxalates"]
                })

        add_meal(d+5, 13, "Beef Fried Rice with Extra Spinach", ["Beef", "Rice", "Spinach", "Pine Nuts"], 
                {
                    "Beef": ["Histamine", "Purines"],
                    "Rice": ["Arsenic", "Phytic Acid"],
                    "Spinach": ["Vitamin E", "Oxalates"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]
                })

        add_meal(d+5, 16, "Large Handful Sunflower Seeds", ["Sunflower Seeds"], 
                {"Sunflower Seeds": ["Vitamin E", "Omega-6", "Phytic Acid"]})

        add_meal(d+5, 19, "Salmon with Swiss Chard & Pine Nuts", ["Salmon", "Swiss Chard", "Pine Nuts"], 
                {
                    "Salmon": ["Parvalbumin", "Omega-3"],
                    "Swiss Chard": ["Vitamin E", "Oxalates"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]
                })

        # Day 7
        add_meal(d+6, random.randint(7,9), "Oatmeal with Almonds & Kiwi", ["Oats", "Almonds", "Kiwi"], 
                {
                    "Oats": ["Avenin", "Phytic Acid"],
                    "Almonds": ["Vitamin E", "Oxalates"],
                    "Kiwi": ["Fructose", "Salicylic Acid"]
                })

        add_meal(d+6, random.randint(12,14), "Tofu Vegetable Stir-fry with Avocado", ["Tofu", "Choy Sum", "Spinach", "Avocado"], 
                {
                    "Tofu": ["Isoflavones", "Histamine"],
                    "Choy Sum": ["Salicylic Acid", "Oxalates"],
                    "Spinach": ["Vitamin E", "Oxalates"],
                    "Avocado": ["Vitamin E", "Oleic Acid"]
                })

        add_meal(d+6, 16, "Pine Nuts & Apple (Snack)", ["Pine Nuts", "Apple"], 
                {"Pine Nuts": ["Vitamin E", "Pinolenic Acid"], "Apple": ["Salicylic Acid", "Fructose"]})

        add_meal(d+6, 19, "Steamed Fish with Asparagus & Sunflower Seeds", ["Grass Carp", "Asparagus", "Sunflower Seeds"], 
                {
                    "Grass Carp": ["Parvalbumin", "Histamine"],
                    "Asparagus": ["Fructans", "Asparagine"],
                    "Sunflower Seeds": ["Vitamin E", "Omega-6"]
                })

    # ==========================================
    # Heavy Vitamin E Protective Week
    # ==========================================
    def generate_vitamin_e_week(start_day_offset):
        d = start_day_offset
        
        # Day 1
        add_meal(d+0, random.randint(7,9), "Avocado Toast with Sunflower Seeds", ["Avocado", "Whole Wheat Bread", "Sunflower Seeds"], 
                {
                    "Avocado": ["Vitamin E", "Oleic Acid", "Salicylic Acid"],
                    "Whole Wheat Bread": ["Gliadin", "Phytic Acid"],
                    "Sunflower Seeds": ["Vitamin E", "Omega-6", "Phytic Acid"]
                })

        add_meal(d+0, random.randint(12,14), "Spinach & Pine Nut Stir-fry with Rice", ["Spinach", "Pine Nuts", "Rice"], 
                {
                    "Spinach": ["Vitamin E", "Oxalates"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"],
                    "Rice": ["Arsenic", "Phytic Acid"]
                })

        add_meal(d+0, 16, "Almonds + Kiwi (Snack)", ["Almonds", "Kiwi"], 
                {"Almonds": ["Vitamin E", "Oxalates"], "Kiwi": ["Fructose", "Salicylic Acid"]})

        add_meal(d+0, 19, "Grilled Salmon with Swiss Chard", ["Salmon", "Swiss Chard"], 
                {
                    "Salmon": ["Parvalbumin", "Omega-3"],
                    "Swiss Chard": ["Vitamin E", "Oxalates"]
                })

        # Day 2
        add_meal(d+1, 8, "Satay Beef Noodles + Avocado Side", ["Beef", "Wheat Noodles", "Satay Sauce", "Avocado"], 
                {
                    "Beef": ["Histamine", "Purines"],
                    "Wheat Noodles": ["Gliadin", "FODMAPs"],
                    "Satay Sauce": ["Tyramine", "Monosodium Glutamate"],
                    "Avocado": ["Vitamin E", "Oleic Acid"]
                })

        add_meal(d+1, 13, "Baked Pork Chop Rice with Tomato + Pine Nuts", ["Pork Chop", "Tomato", "Rice", "Pine Nuts"], 
                {
                    "Pork Chop": ["Tyramine", "Histamine"],
                    "Tomato": ["Solanine", "Tomatine", "Histamine"],
                    "Rice": ["Arsenic", "Phytic Acid"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]
                })

        add_meal(d+1, 16, "Large Handful Almonds (Snack)", ["Almonds"], 
                {"Almonds": ["Vitamin E", "Oxalates", "Amygdalin"]})

        add_meal(d+1, 19, "Mapo Tofu with Extra Spinach & Avocado", ["Tofu", "Minced Pork", "Chili Bean Paste", "Spinach", "Avocado"], 
                {
                    "Tofu": ["Isoflavones", "Histamine"],
                    "Minced Pork": ["Tyramine", "Histamine"],
                    "Chili Bean Paste": ["Capsaicin", "Tyramine"],
                    "Spinach": ["Vitamin E", "Oxalates"],
                    "Avocado": ["Vitamin E", "Oleic Acid"]
                })

        # Day 3
        add_meal(d+2, random.randint(7,9), "Almond Butter Overnight Oats with Sunflower Seeds", ["Oats", "Almond Butter", "Sunflower Seeds"], 
                {
                    "Oats": ["Avenin", "Phytic Acid"],
                    "Almond Butter": ["Vitamin E", "Oxalates"],
                    "Sunflower Seeds": ["Vitamin E", "Omega-6"]
                })

        add_meal(d+2, random.randint(12,14), "Salmon Salad with Spinach, Avocado & Pine Nuts", ["Salmon", "Spinach", "Avocado", "Pine Nuts"], 
                {
                    "Salmon": ["Parvalbumin", "Omega-3"],
                    "Spinach": ["Vitamin E", "Oxalates"],
                    "Avocado": ["Vitamin E", "Oleic Acid"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]
                })

        add_meal(d+2, 16, "Mixed Nuts (Almonds + Pine Nuts)", ["Almonds", "Pine Nuts"], 
                {"Almonds": ["Vitamin E", "Oxalates"], "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]})

        add_meal(d+2, 19, "Steamed Chicken with Choy Sum & Swiss Chard", ["Chicken", "Choy Sum", "Swiss Chard"], 
                {
                    "Chicken": ["Tyramine", "Histamine"],
                    "Choy Sum": ["Salicylic Acid", "Oxalates"],
                    "Swiss Chard": ["Vitamin E", "Oxalates"]
                })

        # Day 4
        add_meal(d+3, 8, "Pineapple Bun with Almond Butter", ["Wheat Flour", "Butter", "Almond Butter"], 
                {
                    "Wheat Flour": ["Gliadin", "Glutenin"],
                    "Butter": ["Casein", "Lactose"],
                    "Almond Butter": ["Vitamin E", "Oxalates"]
                })

        add_meal(d+3, 13, "Char Siu Rice with Large Avocado Side", ["Pork", "Char Siu Sauce", "Rice", "Avocado"], 
                {
                    "Pork": ["Tyramine", "Histamine"],
                    "Char Siu Sauce": ["Sodium Nitrite", "Monosodium Glutamate"],
                    "Rice": ["Arsenic", "Phytic Acid"],
                    "Avocado": ["Vitamin E", "Oleic Acid"]
                })

        add_meal(d+3, 16, "Sunflower Seeds & Kiwi", ["Sunflower Seeds", "Kiwi"], 
                {"Sunflower Seeds": ["Vitamin E", "Omega-6"], "Kiwi": ["Fructose", "Salicylic Acid"]})

        add_meal(d+3, 19, "Pork Ribs with Black Bean Sauce + Extra Spinach", ["Pork Ribs", "Black Bean Sauce", "Rice", "Spinach"], 
                {
                    "Pork Ribs": ["Tyramine", "Histamine"],
                    "Black Bean Sauce": ["Tyramine", "Putrescine"],
                    "Rice": ["Arsenic", "Phytic Acid"],
                    "Spinach": ["Vitamin E", "Oxalates"]
                })

        # Day 5
        add_meal(d+4, random.randint(7,9), "Avocado & Almond Smoothie", ["Avocado", "Almond Milk", "Spinach"], 
                {
                    "Avocado": ["Vitamin E", "Oleic Acid"],
                    "Almond Milk": ["Vitamin E", "Oxalates"],
                    "Spinach": ["Vitamin E", "Oxalates"]
                })

        add_meal(d+4, random.randint(12,14), "Fish with Asparagus & Pine Nuts", ["Grass Carp", "Asparagus", "Pine Nuts"], 
                {
                    "Grass Carp": ["Parvalbumin", "Histamine"],
                    "Asparagus": ["Fructans", "Asparagine"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]
                })

        add_meal(d+4, 16, "Handful of Almonds", ["Almonds"], 
                {"Almonds": ["Vitamin E", "Oxalates"]})

        add_meal(d+4, 19, "Vegetable Stir-fry with Swiss Chard & Sunflower Seeds", ["Choy Sum", "Swiss Chard", "Sunflower Seeds"], 
                {
                    "Choy Sum": ["Salicylic Acid", "Oxalates"],
                    "Swiss Chard": ["Vitamin E", "Oxalates"],
                    "Sunflower Seeds": ["Vitamin E", "Omega-6"]
                })

        # Day 6
        add_meal(d+5, 8, "Shrimp Dumplings with Avocado", ["Shrimp", "Wheat Wrapper", "Avocado"], 
                {
                    "Shrimp": ["Tropomyosin", "Histamine"],
                    "Wheat Wrapper": ["Gliadin", "Glutenin"],
                    "Avocado": ["Vitamin E", "Oleic Acid"]
                })

        add_meal(d+5, 13, "Beef Noodles + Large Spinach Portion", ["Beef", "Wheat Noodles", "Spinach"], 
                {
                    "Beef": ["Histamine", "Purines"],
                    "Wheat Noodles": ["Gliadin", "FODMAPs"],
                    "Spinach": ["Vitamin E", "Oxalates"]
                })

        add_meal(d+5, 16, "Pine Nuts Snack", ["Pine Nuts"], 
                {"Pine Nuts": ["Vitamin E", "Pinolenic Acid"]})

        add_meal(d+5, 19, "Salmon Bowl with Avocado & Sunflower Seeds", ["Salmon", "Avocado", "Sunflower Seeds"], 
                {
                    "Salmon": ["Parvalbumin", "Omega-3"],
                    "Avocado": ["Vitamin E", "Oleic Acid"],
                    "Sunflower Seeds": ["Vitamin E", "Omega-6"]
                })

        # Day 7
        add_meal(d+6, random.randint(7,9), "Oatmeal with Almond Butter & Kiwi", ["Oats", "Almond Butter", "Kiwi"], 
                {
                    "Oats": ["Avenin", "Phytic Acid"],
                    "Almond Butter": ["Vitamin E", "Oxalates"],
                    "Kiwi": ["Fructose", "Salicylic Acid"]
                })

        add_meal(d+6, random.randint(12,14), "Tofu & Vegetable Medley with Pine Nuts", ["Tofu", "Spinach", "Swiss Chard", "Pine Nuts"], 
                {
                    "Tofu": ["Isoflavones", "Histamine"],
                    "Spinach": ["Vitamin E", "Oxalates"],
                    "Swiss Chard": ["Vitamin E", "Oxalates"],
                    "Pine Nuts": ["Vitamin E", "Pinolenic Acid"]
                })

        add_meal(d+6, 16, "Almonds & Apple", ["Almonds", "Apple"], 
                {"Almonds": ["Vitamin E", "Oxalates"], "Apple": ["Salicylic Acid", "Fructose"]})

        add_meal(d+6, 19, "Steamed Fish with Choy Sum & Avocado", ["Grass Carp", "Choy Sum", "Avocado"], 
                {
                    "Grass Carp": ["Parvalbumin", "Histamine"],
                    "Choy Sum": ["Salicylic Acid", "Oxalates"],
                    "Avocado": ["Vitamin E", "Oleic Acid"]
                })

    # ==========================================
    # Generate 3 weeks (most recent first)
    # ==========================================
    generate_standard_week(0)   # Week 1 - Most recent
    generate_vitamin_e_week(7)  # Week 2 - Heavy Vitamin E protection
    generate_standard_week(14)  # Week 3 - Older baseline

    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)
