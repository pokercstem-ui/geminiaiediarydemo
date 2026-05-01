from datetime import datetime, timedelta

def get_preset_logs():
    """Generates 1 week of granular HK diet preset logs (4 meals/day + flares)."""
    now = datetime.now()
    return [
        # --- DAY 1 (Most Recent) ---
        {
            "type": "meal",
            "content": "Steamed Minced Pork with Preserved Egg and White Rice",
            "ingredients": ["Pork", "Salted Duck Egg", "White Rice"],
            "chemical_composition": {
                "Pork": ["Tyramine"],
                "Salted Duck Egg": ["Ovalbumin", "Tyramine", "Hydrogen Sulfide"]
            },
            "timestamp": (now - timedelta(hours=8)).isoformat()
        },
        {
            "type": "meal",
            "content": "Fuji Apple (Snack)",
            "ingredients": ["Apple"],
            "chemical_composition": {
                "Apple": ["Salicylic Acid", "Fructose", "Mal d 1"]
            },
            "timestamp": (now - timedelta(hours=12)).isoformat()
        },
        {
            "type": "meal",
            "content": "Vegetarian Fried Rice with Choy Sum",
            "ingredients": ["Rice", "Choy Sum", "Egg", "Vegetable Oil"],
            "chemical_composition": {
                "Choy Sum": ["Salicylic Acid", "Glucosinolates"],
                "Egg": ["Ovalbumin", "Ovomucoid"]
            },
            "timestamp": (now - timedelta(hours=15)).isoformat()
        },
        {
            "type": "meal",
            "content": "Plain Congee with Youtiao (Fried Dough)",
            "ingredients": ["Rice", "Wheat Flour", "Oil"],
            "chemical_composition": {
                "Wheat Flour": ["Gliadin", "Glutenin"]
            },
            "timestamp": (now - timedelta(hours=20)).isoformat()
        },

        # --- DAY 2 (Trigger Day) ---
        {
            "type": "flareup",
            "severity": 6,
            "symptoms": ["Redness", "Itching"],
            "affected_areas": ["Neck", "Arms"],
            "timestamp": (now - timedelta(hours=26)).isoformat()
        },
        {
            "type": "meal",
            "content": "Sichuan Hot Pot (Beef, Fish Balls, Enoki, Sa Cha Sauce)",
            "ingredients": ["Beef", "Fish Paste", "Enoki Mushroom", "Sa Cha Sauce", "Broth"],
            "chemical_composition": {
                "Beef": ["Histamine", "Tyramine"],
                "Fish Paste": ["Parvalbumin", "Histamine"],
                "Sa Cha Sauce": ["Tropomyosin", "Monosodium Glutamate", "Histamine", "Capsaicin"]
            },
            "timestamp": (now - timedelta(hours=32)).isoformat()
        },
        {
            "type": "meal",
            "content": "Bubble Tea with Tapioca Pearls (Snack)",
            "ingredients": ["Black Tea", "Milk", "Tapioca", "Sugar"],
            "chemical_composition": {
                "Black Tea": ["Tannic Acid", "Histamine"],
                "Milk": ["Casein", "Beta-lactoglobulin", "Lactose"]
            },
            "timestamp": (now - timedelta(hours=36)).isoformat()
        },
        {
            "type": "meal",
            "content": "Sushi Lunch Set (Salmon, Tuna, Soy Sauce)",
            "ingredients": ["Salmon", "Tuna", "Rice", "Soy Sauce", "Wasabi"],
            "chemical_composition": {
                "Salmon": ["Histamine", "Parvalbumin"],
                "Tuna": ["Histamine", "Parvalbumin"],
                "Soy Sauce": ["Tyramine", "Monosodium Glutamate", "Histamine", "Gliadin"]
            },
            "timestamp": (now - timedelta(hours=39)).isoformat()
        },
        {
            "type": "meal",
            "content": "Satay Beef Macaroni in Soup",
            "ingredients": ["Beef", "Macaroni", "Satay Sauce", "Broth"],
            "chemical_composition": {
                "Beef": ["Histamine"],
                "Macaroni": ["Gliadin", "Glutenin"],
                "Satay Sauce": ["Ara h 1", "Ara h 2", "Histamine", "Capsaicin"]
            },
            "timestamp": (now - timedelta(hours=44)).isoformat()
        },

        # --- DAY 3 (Safe Day) ---
        {
            "type": "meal",
            "content": "Pan-fried Salmon with Asparagus",
            "ingredients": ["Salmon", "Asparagus", "Olive Oil"],
            "chemical_composition": {
                "Salmon": ["Parvalbumin"],
                "Asparagus": ["Asparagine", "Fructans"]
            },
            "timestamp": (now - timedelta(hours=56)).isoformat()
        },
        {
            "type": "meal",
            "content": "Fresh Mango (Snack)",
            "ingredients": ["Mango"],
            "chemical_composition": {
                "Mango": ["Urushiol-related compounds", "Fructose"]
            },
            "timestamp": (now - timedelta(hours=60)).isoformat()
        },
        {
            "type": "meal",
            "content": "Steamed Chicken with Shiitake Mushrooms and Rice",
            "ingredients": ["Chicken", "Shiitake Mushroom", "White Rice", "Soy Sauce"],
            "chemical_composition": {
                "Chicken": ["Tyramine"],
                "Shiitake Mushroom": ["Lentinan", "Guanylic Acid", "Monosodium Glutamate"],
                "Soy Sauce": ["Tyramine", "Monosodium Glutamate"]
            },
            "timestamp": (now - timedelta(hours=63)).isoformat()
        },
        {
            "type": "meal",
            "content": "Boiled Eggs and Whole Wheat Toast",
            "ingredients": ["Egg", "Whole Wheat Bread"],
            "chemical_composition": {
                "Egg": ["Ovalbumin", "Ovomucoid"],
                "Whole Wheat Bread": ["Gliadin", "Glutenin", "Fructans"]
            },
            "timestamp": (now - timedelta(hours=68)).isoformat()
        },

        # --- DAY 4 (Heavy Trigger Day) ---
        {
            "type": "flareup",
            "severity": 8,
            "symptoms": ["Oozing", "Swelling", "Sleep disturbance"],
            "affected_areas": ["Face", "Eyelids", "Hands"],
            "timestamp": (now - timedelta(hours=74)).isoformat()
        },
        {
            "type": "meal",
            "content": "Baked Pork Chop Rice with Tomato Sauce",
            "ingredients": ["Pork Chop", "Tomato", "Cheese", "Rice"],
            "chemical_composition": {
                "Pork Chop": ["Tyramine"],
                "Tomato": ["Tomatine", "Solanine", "Histamine", "Salicylic Acid"],
                "Cheese": ["Casein", "Tyramine", "Histamine"]
            },
            "timestamp": (now - timedelta(hours=80)).isoformat()
        },
        {
            "type": "meal",
            "content": "Shrimp Crackers (Snack)",
            "ingredients": ["Shrimp Paste", "Tapioca Flour", "Palm Oil"],
            "chemical_composition": {
                "Shrimp Paste": ["Tropomyosin", "Arginine Kinase", "Monosodium Glutamate"]
            },
            "timestamp": (now - timedelta(hours=84)).isoformat()
        },
        {
            "type": "meal",
            "content": "Tom Yum Goong (Thai Shrimp Soup) with Rice",
            "ingredients": ["Shrimp", "Lemongrass", "Chili", "Lime", "Broth"],
            "chemical_composition": {
                "Shrimp": ["Tropomyosin", "Arginine Kinase", "Histamine"],
                "Chili": ["Capsaicin", "Salicylic Acid"],
                "Lime": ["Citric Acid", "Histamine liberators"]
            },
            "timestamp": (now - timedelta(hours=87)).isoformat()
        },
        {
            "type": "meal",
            "content": "Shrimp Wonton Noodle Soup",
            "ingredients": ["Shrimp", "Pork", "Wheat Noodles", "Broth"],
            "chemical_composition": {
                "Shrimp": ["Tropomyosin", "Arginine Kinase", "Histamine"],
                "Wheat Noodles": ["Gliadin", "Glutenin"],
                "Pork": ["Tyramine"]
            },
            "timestamp": (now - timedelta(hours=92)).isoformat()
        },

        # --- DAY 5 (Recovery Day) ---
        {
            "type": "meal",
            "content": "Stir-fried Beef with Choy Sum",
            "ingredients": ["Beef", "Choy Sum", "Garlic", "Oil"],
            "chemical_composition": {
                "Beef": ["Tyramine"],
                "Choy Sum": ["Salicylic Acid", "Glucosinolates"],
                "Garlic": ["Allicin", "Fructans"]
            },
            "timestamp": (now - timedelta(hours=104)).isoformat()
        },
        {
            "type": "meal",
            "content": "Tofu Fa (Silken Tofu) with Ginger Syrup (Snack)",
            "ingredients": ["Soybeans", "Ginger", "Sugar"],
            "chemical_composition": {
                "Soybeans": ["Phytic Acid", "Isoflavones"],
                "Ginger": ["Salicylic Acid", "Gingerol"]
            },
            "timestamp": (now - timedelta(hours=108)).isoformat()
        },
        {
            "type": "meal",
            "content": "Sliced Grass Carp Fish Congee",
            "ingredients": ["Grass Carp", "Rice", "Ginger"],
            "chemical_composition": {
                "Grass Carp": ["Parvalbumin"],
                "Ginger": ["Salicylic Acid", "Gingerol"]
            },
            "timestamp": (now - timedelta(hours=111)).isoformat()
        },
        {
            "type": "meal",
            "content": "Oatmeal with Soy Milk",
            "ingredients": ["Rolled Oats", "Soy Milk"],
            "chemical_composition": {
                "Rolled Oats": ["Avenin", "Phytic Acid"],
                "Soy Milk": ["Phytic Acid", "Isoflavones"]
            },
            "timestamp": (now - timedelta(hours=116)).isoformat()
        },

        # --- DAY 6 (Trigger Day) ---
        {
            "type": "flareup",
            "severity": 7,
            "symptoms": ["Dryness", "Cracking", "Pain"],
            "affected_areas": ["Hands", "Fingers"],
            "timestamp": (now - timedelta(hours=122)).isoformat()
        },
        {
            "type": "meal",
            "content": "Spicy Crab with Garlic and Chili (Typhoon Shelter Style)",
            "ingredients": ["Crab", "Garlic", "Chili", "Black Bean"],
            "chemical_composition": {
                "Crab": ["Tropomyosin", "Arginine Kinase"],
                "Garlic": ["Allicin", "Fructans"],
                "Chili": ["Capsaicin"],
                "Black Bean": ["Tyramine", "Putrescine"]
            },
            "timestamp": (now - timedelta(hours=128)).isoformat()
        },
        {
            "type": "meal",
            "content": "Shredded Dried Squid (Snack)",
            "ingredients": ["Squid", "Sugar", "Salt"],
            "chemical_composition": {
                "Squid": ["Tropomyosin", "Histamine", "Tyramine"]
            },
            "timestamp": (now - timedelta(hours=132)).isoformat()
        },
        {
            "type": "meal",
            "content": "Curry Beef Brisket with Rice",
            "ingredients": ["Beef Brisket", "Curry Powder", "Potato", "Rice"],
            "chemical_composition": {
                "Beef Brisket": ["Histamine", "Tyramine"],
                "Curry Powder": ["Salicylic Acid", "Curcumin", "Capsaicin"],
                "Potato": ["Solanine"]
            },
            "timestamp": (now - timedelta(hours=135)).isoformat()
        },
        {
            "type": "meal",
            "content": "Pineapple Bun with Butter (Bolo Bao) and Milk Tea",
            "ingredients": ["Wheat Flour", "Butter", "Black Tea", "Evaporated Milk"],
            "chemical_composition": {
                "Wheat Flour": ["Gliadin", "Glutenin"],
                "Butter": ["Casein", "Lactose"],
                "Black Tea": ["Tannic Acid", "Histamine"],
                "Evaporated Milk": ["Casein", "Beta-lactoglobulin"]
            },
            "timestamp": (now - timedelta(hours=140)).isoformat()
        },

        # --- DAY 7 (Oldest - Safe Day) ---
        {
            "type": "meal",
            "content": "Steamed Pork Ribs with Black Bean Sauce, Rice",
            "ingredients": ["Pork Ribs", "Black Bean Sauce", "Rice"],
            "chemical_composition": {
                "Pork Ribs": ["Tyramine"],
                "Black Bean Sauce": ["Tyramine", "Monosodium Glutamate", "Putrescine"]
            },
            "timestamp": (now - timedelta(hours=152)).isoformat()
        },
        {
            "type": "meal",
            "content": "Hong Kong Style Egg Tart (Snack)",
            "ingredients": ["Egg", "Wheat Flour", "Butter", "Sugar"],
            "chemical_composition": {
                "Egg": ["Ovalbumin", "Ovomucoid"],
                "Wheat Flour": ["Gliadin", "Glutenin"],
                "Butter": ["Casein"]
            },
            "timestamp": (now - timedelta(hours=156)).isoformat()
        },
        {
            "type": "meal",
            "content": "Hainanese Chicken Rice",
            "ingredients": ["Chicken", "Rice", "Chicken Fat", "Ginger Scallion Oil"],
            "chemical_composition": {
                "Chicken": ["Tyramine"],
                "Ginger Scallion Oil": ["Salicylic Acid", "Gingerol", "Allicin"]
            },
            "timestamp": (now - timedelta(hours=159)).isoformat()
        },
        {
            "type": "meal",
            "content": "Rice Noodle Roll (Cheong Fun) with Sweet Soy Sauce",
            "ingredients": ["Rice Flour", "Sweet Soy Sauce", "Sesame Seeds"],
            "chemical_composition": {
                "Sweet Soy Sauce": ["Tyramine", "Histamine", "Monosodium Glutamate", "Gliadin"],
                "Sesame Seeds": ["Ses i 1", "Phytic Acid"]
            },
            "timestamp": (now - timedelta(hours=164)).isoformat()
        }
    ]
