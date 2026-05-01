from datetime import datetime, timedelta

def get_preset_logs():
    """Generates realistic HK diet preset logs with dynamic timestamps."""
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
                "Shrimp": ["Shellfish", "Histamine"],
                "Wheat Noodles": ["Gluten"],
                "Oyster Sauce": ["Shellfish", "Histamine", "Amines"],
                "Pork": ["Amines"]
            },
            "timestamp": (now - timedelta(days=1, hours=14)).isoformat()
        },
        {
            "type": "meal",
            "content": "Macaroni in Soup with Spam, Fried Egg, and Hot Milk Tea",
            "ingredients": ["Macaroni", "Spam", "Egg", "Black Tea", "Evaporated Milk", "Chicken Broth"],
            "chemical_composition": {
                "Macaroni": ["Gluten"],
                "Spam": ["Histamine", "Nitrates", "Amines"],
                "Evaporated Milk": ["Lactose", "Dairy"]
            },
            "timestamp": (now - timedelta(days=2, hours=4)).isoformat()
        },
        {
            "type": "meal",
            "content": "Plain Century Egg and Lean Pork Congee",
            "ingredients": ["Rice", "Century Egg", "Pork"],
            "chemical_composition": {
                "Century Egg": ["Histamine", "Amines"],
                "Pork": ["Amines"]
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
                "Shrimp": ["Shellfish", "Histamine"],
                "Wheat Wrapper": ["Gluten"],
                "Pork": ["Amines"],
                "Pu'er Tea": ["Histamine", "Tannins"]
            },
            "timestamp": (now - timedelta(days=4, hours=1)).isoformat()
        },
        {
            "type": "meal",
            "content": "Steamed Grass Carp with Ginger and Soy Sauce, White Rice",
            "ingredients": ["Grass Carp", "Ginger", "Soy Sauce", "White Rice"],
            "chemical_composition": {
                "Soy Sauce": ["Histamine", "Gluten", "Amines"],
                "Ginger": ["Salicylates"]
            },
            "timestamp": (now - timedelta(days=4, hours=8)).isoformat()
        },
        {
            "type": "meal",
            "content": "Char Siu (BBQ Pork) Rice with Fried Egg",
            "ingredients": ["Pork", "Char Siu Sauce", "Egg", "White Rice"],
            "chemical_composition": {
                "Pork": ["Amines"],
                "Char Siu Sauce": ["Histamine", "Salicylates", "Amines"]
            },
            "timestamp": (now - timedelta(days=5, hours=6)).isoformat()
        },
        {
            "type": "meal",
            "content": "Steamed Chicken with Sand Ginger, Choy Sum, and Rice",
            "ingredients": ["Chicken", "Sand Ginger", "Choy Sum", "White Rice"],
            "chemical_composition": {
                "Chicken": ["Amines"],
                "Sand Ginger": ["Salicylates"],
                "Choy Sum": ["Salicylates"]
            },
            "timestamp": (now - timedelta(days=6, hours=7)).isoformat()
        }
    ]
