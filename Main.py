import tkinter as tk
from tkinter import ttk
from Monitor_Procesov import zobraz_procesy_gui
from Monitor_Hardveru import spust_monitor_hardveru
from Rychlost_Siete import zobraz_rychlost_internetu

# Okno :3
app = tk.Tk()
app.title("Katon - Monitor systému")
app.geometry("1000x600")
app.configure(bg="#2E2E2E")

# Štýl
style = ttk.Style(app)
style.theme_use('default')
style.configure("TButton", background="#444444", foreground="white", padding=6, relief="flat")
style.configure("TLabel", background="#2E2E2E", foreground="white")

# Tie Buttony Na Ľavo
left_frame = tk.Frame(app, bg="#2E2E2E", width=200)
left_frame.pack(side="left", fill="y")

# Otvorený Program
right_frame = tk.Frame(app, bg="#2E2E2E")
right_frame.pack(side="right", fill="both", expand=True)

# Tlačidlá
btn_monitor_procesov = ttk.Button(left_frame, text="Monitor procesov", command=lambda: zobraz_procesy_gui(right_frame))
btn_monitor_procesov.pack(pady=10)

btn_monitor_hardveru = ttk.Button(left_frame, text="Monitor hardvéru", command=lambda: spust_monitor_hardveru(right_frame))
btn_monitor_hardveru.pack(pady=10)

btn_monitor_internetu = ttk.Button(left_frame, text="Monitor internetu", command=lambda: zobraz_rychlost_internetu(right_frame))
btn_monitor_internetu.pack(pady=10)

# Nech Sa Zapne Monitor Procesov Ako Prvý
zobraz_procesy_gui(right_frame)

app.mainloop()
