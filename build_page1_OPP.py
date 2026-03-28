import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config import (p1_presets,
                    p1_table1_labels)

class Page1(ttk.Frame):
    """OOP refactor of previous procedural page1_table1.

    - Encapsulates all widgets and state
    - Keeps the external function `page1_table1(root)` as a thin wrapper
      so existing call sites do not need changes
    - Makes it easier to add table2, presets, export, and testing
    """

    def __init__(self, parent, presets, table1_labels, *args, **kwargs):
        super().__init__(parent, padding=15, *args, **kwargs)
        self.presets = presets
        self.table1_labels = table1_labels

        # state
        self.selected = tk.StringVar(value="手动输入")
        self.entries = []  # list of Entry widgets for table1
        self.entries_by_table = {}

        # build UI
        self._build_layout()

    # ------------------------- builders ------------------------------
    def _build_layout(self):
        # table block
        self.table_block1 = ttk.Frame(self)
        self.table_block1.pack(fill="both", expand=True)

        # header and preset combobox
        self._build_header()

        # table area
        self.table1_frame = ttk.Frame(self.table_block1)
        self.table1_frame.pack(fill="both", expand=True)

        self._build_table1(self.table1_frame)

        # map for later preset handling
        self.entries_by_table = {"table1": self.entries}

        # footer
        self.footer = ttk.Frame(self)
        self.footer.pack(fill="x", pady=(10, 0))

    def _build_header(self):
        header1 = ttk.Frame(self.table_block1)
        header1.pack(fill="x", pady=(0, 10))

        header1.grid_columnconfigure(0, weight=1)
        header1.grid_columnconfigure(1, weight=1)
        header1.grid_columnconfigure(2, weight=1)

        ttk.Label(
            header1,
            text="一",
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=(20, 0))

        ttk.Label(
            header1,
            text="基本参数",
            font=("Segoe UI", 14, "bold"),
            anchor="center"
        ).grid(row=0, column=1, sticky="ew")

        right_container = ttk.Frame(header1)
        right_container.grid(row=0, column=2, sticky="e")

        ttk.Label(right_container, text="数据录入:", font=("Arial", 10)).pack(side="left", padx=(0, 8))

        self.preset_combo = ttk.Combobox(
            right_container,
            values=["手动输入"] + list(self.presets.keys()),
            textvariable=self.selected,
            state="readonly",
            font=("Arial", 9),
            width=10,
            style="option_menu.TCombobox"
        )
        self.preset_combo.pack(side="left")
        self.preset_combo.bind("<<ComboboxSelected>>", self.apply_preset)

    def _build_table1(self, parent):
        table1 = ttk.Frame(parent, borderwidth=2, relief="solid", padding=10)
        table1.pack(fill="x")

        # column spacing
        table1.grid_columnconfigure(0, minsize=40, weight=0)
        table1.grid_columnconfigure(1, minsize=200, weight=1)
        table1.grid_columnconfigure(2, minsize=80, weight=1)
        table1.grid_columnconfigure(3, minsize=80, weight=1)
        table1.grid_columnconfigure(4, minsize=80, weight=1)
        table1.grid_columnconfigure(5, minsize=120, weight=0)

        for r, (idx, label_text) in enumerate(self.table1_labels, start=1):
            ttk.Label(table1, text=idx, font=("Arial", 12, "bold")).grid(
                row=r, column=0, padx=5, pady=4
            )

            ttk.Label(table1, text=label_text, font=("Arial", 12)).grid(
                row=r, column=1, padx=5, pady=4, sticky="w"
            )

            e = ttk.Entry(table1, justify="right", font=("Arial", 12), width=11)
            e.grid(row=r, column=5, padx=5, pady=4)


    # ------------------------- actions -------------------------------
    def clear_all(self):
        for entry_list in self.entries_by_table.values():
            for entry in entry_list:
                entry.delete(0, tk.END)

    def apply_preset(self, event=None):
        name = self.selected.get()

        if name == "手动输入":
            self.clear_all()
            return

        self.clear_all()

        table1_data = self.presets.get(name, {}).get("table1", {})
        for entry, (_, label_text) in zip(self.entries_by_table["table1"], self.table1_labels):
            if label_text in table1_data:
                entry.insert(0, table1_data[label_text])

    # ------------------------- helpers -------------------------------
    def get_table1_values(self):
        return [e.get() for e in self.entries]

    def set_table1_values(self, values):
        for e, v in zip(self.entries, values):
            e.delete(0, tk.END)
            e.insert(0, v)


# backwards-compatible wrapper
def page1_table1(root):
    """Compatibility wrapper for older procedural usage: creates the page UI."""
    page = Page1(root, p1_presets, p1_table1_labels)
    page.pack(fill="both", expand=True)
    return page 

# def page1_table2(root):










