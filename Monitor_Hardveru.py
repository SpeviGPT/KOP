import tkinter as tk
from tkinter import ttk
import psutil
import GPUtil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Funkcia na získanie vyťaženia CPU a GPU v %
def ziskaj_vytazenie():
    vytazenie_cpu = psutil.cpu_percent(interval=0.1)
    gpu = GPUtil.getGPUs()
    vytazenie_gpu = gpu[0].load * 100 if gpu else 0
    return vytazenie_cpu, vytazenie_gpu

# Aktualizácia grafu a barov
def aktualizuj_graf(canvas, ax, cpu_vytazenie, gpu_vytazenie, max_points, bar_cpu, bar_gpu, cpu_label, gpu_label):
    vytazenie_cpu, vytazenie_gpu = ziskaj_vytazenie()

    # Aktualizácia barov
    bar_cpu['value'] = vytazenie_cpu
    bar_gpu['value'] = vytazenie_gpu
    cpu_label.config(text=f"{vytazenie_cpu:.1f}%")
    gpu_label.config(text=f"{vytazenie_gpu:.1f}%")

    # Pridanie hodnôt do zoznamov
    cpu_vytazenie.append(vytazenie_cpu)
    gpu_vytazenie.append(vytazenie_gpu)

    # Obmedzenie počtu bodov
    if len(cpu_vytazenie) > max_points:
        cpu_vytazenie.pop(0)
        gpu_vytazenie.pop(0)

    # Aktualizácia grafu
    ax.clear()
    ax.fill_between(range(len(cpu_vytazenie)), 0, cpu_vytazenie, color='#32CD32', alpha=0.7, label='CPU vyťaženie (%)')
    ax.plot(gpu_vytazenie, color='#FF4500', linewidth=2, label='GPU vyťaženie (%)')
    
    ax.grid(color='black', linestyle='-', linewidth=0.5)
    ax.set_ylim(0, 100)
    ax.set_title('Vyťaženie CPU a GPU', color='white')
    ax.set_xlabel('Čas (sekundy)', color='white')
    ax.set_ylabel('Vyťaženie (%)', color='white')
    ax.set_facecolor('#2E2E2E')
    ax.tick_params(axis='both', colors='white')
    ax.legend(loc='upper right', facecolor='black', edgecolor='white', prop={'size': 10, 'weight': 'bold'}, labelcolor='white')
    
    # Aktualizácia canvasu
    canvas.draw()
    canvas.get_tk_widget().after(1000, aktualizuj_graf, canvas, ax, cpu_vytazenie, gpu_vytazenie, max_points, bar_cpu, bar_gpu, cpu_label, gpu_label)


def spust_monitor_hardveru(right_frame):
    # Vyčistenie tej pravej časti
    for widget in right_frame.winfo_children():
        widget.destroy()
    
    cpu_vytazenie = []
    gpu_vytazenie = []
    max_points = 300  # 5 minút

    # Rám pre horizontálne rozloženie
    main_frame = tk.Frame(right_frame, bg="#2E2E2E")
    main_frame.pack(side="left", fill="both", expand=True, padx=10)

    # Rám pre bary
    bar_frame = tk.Frame(main_frame, bg="#2E2E2E")
    bar_frame.pack(side="left")

    # Rám pre vertikálne bary
    cpu_frame = tk.Frame(bar_frame, bg="#2E2E2E")
    cpu_frame.pack(side="left", padx=5)
    
    gpu_frame = tk.Frame(bar_frame, bg="#2E2E2E")
    gpu_frame.pack(side="left", padx=5)

    # CPU bar
    cpu_label = ttk.Label(cpu_frame, text="CPU", foreground="white", background="#2E2E2E")
    cpu_label.pack()
    bar_cpu = ttk.Progressbar(cpu_frame, orient="vertical", length=300, mode="determinate", maximum=100, style="Green.Vertical.TProgressbar")
    bar_cpu.pack(pady=5)
    cpu_value_label = ttk.Label(cpu_frame, text="0%", foreground="white", background="#2E2E2E")
    cpu_value_label.pack()

    # GPU bar
    gpu_label = ttk.Label(gpu_frame, text="GPU", foreground="white", background="#2E2E2E")
    gpu_label.pack()
    bar_gpu = ttk.Progressbar(gpu_frame, orient="vertical", length=300, mode="determinate", maximum=100, style="Red.Vertical.TProgressbar")
    bar_gpu.pack(pady=5)
    gpu_value_label = ttk.Label(gpu_frame, text="0%", foreground="white", background="#2E2E2E")
    gpu_value_label.pack()

    # Definovanie farieb pre CPU a GPU bary
    style = ttk.Style()
    style.configure("Green.Vertical.TProgressbar", troughcolor="#2E2E2E", background="#32CD32")
    style.configure("Red.Vertical.TProgressbar", troughcolor="#2E2E2E", background="#FF4500")

    # Graf
    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side="right", fill=tk.BOTH, expand=True)

    # Nastavenie dark módu
    fig.patch.set_facecolor('#2E2E2E')
    ax.set_facecolor('#2E2E2E')

    # Spustenie aktualizácie grafu
    aktualizuj_graf(canvas, ax, cpu_vytazenie, gpu_vytazenie, max_points, bar_cpu, bar_gpu, cpu_value_label, gpu_value_label)
