import tkinter as tk
from tkinter import ttk
from Monitor_Procesov import zobraz_procesy_gui

# Hlavné okno aplikácie
app = tk.Tk()
app.title("Katon - Monitor systému")
app.geometry("1000x600")
app.configure(bg="#2E2E2E")

# Nastavenie štýlu
style = ttk.Style(app)
style.theme_use('default')
style.configure("TButton", background="#444444", foreground="white", padding=6, relief="flat")
style.configure("TLabel", background="#2E2E2E", foreground="white")

# Vytvorenie rámca pre tlačidlá na ľavej strane
left_frame = tk.Frame(app, bg="#2E2E2E", width=200)
left_frame.pack(side="left", fill="y")

# Rámec pre obsah na pravej strane (tu sa bude zobrazovať obsah podľa výberu)
right_frame = tk.Frame(app, bg="#2E2E2E")
right_frame.pack(side="right", fill="both", expand=True)

# Tlačidlá pre jednotlivé funkcie
btn_monitor_procesov = ttk.Button(left_frame, text="Monitor procesov", command=lambda: zobraz_procesy_gui(right_frame))
btn_monitor_procesov.pack(pady=10)

btn_monitor_hardveru = ttk.Button(left_frame, text="Monitor hardvéru", command=lambda: print("Monitor hardvéru ešte nie je implementovaný."))
btn_monitor_hardveru.pack(pady=10)

btn_monitor_internetu = ttk.Button(left_frame, text="Monitor internetu", command=lambda: print("Monitor internetu ešte nie je implementovaný."))
btn_monitor_internetu.pack(pady=10)

# Automaticky otvorí monitor procesov po spustení
zobraz_procesy_gui(right_frame)

# Spustenie hlavnej slučky aplikácie
app.mainloop()
