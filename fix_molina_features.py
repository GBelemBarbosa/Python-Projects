import pickle
import os

file_path = r"ClientRPG/Char configs/Molina.pkl"

# Items to REMOVE (From "Want" list)
removals = [
    "Wand of Secrets",
    "Cube of Force",
    "Abracadabrus",
    "Amulet of Quick Casting",
    "Portal Chalk",
    "Dead Man's Hands",
    "Winged Boots",
    "Portent/Divination" # User didn't explicitly mention this but it might be future if not level appropriate?
    # Actually Portent/Divination is usually Divination Wizard. Molina seems to be Mentalist/Sorcer.
    # Text says "Divination ... R" in spell list?
    # Let's verify Portent.
    # Text says "Future: ... Feats: Prodigy ... Observant ... Class features: Wizard: ... Indirect mischief ... Voodoo Doll ... Illusory reality ... The Old Ways ... Shroud of oblivion"
    # Portent isn't explicitly in the "Future" list but "Divination" is in the spell list as a ritual.
    # "Portent/Divination" was added by me in step 874 as "Roll d20s and store them".
    # I don't see "Portent" feature in the text! I see "Divination" spell.
    # Text: "Divination - Casting Time: 1 action... R"
    # So "Portent" feature is likely NOT present. I'll remove it.
]

# Items/Features to ADD (Current)
additions = [
    # Feats
    ("Skilled", "-", "-", "-", "Proficiency in 3 aspects/tools/expertise."),
    ("Quick Fingered", "-", "-", "-", "Bonus action Dex checks to plant/steal, +1 Senses."),
    ("Practiced Expert", "-", "-", "-", "+1 Stat, Proficiency/Expertise."),
    
    # Items (Current)
    ("Lupine Mask", "-", "-", "-", "Advantage on hearing/smell & wolves."),
    ("Bag of Holding", "-", "-", "-", "500 lbs capacity, 64 cubic ft."),
    
    # Subclass / Class Features
    ("Telepathic Channel", "-", "-", "-", "communicate telepathically (30ft / 120ft)."),
    ("Obscurus Arcana", "-", "-", "-", "Invisible Mage Hand, committed memory, Befuddle mind."),
    ("Mimic Trait", "1", "1", "SR", "Action: Mimic sense, speed, prof, or accent."), # "until you use this feature again" - implies resource? Just says "Action".
    ("Master Simulator", "-", "-", "-", "Halved cost for Simulacrum, up to 2 active."),
    
    # Background
    ("Rebel Kinship", "-", "-", "-", "Network of dissidents, safe passage."),
    
    # Check existing but maybe refine
    ("Innate Expertise", "-", "-", "-", "Two aspect expertises.")
]

if os.path.exists(file_path):
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        
        if "features" in data:
            # 1. Remove incorrect items
            original_len = len(data["features"])
            data["features"] = [f for f in data["features"] if f[0] not in removals]
            removed_count = original_len - len(data["features"])
            
            # 2. Add missing items
            existing_names = {f[0] for f in data["features"]}
            added_count = 0
            for feat in additions:
                if feat[0] not in existing_names:
                    data["features"].append(feat)
                    added_count += 1
            
            with open(file_path, "wb") as f:
                pickle.dump(data, f)
                
            print(f"Removed {removed_count} 'Want' items.")
            print(f"Added {added_count} missing features/feats.")
            
    except Exception as e:
        print(f"Error correcting file: {e}")
else:
    print(f"File not found: {file_path}")
