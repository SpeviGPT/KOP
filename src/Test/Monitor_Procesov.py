import tkinter as tk
from tkinter import ttk
import psutil

def zobraz_procesy_gui(frame):
    # Vyčistiť obsah predchádzajúcej obrazovky
    for widget in frame.winfo_children():
        widget.destroy()

    # Tabuľka na zobrazenie procesov
    text = ttk.Treeview(frame, columns=('PID', 'Názov', 'Pamäť (MB)'), show='headings', height=25)
    text.heading('PID', text='PID')
    text.heading('Názov', text='Názov')
    text.heading('Pamäť (MB)', text='Pamäť (MB)')
    text.column('PID', width=80, anchor=tk.CENTER)
    text.column('Názov', width=250, anchor=tk.W)
    text.column('Pamäť (MB)', width=120, anchor=tk.CENTER)
    text.pack(pady=10, fill='both', expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
    scrollbar.pack(side="right", fill="y")
    text.configure(yscrollcommand=scrollbar.set)

    # Funkcia na zobrazenie procesov
    def zobraz_beziace_procesy():
        procesy = []
        for proces in psutil.process_iter(['pid', 'name', 'memory_info']):
            info = proces.info
            procesy.append({
                'pid': info['pid'],
                'name': info['name'],
                'memory': info['memory_info'].rss / (1024 * 1024)  # Prevod na MB
            })
        return procesy

    def aktualizuj_procesy():
        procesy = zobraz_beziace_procesy()
        text.delete(*text.get_children())
        proces_map = {}

        # Uloženie otvorených "foldrov"
        open_items = {}
        for item in text.get_children():
            open_items[item] = text.item(item)['open']

        for proces in procesy:
            if proces['name'] in proces_map:
                proces_map[proces['name']].append(proces)
            else:
                proces_map[proces['name']] = [proces]

        for name, proces_list in proces_map.items():
            if len(proces_list) > 1:
                total_memory = sum(proces['memory'] for proces in proces_list)
                parent = text.insert('', 'end', text=name, values=('', f"{name} ({len(proces_list)})", f"{total_memory:.2f} MB"), open=False)
                for proces in proces_list:
                    text.insert(parent, 'end', text=proces['pid'], values=(proces['pid'], f"    {proces['name']}", f"{proces['memory']:.2f} MB"))
            else:
                proces = proces_list[0]
                text.insert('', 'end', text=proces['pid'], values=(proces['pid'], proces['name'], f"{proces['memory']:.2f} MB"))

        # Obnovenie stavu "foldrov"
        for item, is_open in open_items.items():
            if is_open:
                text.item(item, open=True)

        # Nastavenie ďalšej aktualizácie po 2000 ms (2 sekundy)
        frame.after(2000, aktualizuj_procesy)

    aktualizuj_procesy()  # Automatické spustenie aktualizácie procesov
