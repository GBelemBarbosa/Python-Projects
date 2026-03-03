import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x600")

schools = {
    "Abjuration": "🛡️", "Conjuration": "🌀", "Divination": "👁️",
    "Enchantment": "💫", "Evocation": "💥", "Illusion": "🎭",
    "Necromancy": "💀", "Transmutation": "🧪", "Unknown": "📜"
}

f1 = ctk.CTkFrame(app)
f1.pack(pady=10)
ctk.CTkLabel(f1, text="Roboto 12").pack()
for k, v in schools.items():
    row = ctk.CTkFrame(f1, fg_color="gray30")
    row.pack(pady=2, fill="x")
    sym_container = ctk.CTkFrame(row, width=24, height=24, fg_color="gray50")
    sym_container.pack_propagate(False)
    sym_container.pack(padx=5, pady=5)
    sym_lbl = ctk.CTkLabel(sym_container, text=v, font=("Roboto", 12), fg_color="gray70")
    sym_lbl.place(relx=0.5, rely=0.5, anchor="center")

f2 = ctk.CTkFrame(app)
f2.pack(pady=10)
ctk.CTkLabel(f2, text="Segoe UI Emoji 12").pack()
for k, v in schools.items():
    row = ctk.CTkFrame(f2, fg_color="gray30")
    row.pack(pady=2, fill="x")
    sym_container = ctk.CTkFrame(row, width=24, height=24, fg_color="gray50")
    sym_container.pack_propagate(False)
    sym_container.pack(padx=5, pady=5)
    sym_lbl = ctk.CTkLabel(sym_container, text=v, font=("Segoe UI Emoji", 12), fg_color="gray70")
    sym_lbl.place(relx=0.5, rely=0.5, anchor="center")

# Also run an automated check of width sizes
for font_name in ["Roboto", "Segoe UI Emoji"]:
    print(f"Font: {font_name}")
    from tkinter.font import Font
    try:
        f = Font(font=(font_name, 12))
        for k, v in schools.items():
            print(f"  {v}: {f.measure(v)}")
    except:
        pass

app.update()
app.after(2000, app.destroy)
app.mainloop()
