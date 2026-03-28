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

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, padding=15, *args, **kwargs)
        
        # Make this frame fill its parent
        self.pack(fill="both", expand=True)          # ← here (self = the frame)
                                        
        # parameters
        self.presets = p1_presets
        self.table1_labels = p1_table1_labels
          
        # state
        self.selected = tk.StringVar(value="手动输入")
        self.entries = []  # list of Entry widgets for table1
        self.entries_by_table = {}

        # build UI
        self._build_layout()

    # ------------------------- builders ------------------------------
    def _build_layout(self):
        # Horizontal splitter: left pane for tables, right pane for main/plots
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        # Left pane (tables)
        self.left_pane = ttk.Frame(paned, padding=12)
        paned.add(self.left_pane, weight=1)

        # Use grid inside left pane so we can stack a controls row + two table areas
        self.left_pane.grid_rowconfigure(0, weight=0)  # controls
        self.left_pane.grid_rowconfigure(1, weight=0)  # table1 keeps natural height
        self.left_pane.grid_rowconfigure(2, weight=1)  # table2 fills remaining space
        self.left_pane.grid_columnconfigure(0, weight=1)

        # Controls row (preset combobox placed at top-right, above both tables)
        controls = ttk.Frame(self.left_pane)
        controls.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        controls.grid_columnconfigure(0, weight=1)

        right_container = ttk.Frame(controls)
        right_container.grid(row=0, column=1, sticky="e")

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

        # ── Table 1 (with custom larger title that includes Chinese labels) ────────────────────
        title1 = ttk.Label(self.left_pane, text="一   基本参数", font=('Segoe UI', 16, 'bold'))
        lf1 = ttk.LabelFrame(self.left_pane, labelwidget=title1, padding=10) 
        lf1.grid(row=1, column=0, sticky="nsew")  

        # table area inside lf1
        self._build_table1(lf1)

        # ── Table 2 (same) ────────────────────────────────────────
        title2 = ttk.Label(self.left_pane, text="二   运行速度图参数计算", font=('Segoe UI', 14, 'bold'))
        lf2 = ttk.LabelFrame(self.left_pane, labelwidget=title2, padding=10)
        lf2.grid(row=2, column=0, sticky="nsew")
        self.table2_frame = lf2

        # Right pane (main area / plots)
        self.right_pane = ttk.Frame(paned, padding=20)
        paned.add(self.right_pane, weight=65)

        # right_pane left empty for plots (will be added later)

        # map for later preset handling
        self.entries_by_table = {"table1": self.entries}

        # footer
        self.footer = ttk.Frame(self)
        self.footer.pack(fill="x", pady=(10, 0))



    def _build_table1(self, parent):
        # Use the LabelFrame (parent) directly as the container — no inner frame.
        # column spacing (simplified: index, label, value)
        parent.grid_columnconfigure(0, minsize=40, weight=0)
        # prevent the middle (label) column from absorbing extra space — keep it natural width
        parent.grid_columnconfigure(1, minsize=80, weight=0)
        parent.grid_columnconfigure(2, minsize=80, weight=1)

        # rows start at 0 (controls are outside lf1)
        for r, (idx, label_text) in enumerate(self.table1_labels, start=0):
            ttk.Label(parent, text=idx, font=("Arial", 12, "bold")).grid(
                row=r, column=0, padx=5, pady=4
            )

            ttk.Label(parent, text=label_text, font=("Arial", 12)).grid(
                row=r, column=1, padx=5, pady=4, sticky="w"
            )

            e = ttk.Entry(parent, justify="right", font=("Arial", 12), width=11)
            # align entries to the left of their column so they sit closer to labels
            e.grid(row=r, column=2, padx=5, pady=4, sticky="e")
            self.entries.append(e)


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



# def page1_table2(root):










