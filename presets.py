from datetime import datetime, timedelta

def get_preset_logs():
    """Generates realistic HK diet preset logs with dynamic timestamps and granular chemical profiles."""
    now = datetime.now()
    return [
        {
            "type": "flareup",
            "severity": 7,
            "symptoms": ["Itching", "Redness", "Swelling"],
            "affected_areas": ["Face", "Neck", "Arms"],
            "timestamp": (now - timedelta(days=1, hours=2)).isoformat()
        },
        {
            "type": "meal",
            "content": "Shrimp Wonton Noodle Soup and a side of Gai Lan with Oyster Sauce",
            "ingredients": ["Shrimp", "Pork", "Wheat Noodles", "Gai Lan", "Oyster Sauce", "Broth"],
            "chemical_composition": {
                "Shrimp": ["Tropomyosin", "Arginine Kinase", "Histamine"],
                "Wheat Noodles": ["Gliadin", "Glutenin", "Fructans"],
                "Oyster Sauce": ["Monosodium Glutamate", "Tropomyosin", "Tyramine", "Sodium Benzoate"],
                "Pork": ["Tyramine"]
            },
            "timestamp": (now - timedelta(days=1, hours=14)).isoformat()
        },
        {
            "type": "meal",
            "content": "Macaroni in Soup with Spam, Fried Egg, and Hot Milk Tea",
            "ingredients": ["Macaroni", "Spam", "Egg", "Black Tea", "Evaporated Milk", "Chicken Broth"],
            "chemical_composition": {
                "Macaroni": ["Gliadin", "Glutenin"],
                "Spam": ["Sodium Nitrite", "Tyramine", "Histamine"],
                "Egg": ["Ovalbumin", "Ovomucoid", "Lysozyme"],
                "Black Tea": ["Tannic Acid", "Theaflavins", "Histamine"],
                "Evaporated Milk": ["Lactose", "Casein", "Beta-lactoglobulin"]
            },
            "timestamp": (now - timedelta(days=2, hours=4)).isoformat()
        },
        {
            "type": "meal",
            "content": "Plain Century Egg and Lean Pork Congee",
            "ingredients": ["Rice", "Century Egg", "Pork"],
            "chemical_composition": {
                "Century Egg": ["Tyramine", "Putrescine", "Hydrogen Sulfide", "Ammonia"],
                "Pork": ["Tyramine"]
            },
            "timestamp": (now - timedelta(days=2, hours=12)).isoformat()
        },
        {
            "type": "flareup",
            "severity": 8,
            "symptoms": ["Itching", "Oozing", "Sleep disturbance"],
            "affected_areas": ["Face", "Elbows"],
            "timestamp": (now - timedelta(days=3, hours=5)).isoformat()
        },
        {
            "type": "meal",
            "content": "Dim Sum: Har Gow (Shrimp Dumplings), Siu Mai, and Pu'er Tea",
            "ingredients": ["Shrimp", "Pork", "Wheat Wrapper", "Pu'er Tea"],
            "chemical_composition": {
                "Shrimp": ["Tropomyosin", "Arginine Kinase", "Histamine"],
                "Wheat Wrapper": ["Gliadin", "Glutenin"],
                "Pork": ["Tyramine", "Putrescine"],
                "Pu'er Tea": ["Tannic Acid", "Histamine", "Theaflavins"]
            },
            "timestamp": (now - timedelta(days=4, hours=1)).isoformat()
        },
        {
            "type": "meal",
            "content": "Steamed Grass Carp with Ginger and Soy Sauce, White Rice",
            "ingredients": ["Grass Carp", "Ginger", "Soy Sauce", "White Rice"],
            "chemical_composition": {
                "Soy Sauce": ["Tyramine", "Monosodium Glutamate", "Histamine", "Gliadin"],
                "Ginger": ["Salicylic Acid", "Gingerol"]
            },
            "timestamp": (now - timedelta(days=4, hours=8)).isoformat()
        },
        {
            "type": "meal",
            "content": "Char Siu (BBQ Pork) Rice with Fried Egg",
            "ingredients": ["Pork", "Char Siu Sauce", "Egg", "White Rice"],
            "chemical_composition": {
                "Pork": ["Tyramine"],
                "Char Siu Sauce": ["Monosodium Glutamate", "Salicylic Acid", "Tyramine", "Tartrazine"],
                "Egg": ["Ovalbumin", "Ovomucoid"]
            },
            "timestamp": (now - timedelta(days=5, hours=6)).isoformat()
        },
        {
            "type": "meal",
            "content": "Steamed Chicken with Sand Ginger, Choy Sum, and Rice",
            "ingredients": ["Chicken", "Sand Ginger", "Choy Sum", "White Rice"],
            "chemical_composition": {
                "Chicken": ["Tyramine"],
                "Sand Ginger": ["Salicylic Acid", "Kaempferol"],
                "Choy Sum": ["Salicylic Acid", "Glucosinolates"]
            },
            "timestamp": (now - timedelta(days=6, hours=7)).isoformat()
        }
    ]
