import tkinter as tk
from tkinter import ttk
from Monitor_Procesov import zobraz_beziace_procesy

# Funkcia na zobrazenie procesov v okne
def zobraz_procesy_gui():
    procesy = zobraz_beziace_procesy()
    text.delete(*text.get_children())  # Vymaže staré riadky v tabuľke
    proces_map = {}  # Mapa pre zoskupovanie procesov

    # Uloženie procesov do mapy
    for proces in procesy:
        if proces['name'] in proces_map:
            proces_map[proces['name']].append(proces)
        else:
            proces_map[proces['name']] = [proces]

    # Vloženie zoskupených procesov do tabuľky
    for name, proces_list in proces_map.items():
        if len(proces_list) > 1:
            # Spočítanie celkovej pamäte pre PP
            total_memory = sum(proces['memory'] for proces in proces_list)
            # Pridanie riadku pre zoskupený proces, ktorý bude zminimalizovaný
            parent = text.insert('', 'end', text=name, values=('', f"{name} ({len(proces_list)})", f"{total_memory:.2f} MB"), open=False)
            # Pridanie podriadených procesov s odsadením
            for proces in proces_list:
                text.insert(parent, 'end', text=proces['pid'], values=(proces['pid'], f"    {proces['name']}", f"{proces['memory']:.2f} MB"))  # Odsadenie
        else:
            # Pridanie normálneho procesu
            proces = proces_list[0]
            text.insert('', 'end', text=proces['pid'], values=(proces['pid'], proces['name'], f"{proces['memory']:.2f} MB"))

    # Zmena písma pre tabuľku
    for item in text.get_children():
        text.item(item, tags=('bold',))  # Všetky riadky ako tučné
        # Ak je to podriadený proces, zmeniť tag na normálne
        if text.parent(item):
            text.item(item, tags=('normal',))

# Hlavné okno aplikácie
app = tk.Tk()
app.title("SysMon - Monitor systému")  # Zatiaľ názov, upravíme neskôr
app.geometry("800x600")  # Zväčšené okno
app.configure(bg="#2E2E2E")  # Tmavé pozadie aplikácie

# Nastavenie štýlu pre aplikáciu
style = ttk.Style(app)
style.theme_use('default')
style.configure("TButton", background="#444444", foreground="white", padding=6, relief="flat")
style.configure("TLabel", background="#2E2E2E", foreground="white")
style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", borderwidth=0)
style.configure("Treeview.Heading", background="#444444", foreground="white", borderwidth=1)

# Tabuľka na zobrazenie procesov
text = ttk.Treeview(app, columns=('PID', 'Názov', 'Pamäť (MB)'), show='headings', height=25)  # Zvýšený počet riadkov
text.heading('PID', text='PID')
text.heading('Názov', text='Názov')
text.heading('Pamäť (MB)', text='Pamäť (MB)')
text.column('PID', width=80, anchor=tk.CENTER)
text.column('Názov', width=250, anchor=tk.W)
text.column('Pamäť (MB)', width=120, anchor=tk.CENTER)
text.pack(pady=10)

# Nastavenie scrollbar-u pre tabuľku
scrollbar = ttk.Scrollbar(app, orient="vertical", command=text.yview)
scrollbar.pack(side="right", fill="y")
text.configure(yscrollcommand=scrollbar.set)

# Tlačidlo na spustenie monitorovania procesov
tlacidlo = ttk.Button(app, text="Zobraziť bežiace procesy", command=zobraz_procesy_gui)
tlacidlo.pack(pady=10)

# Nastavenie písma pre procesy
text.tag_configure('normal', font=('Arial', 10))  # Normálne písmo pre podriadené procesy
text.tag_configure('bold', font=('Arial', 10, 'bold'))  # Tučné písmo pre hlavné procesy

# Spustenie hlavnej slučky aplikácie
app.mainloop()
