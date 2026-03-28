import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional

import menu_bar
from menu_bar import MenuBar

import config
from config import p1_title_texts, p1_presets, p1_table1_texts, default_language, menu_texts, default_page

class MyApp(ttk.Frame): # root from main.py
    """OOP refactor of previous procedural page1_table1.

    - Encapsulates all widgets and state
    - Keeps the external function `page1_table1(root)` as a thin wrapper
      so existing call sites do not need changes
    - Makes it easier to add table2, presets, export, and testing
    """

    def __init__(self, parent: tk.Tk, *args, **kwargs): # root is parent here

        # initialization of the Frame (root from main.py -> parent here)--------------------------
        
        
        super().__init__(parent, padding=15, *args, **kwargs) # frame= ttk.Frame(root) in procedural version, now self = the frame itself, parent = root
        
        self.parent = parent
        
        # ── 1. State variables FIRST ────────────────────────────────────────────
        self.current_language = tk.StringVar(value=default_language)
        self.selected = tk.StringVar()
        self.current_page_key = default_page
        
        # Note: For each ttk Label, there are 2 variables: 1. field keys(to know which text to pull from config), 
        # 2. the actual Label widget (to call .config(text=...) on it)
    
        self.pages = {}
        self.pages["page1"] = {
            "tables": {
                "table1": {"keys": [],     # field keys to know which text to pull from config for each row (for refresh)
                       "entries": [],      # Entry widgets for table 1 (for data retrieval and preset application)
                       "row_labels": [],   # Row label widgets for refresh
                       "title_label": None # Label widget for table 1 title (for refresh)
                       },
                "table2": {"keys": [], "entries": [], "row_labels": [], "title_label": None}
            }       
        }

        # ── 2. Data / configuration ─────────────────────────────────────────────
        self.presets = p1_presets
        # Texts for UI labels (menus, table titles, row labels)
        self.p1_table1_texts = p1_table1_texts
        self.p1_title_texts = p1_title_texts
        self.menu_texts = menu_texts 
        
        # ── 3. Window setup (now safe to call methods) ──────────────────────────
        self._update_window_title()
        self.parent.minsize(600, 350)
        self.parent.configure(bg="#E4E2E2")
        self.parent.geometry("900x600")
        
        # ── 4. Style ────────────────────────────────────────────────────────────
        style = ttk.Style(self.parent)
        style.theme_use("vista")

        style.configure(
            "option_menu.TCombobox",
            fieldbackground="#E4E2E2",
            foreground="#000"
        )    
                                
        # ── 5. Build UI ─────────────────────────────────────────────────────────
        self._build_menu()
        self._build_layout()
        
        # Pack self last
        self.pack(fill="both", expand=True)  # Make this frame fill its parent

    # ===========================================================================
    # BUILDERS
    # ===========================================================================
    def _build_menu(self):
        # create MenuBar after state exists
        self.menu_bar = MenuBar(self.master, controller=self)
        self.master.config(menu=self.menu_bar)

    def _build_layout(self):
        """
        Main layout: horizontal paned window with left (tables) and right (plots/content) pane
        """
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

        # ── Root-level splitter ────────────────────────────────────────────────────────────────
        # Horizontal splitter: left pane for tables, right pane for main/plots
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        # ── LEFT PANE: Tables and controls ─────────────────────────────────────────────────────
        LEFT_PANE_WEIGHT = 20

        self.left_pane = ttk.Frame(paned, padding=12)
        paned.add(self.left_pane, weight=LEFT_PANE_WEIGHT)

        # Grid configuration inside left pane
        self.left_pane.grid_rowconfigure(0, weight=0)    # controls row
        self.left_pane.grid_rowconfigure(1, weight=0)    # table 1 (fixed height)
        self.left_pane.grid_rowconfigure(2, weight=1)    # table 2 (expands)
        self.left_pane.grid_columnconfigure(0, weight=1)

        # ── Table 1 ────────────────────────────────────────────────────────────────────────────
        title1_text = self.get_text("p1_table1", self.p1_title_texts)
        title1_label = ttk.Label(
            self.left_pane,
            text=title1_text,
            font=('Segoe UI', 16, 'bold')
        )
        self.pages["page1"]["tables"]["table1"]["title_label"] = title1_label
        lf1 = ttk.LabelFrame(self.left_pane, labelwidget=title1_label, padding=10)
        lf1.grid(row=1, column=0, sticky="nsew")

        # Build table 1 content inside the labelframe
        self._build_table1(lf1)

        # ── Table 2 ────────────────────────────────────────────────────────────────────────────
        title2_text = self.get_text("p1_table2", self.p1_title_texts)
        title2_label = ttk.Label(
            self.left_pane,
            text=title2_text,
            font=('Segoe UI', 14, 'bold')
        )
        self.pages["page1"]["tables"]["table2"]["title_label"] = title2_label
        lf2 = ttk.LabelFrame(self.left_pane, labelwidget=title2_label, padding=10)
        lf2.grid(row=2, column=0, sticky="nsew")
        self.table2_frame = lf2

        # ── RIGHT PANE: Main content / plots ───────────────────────────────────────────────────
        RIGHT_PANE_WEIGHT = 100 - LEFT_PANE_WEIGHT

        self.right_pane = ttk.Frame(paned, padding=20)
        paned.add(self.right_pane, weight=RIGHT_PANE_WEIGHT)

        # Right pane currently empty (plots/content will be added later)

        # ── Additional setup ───────────────────────────────────────────────────────────────────
        # Footer (full width, bottom)
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
        
        for r, field_key in enumerate(self.p1_table1_texts.keys(), start=0):
            self.pages["page1"]["tables"]["table1"]["keys"].append(field_key) # Store the field key from config
            label_text = self.get_text(field_key, self.p1_table1_texts)
            
            # Row structure: index | label | entry
            # create index label (1, 2, 3, ...)
            ttk.Label(parent, text=str(r + 1), font=("Arial", 12, "bold")).grid(
                row=r, column=0, padx=5, pady=4
            )
            # create field label
            row_label = ttk.Label(parent, text=label_text, font=("Arial", 12))
            row_label.grid(row=r, column=1, padx=5, pady=4, sticky="w")
            self.pages["page1"]["tables"]["table1"]["row_labels"].append(row_label)  # Store for refresh
            # create entry
            e = ttk.Entry(parent, justify="right", font=("Arial", 12), width=11)
            # align entries to the left of their column so they sit closer to labels
            e.grid(row=r, column=2, padx=5, pady=4, sticky="e")
            self.pages["page1"]["tables"]["table1"]["entries"].append(e)


    # ===========================================================================
    # REFRESH HELPERS
    # ===========================================================================
    def refresh_ui(self):
        """Refresh all UI labels when language changes"""
        self._update_window_title()
        # Update menu will automatically refresh since it rebuilds based on current_language
        if hasattr(self, 'menu_bar'):
            self.master.config(menu=None)
            self._build_menu()
        # Update tables
        self._refresh_table_titles()
        self._refresh_table1_rows()

    # update main window title based on current language
    def _update_window_title(self): 
        """Update window title based on current language"""
        title = self.get_text("p1_main_title", self.p1_title_texts) 
        self.parent.title(title)

    def _refresh_table1_rows(self):
        """Refresh table1 row labels when language changes"""
        for r, field_key in enumerate(self.pages["page1"]["tables"]["table1"]["keys"]):
            self.pages["page1"]["tables"]["table1"]["row_labels"][r].config(text=
                                            self.get_text(field_key, self.p1_table1_texts)
                                            )

    def _refresh_table_titles(self):
        """Refresh table titles when language changes"""
        self.pages["page1"]["tables"]["table1"]["title_label"].config(text=
                                       self.get_text("p1_table1", self.p1_title_texts)
                                       )
        self.pages["page1"]["tables"]["table2"]["title_label"].config(text=
                                       self.get_text("p1_table2", self.p1_title_texts)
                                       )


    # ===========================================================================
    # ACTIONS
    # ===========================================================================
    def clear_page(self, page_key: Optional[str] = None) -> None:
        # in python 3.10+ we can use clear_page(self, page_key: str | None = None) -> None:
        """Clears all input fields on the given page (or current page if None)."""
        if page_key is None:
            page_key = self.current_page_key

        if page_key not in self.pages:
            return

        for table in self.pages[page_key]["tables"].values():
            for entry in table.get("entries", []):
                entry.delete(0, tk.END)

    def apply_preset(self, event=None):
        name = self.selected.get()

        reset_text = self.get_text("default_mode", self.menu_texts)
        if name == reset_text or name == "":
            self.clear_page()
            return

        self.clear_page()

        table1_data = self.presets.get(name, {}).get("table1", {})
        for entry, field_key in zip(self.pages["page1"]["tables"]["table1"]["entries"], 
                                    self.pages["page1"]["tables"]["table1"]["keys"]):
            if field_key in table1_data:
                entry.insert(0, table1_data[field_key])


    # ===========================================================================
    # HELPERS / UTILITIES
    # ===========================================================================
    def get_text(self, key, label_dict):
        """
        Get label in the currently selected language from the given dictionary.
        Falls back to default_language if missing.
        Last resort: returns the key itself.
        """
        lang = self.current_language.get()
        entry = label_dict.get(key, {})
        return entry.get(lang) or entry.get(default_language) or key  # current lang -> default lang -> key


    # ===========================================================================
    # GETTERS / SETTERS
    # ===========================================================================
    def get_table1_values(self):
        return [e.get() for e in self.pages["page1"]["tables"]["table1"]["entries"]]

    def set_table1_values(self, values):
        for e, v in zip(self.pages["page1"]["tables"]["table1"]["entries"], values):
            e.delete(0, tk.END)
            e.insert(0, v)


# def page1_table2(root):










