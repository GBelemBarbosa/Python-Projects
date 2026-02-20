import zipfile
import re
import os

docx_path = r"ClientRPG/Molina.docx"

if not os.path.exists(docx_path):
    print(f"File not found: {docx_path}")
    exit()

try:
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read("word/document.xml").decode("utf-8")
        
    # Regex approach: Find all runs
    # A run is typically <w:r ...> ... </w:r>
    # Logic: simple split by <w:r> isn't perfect but scanning the string is better.
    
    # Let's find all occurrences of <w:r [^>]*>(.*?)</w:r>
    # Note: DOTALL is needed
    runs = re.findall(r'(<w:r(?: [^>]*)?>.*?</w:r>)', xml_content, re.DOTALL)
    
    colors_found = {}
    
    for run_content in runs:
        # Check for text
        text_match = re.search(r'<w:t(?: [^>]*)?>(.*?)</w:t>', run_content, re.DOTALL)
        if text_match:
            text = text_match.group(1).strip()
            if not text:
                continue
                
            # Check for color
            # <w:color w:val="HEX"/>
            color = "Auto/Black"
            color_match = re.search(r'<w:color [^>]*w:val="([^"]+)"', run_content)
            if color_match:
                color = color_match.group(1)
            
            if color not in colors_found:
                colors_found[color] = []
            
            if len(colors_found[color]) < 10: 
                colors_found[color].append(text)
                    
    print(f"Parsed {len(runs)} runs.")
    print("Colors found and sample text:")
    for color, texts in colors_found.items():
        print(f"Color: {color} -> {texts}")

except Exception as e:
    print(f"Error: {e}")
