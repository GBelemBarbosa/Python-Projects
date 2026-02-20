import os

file_path = r"ClientRPG/D&D 5.5e - G(r)ay.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = 0

for i, line in enumerate(lines):
    if skip > 0:
        skip -= 1
        continue
        
    if "self.qp_chk = ctk.CTkCheckBox(footer" in line:
        # Found the start of the bad block.
        # We want to replace this line and the next 3 lines (font, width, border)
        # The bad block likely spans 3 or 4 lines.
        # Let's verify we are in the right place.
        print(f"Found target at line {i+1}")
        
        # Insert clean block
        new_lines.append('        self.qp_chk = ctk.CTkCheckBox(footer, text="Quick Prep (1/LR)", variable=self.quick_prep_used,\n')
        new_lines.append('                                       font=("Roboto", 10), fg_color=self.color,\n')
        new_lines.append('                                       checkbox_width=18, checkbox_height=18, hover_color=self.color,\n')
        new_lines.append('                                       border_color=self.color)\n')
        
        # Now we need to determine how many lines to skip.
        # We skipped lines until we hit the next statement or empty line?
        # The next statement is `        # Add some padx to separate from button` (line 1803 in view) or `self.qp_chk.grid`
        # Let's peek ahead.
        # Just skipping 3 lines is risky if user has 4 lines.
        # Let's look for "self.qp_chk.grid" to stop skipping.
        
        j = i + 1
        while j < len(lines):
            if "self.qp_chk.grid" in lines[j]:
                break
            j += 1
        
        skip = j - i - 1 # Skip the lines between start and grid
        print(f"Skipping {skip} lines of bad code.")
        
    else:
        new_lines.append(line)

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
    
print("File fixed.")
