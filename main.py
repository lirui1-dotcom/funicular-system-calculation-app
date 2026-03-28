import os
os.system('cls' if os.name == 'nt' else 'clear')  # clear console

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import build_page1


# ===============================================================
# LAYOUT STRUCTURE
# ===============================================================
# root
# ├─ menu_bar
# └─ page1                    (pack, expand)
#     ├─ table_block1         (pack, expand)
#     │   ├─ header1          (pack)
#     │   │   ├─ title        (grid)
#     │   │   ├─ preset_lbl   (grid)
#     │   │   └─ preset_combo (grid)
#     │   └─ table_frame      (pack, expand)
#     │       └─ table1       (grid)
#     └─ footer               (pack)

# ===============================================================
# MAIN WINDOW
# =============================================================== 
root = tk.Tk()
root.title("双往复式客运缆车系统运行参数计算程序")
#root.minsize(600, 350)
root.configure(bg="#E4E2E2")

# ===============================================================
# STYLE (FROM PyUIBuilder)
# ===============================================================
style = ttk.Style(root)
style.theme_use("vista")

style.configure(
    "option_menu.TCombobox",
    fieldbackground="#E4E2E2",
    foreground="#000"
)

# ===============================================================
# MENU BAR (EXCEL-READY)
# ===============================================================

menu_bar = tk.Menu(root, font=("Arial", 12))   # top-level bar
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 9))  # dropdown items


def import_excel():
    path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not path:
        return
    messagebox.showinfo("Import", f"Excel selected:\n{path}")
    # Hook point: pandas.read_excel(path)

def export_excel():
    path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")]
    )
    if not path:
        return
    messagebox.showinfo("Export", f"Export to:\n{path}")
    # Hook point: dataframe.to_excel(path, index=False)

file_menu.add_command(label="Import Excel…", command=import_excel)
file_menu.add_command(label="Export Excel…", command=export_excel)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="File", menu=file_menu)

# ===============================================================
# Page 1
# ===============================================================
# Compose page using the central `page1_table1` function (header + tables)
build_page1.page1_table1(root)
  







root.mainloop()
