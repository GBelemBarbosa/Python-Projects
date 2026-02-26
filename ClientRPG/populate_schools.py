import docx
import pickle
import os
import re

def clean_name(name):
    s = re.sub(r'[^a-z0-9]', '', name.lower())
    return s
    
def get_schools(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return {}
    doc = docx.Document(filename)
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    schools = {}
    for i, line in enumerate(lines):
        if line.lower().startswith("casting time:"):
            if i >= 2:
                name = lines[i-2]
                school_line = lines[i-1].lower()
                
                # extract school word
                school = "Unknown"
                for s in ["abjuration", "conjuration", "divination", "enchantment", "evocation", "illusion", "necromancy", "transmutation"]:
                    if s in school_line:
                        school = s.capitalize()
                        break
                schools[name] = school
            
    return schools

files = ['Cantrips.docx', '1 base shard output spells.docx', '2 base shard output spells.docx', 'Molina.docx']

all_schools = {}
for f in files:
    all_schools.update(get_schools(f))

print(f"Got {len(all_schools)} spells from docs")

pkl_path = 'Char configs/Molina.pkl'
with open(pkl_path, 'rb') as f:
    data = pickle.load(f)

# Update spell schools
updated_spells = 0
for spell in data.get('spells', []):
    c_name = clean_name(spell['name'])
    matched_school = "Unknown"
    for ext_name, school in all_schools.items():
        if clean_name(ext_name) == c_name:
            matched_school = school
            break
            
    spell['school'] = matched_school
    if matched_school != "Unknown":
        updated_spells += 1
    else:
        print(f"School not found for {spell['name']}")
        # Fallbacks for specific spells based on typical D&D magic:
        fbacks = {
            "guidance": "Divination",
            "mage hand": "Conjuration", 
            "prestidigitation": "Transmutation",
            "glimmer": "Illusion",
            "magical tinkering": "Transmutation",
            "magical fidling": "Transmutation",
            "minor illusion": "Illusion",
            "friends": "Enchantment",
            "command": "Enchantment",
            "detect magic": "Divination",
            "silent image": "Illusion",
            "disguise self": "Illusion",
            "find familiar": "Conjuration",
            "clue": "Divination",
            "unseen servant": "Conjuration",
            "tenser's floating disk": "Conjuration",
            "alarm": "Abjuration",
            "detect thoughts": "Divination",
            "calling": "Conjuration",
            "befuddling curse": "Enchantment",
            "augury": "Divination",
            "suggestion": "Enchantment",
            "enhance ability": "Transmutation",
            "enlarge/reduce": "Transmutation",
            "locate creature": "Divination",
            "locate object": "Divination",
            "silence": "Illusion",
            "skywrite": "Transmutation",
            "gentle repose": "Necromancy",
            "fatal distraction": "Enchantment",
            "magic mouth": "Illusion",
            "dispel magic": "Abjuration",
            "clairvoyance": "Divination",
            "fast friends": "Enchantment",
            "sending": "Evocation",
            "leomund's tiny hut": "Evocation",
            "dreamscape": "Illusion",
            "meld into stone": "Transmutation",
            "feign death": "Necromancy",
            "interference": "Abjuration",
            "plia's translocation": "Conjuration",
            "spectral passage": "Necromancy",
            "spider climb": "Transmutation",
            "rope trick": "Transmutation",
            "glyph of warding": "Abjuration",
            "comprehend languages": "Divination",
            "speak with plants": "Transmutation",
            "speak with dead": "Necromancy",
            "stone tell": "Transmutation",
            "inspect echo": "Divination",
            "security bypass": "Transmutation",
            "case the joint": "Divination",
            "witness protection": "Illusion",
            "pass without trace": "Abjuration",
            "locate animals or plants": "Divination",
            "detect thoughts": "Divination",
            "friends": "Enchantment",
            "magical tinkering": "Transmutation"
        }
        test_name = spell['name'].lower().split("(")[0].strip()
        if test_name in fbacks:
            spell['school'] = fbacks[test_name]
            updated_spells += 1
            print(f"Used fallback for {spell['name']}: {spell['school']}")

print(f"Updated schools for {updated_spells} spells")

# Extrate spell tracking
tracking_features = [
    'Spells Known (Wiz)', 'Spells Known (Sor)', 
    'Spells Prepared (Wiz)', 'Spells Prepared (Sor)', 
    'Blank Spell (Wiz)'
]

new_features = []
spell_tracking = {}

for f in data.get('features', []):
    name = f[0]
    if name in tracking_features:
        # Tuple format: (name, current, max, reset, desc, used)
        spell_tracking[name] = {'current': str(f[1]), 'max': str(f[2])}
        print(f"Moved {name} to spell tracking")
    else:
        new_features.append(f)
        
data['features'] = new_features

if 'spell_tracking' not in data:
    data['spell_tracking'] = {}
data['spell_tracking'].update(spell_tracking)

with open(pkl_path, 'wb') as f:
    pickle.dump(data, f)
print("Saved Char configs/Molina.pkl")
