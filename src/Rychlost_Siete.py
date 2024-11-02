import tkinter as tk
from tkinter import ttk
import speedtest
import threading
import time

def zobraz_rychlost_internetu(frame):
    # Vyčistenie Mainu
    for widget in frame.winfo_children():
        widget.destroy()

    # Štýl
    style = ttk.Style()
    style.configure("TLabel", background="#2E2E2E", foreground="white", font=('Arial', 14))

    # Zobrazenie Rýchlosti
    info_frame = tk.Frame(frame, bg="#2E2E2E")
    info_frame.pack(pady=10, padx=10, fill="both", expand=True)

    label_rychlost = ttk.Label(info_frame, text="Rýchlosť internetu:", font=('Arial', 16))
    label_rychlost.pack(pady=10)

    # Sťahovanie
    label_download_text = ttk.Label(info_frame, text="Sťahovanie:", font=('Arial', 14))
    label_download_text.pack(pady=5)
    label_download_value = ttk.Label(info_frame, text="N/A", font=('Arial', 14), foreground="#00CED1")
    label_download_value.pack(pady=5)

    # Odosielanie
    label_upload_text = ttk.Label(info_frame, text="Odosielanie:", font=('Arial', 14))
    label_upload_text.pack(pady=5)
    label_upload_value = ttk.Label(info_frame, text="N/A", font=('Arial', 14), foreground="#C71585")
    label_upload_value.pack(pady=5)

    # História
    historia_frame = tk.Frame(frame, bg="#2E2E2E")
    historia_frame.pack(pady=10, padx=10, fill="both", expand=True)
    ttk.Label(historia_frame, text="História:", font=('Arial', 14), background="#2E2E2E", foreground="white").pack()

    # História Listbox
    historia_listbox = tk.Listbox(historia_frame, font=('Arial', 12), bg="#1C1C1C", fg="white", height=10, width=50)
    historia_listbox.pack(pady=5)

    # Loading
    def nacitavanie_bodiek(label):
        Bodky = [" .", " ..", " ..."]
        i = 0
        while not stop_loading[0]:  
            label.config(text=Bodky[i % len(Bodky)])
            i += 1
            time.sleep(0.5)

    # Meranie Rýchlosti
    def meraj_rychlost():
        stop_loading[0] = False
        tlacidlo_meraj.config(state="disabled", text="Prebieha Meranie", bg="gray")
        label_download_value.config(text="")  
        label_upload_value.config(text="")

        # Loading Animácia
        bodky_thread_download = threading.Thread(target=nacitavanie_bodiek, args=(label_download_value,))
        bodky_thread_upload = threading.Thread(target=nacitavanie_bodiek, args=(label_upload_value,))
        bodky_thread_download.start()
        bodky_thread_upload.start()

        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / (1024 * 1024)
            upload_speed = st.upload() / (1024 * 1024)
            label_download_value.config(text=f"{download_speed:.2f} Mbps")
            label_upload_value.config(text=f"{upload_speed:.2f} Mbps")
            
            # Pridanie Výsledku do tej Histórie
            
            historia_listbox.insert(tk.END, f"Sťahovanie: {download_speed:.2f} Mbps | Odosielanie: {upload_speed:.2f} Mbps")
        except Exception as e:
            label_download_value.config(text="Chyba pri meraní")
            label_upload_value.config(text="Chyba pri meraní")
            print(f"Chyba pri meraní rýchlosti: {e}")
        finally:
            stop_loading[0] = True 
            tlacidlo_meraj.config(state="normal", text="Zmerať rýchlosť", bg="#4CAF50") 

    # Obnovenie Rýchlosti Button
    tlacidlo_meraj = tk.Button(info_frame, text="Zmerať rýchlosť", command=lambda: threading.Thread(target=meraj_rychlost).start(), font=('Arial', 12), bg="#4CAF50", fg="white")
    tlacidlo_meraj.pack(pady=10)

stop_loading = [True]
