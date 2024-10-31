import tkinter as tk
from tkinter import ttk
import speedtest

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

    label_download = ttk.Label(info_frame, text="Sťahovanie: N/A", font=('Arial', 14))
    label_download.pack(pady=5)

    label_upload = ttk.Label(info_frame, text="Odosielanie: N/A", font=('Arial', 14))
    label_upload.pack(pady=5)

    # Funkcia Meranie Rýchlosti
    def meraj_rychlost():
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / (1024 * 1024) 
            upload_speed = st.upload() / (1024 * 1024)  
            label_download.config(text=f"Sťahovanie: {download_speed:.2f} MB/s")
            label_upload.config(text=f"Odosielanie: {upload_speed:.2f} MB/s")
        except Exception as e:
            label_download.config(text="Sťahovanie: Chyba pri meraní")
            label_upload.config(text="Odosielanie: Chyba pri meraní")
            print(f"Chyba pri meraní rýchlosti: {e}")

    # Tlačidlo Na Obnovenie Rýchlosti
    tlacidlo_meraj = tk.Button(info_frame, text="Zmerať rýchlosť", command=meraj_rychlost, font=('Arial', 12), bg="#4CAF50", fg="white")
    tlacidlo_meraj.pack(pady=10)

    meraj_rychlost()
# EŠTE NEDOROBENÉ..
# Opraviť bug: vždy keď kliknem na tlačidlo rychlosť siete v main. crashne mi to... .-. ale táto časť je len na rýchlo.
