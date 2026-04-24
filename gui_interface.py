import tkinter as tk
import subprocess
import sys

process = None

def start_navigation():
    global process
    if process is None:
        process = subprocess.Popen([sys.executable, "vision_system.py"])

def stop_navigation():
    global process
    if process is not None:
        process.terminate()
        process = None

window = tk.Tk()
window.title("Blind Assist Navigation System")
window.geometry("400x250")

title = tk.Label(window, text="AI Navigation Assistant", font=("Arial", 16))
title.pack(pady=20)

start_btn = tk.Button(window, text="Start Navigation", command=start_navigation, width=20, height=2)
start_btn.pack(pady=10)

stop_btn = tk.Button(window, text="Stop Navigation", command=stop_navigation, width=20, height=2)
stop_btn.pack(pady=10)

exit_btn = tk.Button(window, text="Exit", command=window.quit, width=20, height=2)
exit_btn.pack(pady=10)

window.mainloop()