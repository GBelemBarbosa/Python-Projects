import customtkinter as ctk

app = ctk.CTk()

schools = {
    "Abjuration": "🛡️", "Conjuration": "🌀", "Divination": "👁️",
    "Enchantment": "💫", "Evocation": "💥", "Illusion": "🎭",
    "Necromancy": "💀", "Transmutation": "🧪", "Unknown": "📜"
}

from tkinter.font import Font
f = Font(font=("Roboto", 12))

print("Original:")
for k, v in schools.items():
    print(f"  {v} : {f.measure(v)}")

print("\nStripped U+FE0F:")
for k, v in schools.items():
    stripped = v.replace('\uFE0F', '')
    print(f"  {stripped} : {f.measure(stripped)}")
    
    # Check if rendering changes
    
import sys
sys.exit(0)
