import os
os.system('cls' if os.name == 'nt' else 'clear')  # clear console

import tkinter as tk

import my_app
from my_app import MyApp


if __name__ == "__main__":
    root = tk.Tk()
    MyApp(root)
    root.mainloop()