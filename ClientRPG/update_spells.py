import docx
import pickle
import re
import os

def clean_name(name):
    s = re.sub(r'[^a-z0-9]', '', name.lower())
    return s

def extract_from_docx(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return {}
    doc = docx.Document(filename)
    
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    spells = {}
    # Case insensitive start
    casting_indices = [i for i, line in enumerate(lines) if line.lower().startswith("casting time:")]
    
    for idx, c_idx in enumerate(casting_indices):
        name_line = lines[c_idx - 2]
        
        if idx + 1 < len(casting_indices):
            end_idx = casting_indices[idx + 1] - 2
        else:
            end_idx = len(lines)
            
        desc_start = c_idx + 1
        for cur_idx in range(desc_start, end_idx):
            l_lower = lines[cur_idx].lower()
            if l_lower.startswith("range:") or l_lower.startswith("components:") or l_lower.startswith("duration:") or l_lower.startswith("classes:"):
                desc_start = cur_idx + 1
            else:
                break
                
        desc_lines = []
        for line in lines[desc_start:end_idx]:
            if line.lower().startswith("spell lists.") or line.lower().startswith("classes:"):
                continue
            desc_lines.append(line)
            
        if desc_lines:
            spells[name_line] = "\n\n".join(desc_lines)
            
    return spells

def main():
    files = [
        'Cantrips.docx',
        '1 base shard output spells.docx',
        '3 base shard output spells.docx'
    ]
    
    extracted = {}
    for f in files:
        extracted.update(extract_from_docx(f))
        
    print(f"Extracted {len(extracted)} spells from docx.")
    
    pkl_path = 'Char configs/Molina.pkl'
    # load backup to start fresh
    if os.path.exists(pkl_path + '.backup_new'):
        pass # wait, I want to use original backup just in case
        
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
        
    updated = 0
    not_matched = []
    for spell in data.get('spells', []):
        name = spell['name']
        c_name = clean_name(name)
        
        matched_desc = None
        for ext_name, desc in extracted.items():
            ext_parts = [clean_name(p) for p in ext_name.split('/')]
            ext_cleaned = clean_name(ext_name)
            
            if c_name in ext_parts or c_name == ext_cleaned or any(len(p)>4 and (p in c_name or c_name in p) for p in ext_parts):
                matched_desc = desc
                break
                
        if matched_desc:
            spell['desc'] = matched_desc
            updated += 1
        else:
            not_matched.append(name)
            
    print(f"\nTotal updated: {updated} / {len(data.get('spells', []))}")
    if not_matched:
        print("Not matched:", not_matched)
    
    if updated > 0:
        import shutil
        shutil.copyfile(pkl_path, pkl_path + '.backup_new3')
        with open(pkl_path, 'wb') as f:
            pickle.dump(data, f)
        print("Saved Molina.pkl")

if __name__ == "__main__":
    main()
