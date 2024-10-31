import tkinter as tk
from tkinter import ttk
import psutil

def zobraz_procesy_gui(frame):
    # Vyčistenie Pravej časti
    for widget in frame.winfo_children():
        widget.destroy()

    # Nastavenie farieb pre Treeview
    style = ttk.Style()
    style.configure("Treeview", background="#383838", foreground="white", fieldbackground="#2E2E2E")
    style.map('Treeview', background=[('selected', '#575757')], foreground=[('selected', 'white')])  

    # Tabuľka Na Procesy
    text = ttk.Treeview(frame, columns=('PID', 'Názov', 'Pamäť (MB)'), show='headings', height=25, style="Treeview")
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

    # Funkcia Na Procesy
    def zobraz_beziace_procesy():
        procesy = []
        for proces in psutil.process_iter(['pid', 'name', 'memory_info']):
            info = proces.info
            procesy.append({
                'pid': info['pid'],
                'name': info['name'],
                'memory': info['memory_info'].rss / (1024 * 1024) 
            })
        return procesy

    def aktualizuj_procesy():
        procesy = zobraz_beziace_procesy()
        text.delete(*text.get_children())
        proces_map = {}

        # Uloženie Foldrov
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

        # Obnovenie Foldrov
        for item, is_open in open_items.items():
            if is_open:
                text.item(item, open=True)

        # Každé 2s Update
        frame.after(2000, aktualizuj_procesy)

    aktualizuj_procesy()
