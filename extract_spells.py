import zipfile
import re
import os
import pickle
import uuid

docx_path = r"ClientRPG/Molina.docx"
pkl_path = r"ClientRPG/Char configs/Molina.pkl"

if not os.path.exists(docx_path):
    print(f"File not found: {docx_path}")
    exit()

# Colors
COLOR_WIZ_PREP = ["0070C0", "4F81BD", "0070c0", "4f81bd"] 
COLOR_SORC_PREP = ["7030A0", "5F497A", "7030a0", "5f497a"] 
COLOR_WIZ_UNPREP = ["FFC000", "E36C09", "ffc000", "e36c09"] 

full_text_spells = []

try:
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read("word/document.xml").decode("utf-8")

    # Regex to find paragraphs
    paragraphs = re.findall(r'(<w:p(?: [^>]*)?>.*?</w:p>)', xml_content, re.DOTALL)
    
    current_level = 0
    
    for p in paragraphs:
        # Extract runs to determine color
        runs = re.findall(r'(<w:r(?: [^>]*)?>.*?</w:r>)', p, re.DOTALL)
        
        para_text_parts = []
        highlight_color = None
        
        for r in runs:
            t_match = re.search(r'<w:t(?: [^>]*)?>(.*?)</w:t>', r, re.DOTALL)
            if t_match:
                text = t_match.group(1)
                para_text_parts.append(text)
                
                # Check color of this run
                c_match = re.search(r'<w:color [^>]*w:val="([^"]+)"', r)
                if c_match:
                    c = c_match.group(1)
                    if highlight_color is None and c != "Auto":
                        highlight_color = c
        
        full_line = "".join(para_text_parts).strip()
        lower_line = full_line.lower()
        
        # Headers
        if "cantrips" in lower_line and len(lower_line) < 20:
            current_level = 0
            continue
        if "level 1" in lower_line or "1st level" in lower_line:
            current_level = 1
            continue
        if "level 2" in lower_line or "2nd level" in lower_line:
            current_level = 2
            continue
        if "level 3" in lower_line or "3rd level" in lower_line:
            current_level = 3
            continue
        if "level 4" in lower_line or "4th level" in lower_line:
            current_level = 4
            continue
        if "level 5" in lower_line or "5th level" in lower_line:
            current_level = 5
            continue
            
        # Regex for keywords (wildcard separator)
        # using .*? to be very permissive
        m_time = re.search(r"casting.*?time", lower_line)
        m_range = re.search(r"range", lower_line)
        m_comp = re.search(r"components", lower_line)
        m_dur = re.search(r"duration", lower_line)
        
        idx_time = m_time.start() if m_time else -1
        idx_range = m_range.start() if m_range else -1
        idx_comp = m_comp.start() if m_comp else -1
        idx_dur = m_dur.start() if m_dur else -1
        
        if idx_time != -1:
            # Found a spell line
            
            # Name
            raw_name = full_line[:idx_time].strip()
            name = re.sub(r"[-–—]\s*$", "", raw_name).strip()
            
            # Time
            next_idxs = [i for i in [idx_range, idx_comp, idx_dur] if i != -1 and i > idx_time]
            end_time = min(next_idxs) if next_idxs else len(full_line)
            time_start = m_time.end()
            time_val = full_line[time_start:end_time].strip()
            time_val = re.sub(r"^[:\s\u2013\u2014-]+", "", time_val).strip()
            time_val = re.sub(r"[-–—]\s*$", "", time_val).strip()
            
            # Range
            range_val = ""
            if idx_range != -1:
                next_idxs = [i for i in [idx_comp, idx_dur] if i != -1 and i > idx_range]
                end_range = min(next_idxs) if next_idxs else len(full_line)
                range_start = m_range.end()
                range_val = full_line[range_start:end_range].strip()
                range_val = re.sub(r"^[:\s\u2013\u2014-]+", "", range_val).strip()
                range_val = re.sub(r"[-–—]\s*$", "", range_val).strip()
            
            # Components
            comp_val = ""
            if idx_comp != -1:
                next_idxs = [i for i in [idx_dur] if i != -1 and i > idx_comp]
                end_comp = min(next_idxs) if next_idxs else len(full_line)
                comp_start = m_comp.end()
                comp_val = full_line[comp_start:end_comp].strip()
                comp_val = re.sub(r"^[:\s\u2013\u2014-]+", "", comp_val).strip()
                comp_val = re.sub(r"[-–—]\s*$", "", comp_val).strip()
            
            # Duration
            dur_val = ""
            if idx_dur != -1:
                dur_start = m_dur.end()
                dur_val = full_line[dur_start:].strip()
                dur_val = re.sub(r"^[:\s\u2013\u2014-]+", "", dur_val).strip()
            
            # Ritual Check
            if re.search(r"[-–—]\s*R$", dur_val) or re.search(r"\bR\b", dur_val[-5:]):
                 name += " (R)"
                 dur_val = re.sub(r"[-–—]\s*R$", "", dur_val).strip()
            
            # Determine source/prepared
            prepared = False
            source = "Wizard" # Default
            
            h_color = highlight_color
            
            if h_color in COLOR_WIZ_PREP:
                prepared = True
                source = "Wizard"
            elif h_color in COLOR_SORC_PREP:
                prepared = True
                source = "Sorcerer" 
            elif h_color in COLOR_WIZ_UNPREP:
                prepared = False
                source = "Wizard"
            elif h_color == "Auto/Black" or h_color is None:
                 # Skip black
                 continue
            else:
                # Unknown color, treat as black/skip
                continue
                
            spell_obj = {
                "id": str(uuid.uuid4()),
                "name": name,
                "level": current_level,
                "prepared": prepared,
                "source": source,
                "time": time_val,
                "range": range_val,
                "comp": comp_val,
                "dur": dur_val,
                "desc": f"{full_line}" 
            }
            full_text_spells.append(spell_obj)

    print(f"Extracted {len(full_text_spells)} spells.")
    
    if len(full_text_spells) > 0:
        if os.path.exists(pkl_path):
            with open(pkl_path, "rb") as f:
                data = pickle.load(f)
            
            if "spells" not in data:
                data["spells"] = []
                
            existing_names = {s["name"] for s in data["spells"]}
            added = 0
            for s in full_text_spells:
                if s["name"] not in existing_names:
                    data["spells"].append(s)
                    added += 1
            
            # Ensure "features" is also preserved/handled by other scripts
            
            with open(pkl_path, "wb") as f:
                pickle.dump(data, f)
                
            print(f"Added {added} new spells to {pkl_path}")
        else:
            print("Pickle file not found.")

except Exception as e:
    print(f"Error: {e}")
