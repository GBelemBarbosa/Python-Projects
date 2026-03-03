import customtkinter as ctk
import threading
import time
import random

app = ctk.CTk()
app.geometry("200x200")

label = ctk.CTkLabel(app, text="0", font=("Arial", 40))
label.pack(expand=True)

def roller():
    def setup():
        label.configure(text="Started")
    app.after(0, setup)
    
    # simulate dice roll animation
    sleep_time = 0.05
    for i in range(20):
        current = random.randint(1, 20)
        # Attempt 1: app.after
        app.after(0, lambda r=current: label.configure(text=str(r)))
        
        # In custom tkinter, if we don't update from the background thread,
        # app.after might just queue up. But the main loop should run!
        time.sleep(sleep_time)
        sleep_time += 0.01

    def finalize(img="Done"):
        label.configure(text=img)
    app.after(0, finalize)

def start_roll():
    threading.Thread(target=roller).start()

btn = ctk.CTkButton(app, text="Roll", command=start_roll)
btn.pack(pady=20)

# We can run it for 3 seconds then close
app.after(3000, app.destroy)
app.mainloop()
