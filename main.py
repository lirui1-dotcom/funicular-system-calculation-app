import os
os.system('cls' if os.name == 'nt' else 'clear')  # clear console

# ─── CRITICAL: Enable DPI awareness BEFORE Tk() to prevent blurry text on high-DPI displays ───
import sys
if sys.platform == 'win32':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except (ImportError, AttributeError, OSError):
        # Fallback for older Windows or ctypes unavailable
        pass
# Select Matplotlib backend before any pyplot import to avoid
# the TkAgg backend from altering DPI awareness at import time.
import matplotlib   
matplotlib.use("TkAgg")

import tkinter as tk

import my_app
from my_app import MyApp


if __name__ == "__main__":
    root = tk.Tk()
    MyApp(root)
    root.mainloop() 
