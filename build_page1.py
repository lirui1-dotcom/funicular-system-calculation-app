import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config import (p1_presets,
                    p1_table1_labels,
                    p1_table1_important_labels,
                    p1_table2_label)


def page1_table2(parent):
    """Create table 2 UI inside `parent`.
    Returns (row_labels, entries_matrix) where entries_matrix is a list of rows,
    each row is a list of Entry widgets for the numeric columns.
    """
    table2_frame = ttk.Frame(parent)
    table2_frame.pack(fill="both", expand=True, pady=(10, 0))

    table2 = ttk.Frame(table2_frame, borderwidth=2, relief="solid", padding=8)
    table2.pack(fill="x")

    # set column widths (A..F)
    table2.grid_columnconfigure(0, minsize=40,  weight=0)
    table2.grid_columnconfigure(1, minsize=200, weight=0)
    table2.grid_columnconfigure(2, minsize=80, weight=1)
    table2.grid_columnconfigure(3, minsize=80, weight=1)
    table2.grid_columnconfigure(4, minsize=80, weight=1)
    table2.grid_columnconfigure(5, minsize=120, weight=0)

    row_labels = []
    entries_matrix = []

    for r, row in enumerate(p1_table2_label):
        # header row (first row) uses provided labels and no entry widgets
        if r == 0:
            for c, text in enumerate(row):
                ttk.Label(table2, text=text, font=("Arial", 11, "bold")).grid(
                    row=r, column=c, padx=5, pady=3, sticky="w"
                )
            continue

        # standard rows: first two columns are index and phase name
        idx_text, phase = row[0], row[1]
        ttk.Label(table2, text=idx_text, font=("Arial", 11, "bold")).grid(
            row=r, column=0, padx=5, pady=3
        )
        ttk.Label(table2, text=phase, font=("Arial", 11)).grid(
            row=r, column=1, padx=5, pady=3, sticky="w"
        )

        # create entries for the numeric columns (C-F)
        row_entries = []
        for c in range(2, 6):
            e = ttk.Entry(table2, justify="right", font=("Arial", 11), width=10)
            e.grid(row=r, column=c, padx=5, pady=3)
            row_entries.append(e)

        row_labels.append(phase)
        entries_matrix.append(row_entries)

    return row_labels, entries_matrix


def page1_table1(root):
    # ===============================================================
    # PAGE 1
    # ===============================================================
    
    
    page1 = ttk.Frame(root, padding=15)
    page1.pack(fill="both", expand=True)

    # ===============================================================
    # TABLE BLOCK
    # ===============================================================
    table_block1 = ttk.Frame(page1)
    table_block1.pack(fill="both", expand=True)

    # ===============================================================
    # HEADER
    # ===============================================================
    header1 = ttk.Frame(table_block1)
    header1.pack(fill="x", pady=(0, 10))

     # Force three equal-width columns
    header1.grid_columnconfigure(0, weight=1)
    header1.grid_columnconfigure(1, weight=1)
    header1.grid_columnconfigure(2, weight=1)

    # ─── Part 1: "一" left-aligned in left third ─────────────────────────────
    ttk.Label(
        header1,
        text="一",
        font=("Segoe UI", 14, "bold"),
        anchor="w"              # left-aligned inside the cell
    ).grid(row=0, column=0, sticky="w", padx=(20, 0))   # padding on left only

    # ─── Part 2: "基本参数" perfectly centered in middle third ───────────────
    ttk.Label(
        header1,
        text="基本参数",
        font=("Segoe UI", 14, "bold"),
        anchor="center"         # centers text inside its cell
    ).grid(row=0, column=1, sticky="ew")

    # ─── Part 3: "数据录入:" + combobox as a right-aligned unit ─────────────────────────────
    right_container = ttk.Frame(header1)
    right_container.grid(row=0, column=2, sticky="e")   # frame itself right-aligned in col 2

    # Inside the container: label + combobox packed left-to-right
    ttk.Label(
        right_container,
        text="数据录入:",
        font=("Arial", 10)
    ).pack(side="left", padx=(0, 8))   # small gap between label and combo

    selected = tk.StringVar(value="手动输入")
    preset_combo = ttk.Combobox(
        right_container,
        values=["手动输入"] + list(p1_presets.keys()),
        textvariable=selected,
        state="readonly",
        font=("Arial", 9),
        width=10,
        style="option_menu.TCombobox"
    )
    preset_combo.pack(side="left")
    # ===============================================================
    # TABLE AREA
    # ===============================================================
    table1_frame = ttk.Frame(table_block1)
    table1_frame.pack(fill="both", expand=True)

    table1 = ttk.Frame(table1_frame, borderwidth=2, relief="solid", padding=10)
    table1.pack(fill="x")

    # column spacing
    table1.grid_columnconfigure(0, minsize=40, weight=0)
    table1.grid_columnconfigure(1, minsize=200, weight=1)
    table1.grid_columnconfigure(2, minsize=80, weight=1)
    table1.grid_columnconfigure(3, minsize=80, weight=1)
    table1.grid_columnconfigure(4, minsize=80, weight=1)
    table1.grid_columnconfigure(5, minsize=120,weight=0)


    entries = []

    for r, (idx, label_text) in enumerate(p1_table1_labels, start=1):
        ttk.Label(table1, text=idx, font=("Arial", 12, "bold")).grid(
            row=r, column=0, padx=5, pady=4
        )

        ttk.Label(table1, text=label_text, font=("Arial", 12)).grid(
            row=r, column=1, padx=5, pady=4, sticky="w"
        )

        e = ttk.Entry(
            table1,
            justify="right",
            font=("Arial", 12),
            width=11
        )
        e.grid(row=r, column=5, padx=5, pady=4)

        if label_text in p1_table1_important_labels:
            e.configure(foreground="red")

        entries.append(e)

    # Create table2 below table1 and collect its entries
    table2_row_labels, table2_matrix = page1_table2(table_block1)

    # map table names to their entry lists for easy multi-table handling
    entries_by_table = {
        "table1": entries,
        "table2": [e for row in table2_matrix for e in row],
    }

    # ===============================================================
    # PRESET APPLY LOGIC
    # ===============================================================
    def apply_preset(event=None):
        name = selected.get()

        if name == "手动输入":
            # clear all entries for all tables
            for entry_list in entries_by_table.values():
                for entry in entry_list:
                    entry.delete(0, tk.END)
            return

        # clear all entries once before applying preset 
        # (otherwise inputs will affect preset values)
        for entry_list in entries_by_table.values():
            for entry in entry_list:
                entry.delete(0, tk.END)

        table1_data = p1_presets.get(name, {}).get("table1", {})
        for entry, (_, label_text) in zip(entries_by_table["table1"], p1_table1_labels):
            if label_text in table1_data:
                entry.insert(0, table1_data[label_text])

        # apply table2 presets (supports dict-of-dicts or list-of-lists)
        # table2_data = p1_presets.get(name, {}).get("table2", {})
        # for row_label, row_entries in zip(table2_row_labels, table2_matrix):
        #     preset_row = table2_data.get(row_label)
        #     if not preset_row:
        #         continue
        #     # allow either dict keyed by column header or list in column order
        #     if isinstance(preset_row, dict):
        #         col_headers = ["加速度(m/s²)", "末速度(m/s)", "运行时间(s)", "运行距离(m)"]
        #         for i, h in enumerate(col_headers):
        #             v = preset_row.get(h, "")
        #             if v != "":
        #                 row_entries[i].insert(0, v)
        #     elif isinstance(preset_row, (list, tuple)):
        #         for i, v in enumerate(preset_row):
        #             if v != "":
        #                 row_entries[i].insert(0, v)

    preset_combo.bind("<<ComboboxSelected>>", apply_preset)

    # ===============================================================
    # FOOTER (reserved for buttons later)
    # ===============================================================
    footer = ttk.Frame(page1)
    footer.pack(fill="x", pady=(10, 0))

    # ---- Example: read values (floats) -----------------------------
    # def read_values():
    #     values = [float(e.get()) for e in entries]
    #     print(values)
    # a=ttk.Button(page1, text="Read Values", command=read_values).pack()

# def page1_table2(root):










