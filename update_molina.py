import pickle
import os

# Path to the save file
file_path = r"ClientRPG/Char configs/Molina.pkl"

# Feature List columns: (Name, Current, Max, Reset, Description)
new_features = [
    ("Arcane Recovery", "1", "1", "LR", "Regain shards on Short Rest (once per Long Rest)."),
    ("Sorcery Points", "6", "6", "LR", "Convert to shards or use Metamagic."),
    ("Suppress Memory", "6", "6", "LR", "Force creature to forget limits (amount = Concentration/2)."),
    ("Stonespeaker Crystal", "10", "10", "Dawn", "Cast divination spells or gain advantage on Investigation."),
    ("Wand of Secrets", "3", "3", "Dawn", "Detect secret doors/traps."),
    ("Cube of Force", "36", "36", "Dawn", "Create barriers (Face 1-6)."),
    ("Abracadabrus", "20", "20", "Dawn", "Conjure nonmagical objects."),
    ("Amulet of Quick Casting", "10", "10", "Dawn", "Quickened spell (Cost = TSO)."),
    ("Portal Chalk", "20", "20", "-", "Orange/Blue portals (10 uses each)."),
    ("Dead Man's Hands", "5", "5", "Dawn", "Gain Advantage on Dex checks (Charges = Mobility/2)."),
    ("Winged Boots", "4", "4", "LR", "Fly for up to 4 hours (Reset: 2h per 12h unused)."),
     ("Indirect Mischief", "1", "1", "-", "Cast illusions/enchantments from seen positions."),
     ("Innate Expertise", "1", "1", "-", "Two aspect expertises."),
     ("Portent/Divination", "2", "2", "LR", "Roll d20s and store them.")
]

if os.path.exists(file_path):
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        
        # Initialize or extend
        if "features" not in data:
            data["features"] = []
            
        # Add only if not present (simple check by name)
        existing_names = {f[0] for f in data["features"]}
        count = 0
        for feat in new_features:
            if feat[0] not in existing_names:
                data["features"].append(feat)
                count += 1
        
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
            
        print(f"Successfully added {count} features to Molina.pkl")
        
    except Exception as e:
        print(f"Error updating file: {e}")
else:
    print(f"File not found: {file_path}")
