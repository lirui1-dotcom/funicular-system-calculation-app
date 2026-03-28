import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional

import menu_bar
from menu_bar import MenuBar

import config
from config import table_texts, presets_texts, title_texts, presets, default_language, menu_texts, default_page

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
        self.current_page = tk.StringVar(value=default_page)  
        self.selected = tk.StringVar()
  
        # Note: For each ttk Label, there are 2 variables: 1. field keys(to know which text to pull from config), 
        # 2. the actual Label widget (to call .config(text=...) on it)
    
        self.pages = {}
        self.pages["page1"] = {
            "tables": {
                "table1": {"keys": [],         # field keys to know which text to pull from config for each row (for refresh)
                           "entries": [],      # Entry widgets for table 1 (for data retrieval and preset application)
                           "row_labels": [],   # Row label widgets for refresh
                           "title_label": None # Label widget for table 1 title (for refresh)
                       },
                "table2": {"keys": [], "entries": [], "row_labels": [], "title_label": None}
            }       
        }

        # ── 2. Data / configuration ─────────────────────────────────────────────
        # Texts for UI labels (menus, table titles, row labels, dropdown)
        self.table_texts = table_texts
        self.presets_texts = presets_texts
        self.menu_texts = menu_texts 
        self.title_texts = title_texts

        #self.p1_table1_texts = self.table_texts.get("page1", {}).get("table1", {})
        
        # Get presets and create mapping
        self.get_current_presets()
     
        # Set default selected value after presets_texts is available
        self.selected.set(self.get_text("default_option", self.presets_texts)) 
        
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

        # ── Controls row (preset dropdown) ─────────────────────────────────────────────────────
        controls = ttk.Frame(self.left_pane)
        controls.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        controls.grid_columnconfigure(0, weight=1)

        right_container = ttk.Frame(controls)
        right_container.grid(row=0, column=1, sticky="e")

        # Preset label (left of dropdown)
        preset_label_text = self.get_text("label_text", self.presets_texts)
        self.preset_label = ttk.Label(right_container, text=preset_label_text + ":", font=("Arial", 10))
        self.preset_label.pack(side="left", padx=(0, 8))

        # Preset dropdown
        default_mode_text = self.get_text("default_option", self.presets_texts)
        preset_display_texts = [default_mode_text] + self.preset_mapping("table1") # e.g. ["Manual Input", "Beijing"] 
        
        self.preset_combo = ttk.Combobox(
            right_container,
            values=preset_display_texts, # loads the options
            textvariable=self.selected,
            state="readonly",
            font=("Arial", 9),
            width=10,
            style="option_menu.TCombobox"
        )
        self.preset_combo.pack(side="left")
        self.preset_combo.bind("<<ComboboxSelected>>", self.apply_preset)
        # Set default value
        self.preset_combo.set(default_mode_text)

        # ── Table 1 ────────────────────────────────────────────────────────────────────────────
        title1_text = self.get_lan_text(
            self.title_texts.get("page1", {}).get("table1", {}),
            self.current_language.get()
        )
        title1_label = ttk.Label(
            self.left_pane,
            text=title1_text,
            font=('Segoe UI', 16, 'bold')
        )
        self.pages["page1"]["tables"]["table1"]["title_label"] = title1_label
        lf1 = ttk.LabelFrame(self.left_pane, labelwidget=title1_label, padding=10)
        lf1.grid(row=1, column=0, sticky="nsew")

        # Build table 1 content inside the labelframe
        self._build_table(lf1, "table1")

        # ── Table 2 ────────────────────────────────────────────────────────────────────────────
        title2_text = self.get_lan_text(
            self.title_texts.get("page1", {}).get("table2", {}),
            self.current_language.get()
        )
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


    def _build_table(self, parent,table_name: str):

        table_texts = self.table_texts.get(
        self.current_page.get(), {}
         ).get(table_name, {})
        
        # Use the LabelFrame (parent) directly as the container — no inner frame.
        # column spacing (simplified: index, label, value)
        parent.grid_columnconfigure(0, minsize=40, weight=0)
        # prevent the middle (label) column from absorbing extra space — keep it natural width
        parent.grid_columnconfigure(1, minsize=80, weight=0)
        parent.grid_columnconfigure(2, minsize=80, weight=1)

        # rows start at 0 (controls are outside lf1)
        
        for r, field_key in enumerate(table_texts.keys(), start=0):
            self.pages[self.current_page.get()]["tables"][table_name]["keys"].append(field_key) # Store the field key from config
            label_text = self.get_text(field_key, table_texts)
            
            # Row structure: index | label | entry
            # create index label (1, 2, 3, ...)
            ttk.Label(parent, text=str(r + 1), font=("Arial", 12, "bold")).grid(
                row=r, column=0, padx=5, pady=4
            )
             # create field label
            row_label = ttk.Label(parent, text=label_text, font=("Arial", 12))
            row_label.grid(row=r, column=1, padx=5, pady=4, sticky="w")
            self.pages[self.current_page.get()]["tables"][table_name]["row_labels"].append(row_label)
            # create entry
            e = ttk.Entry(parent, justify="right", font=("Arial", 12), width=11)
            # align entries to the left of their column so they sit closer to labels
            e.grid(row=r, column=2, padx=5, pady=4, sticky="e")
            self.pages[self.current_page.get()]["tables"][table_name]["entries"].append(e)


    # ===========================================================================
    # REFRESH HELPERS
    # ===========================================================================
    def refresh_ui(self):
        """Refresh all UI labels when language changes"""
        current_page = self.current_page.get()
        self._update_window_title()
        # Update menu will automatically refresh since it rebuilds based on current_language
        if hasattr(self, 'menu_bar'):
            self.master.config(menu=None)
            self._build_menu()
        # Update controls
        self._refresh_preset_dropdown() # refresh dropdown options and label text
        # Update tables
        self._refresh_table_titles()
        self._refresh_table_rows()

    # update main window title based on current language
    def _update_window_title(self): 
        """Update window title based on current language"""
        title = self.get_text("main_title", self.title_texts) 
        self.parent.title(  title)

    def _refresh_preset_dropdown(self):
        """Refresh control labels when language changes"""
        # Update label text
        preset_label_text = self.get_text("label_text", self.presets_texts)
        self.preset_label.config(text=preset_label_text + ":")
        
        # Refresh dropdown values to use translated preset labels
        default_mode_text = self.get_text("default_option", self.presets_texts)
        preset_display_values = [default_mode_text] + self.preset_mapping("table1")
        
        self.preset_combo['values'] = preset_display_values
        
        # ── Fix: re-validate current selection ───────────────────────────────
        current = self.selected.get()
        
        if current in preset_display_values:
            # still valid → just keep it (already shown correctly)
            self.preset_combo.set(current)
        else:
            # old selection no longer exists → reset to default
            self.preset_combo.set(default_mode_text)
            self.selected.set(default_mode_text)   # also sync the var
            
    def _refresh_table_rows(self):
        """Refresh row labels for ALL tables on the current page when language changes.
        
        FULLY SCALABLE VERSION (same pattern as _refresh_table_titles and _refresh_preset_dropdown):
        - No hardcoded "page1", "table1", or "table2"
        - No parameters needed (current_page, table_name, texts_dict)
        - Automatically discovers every table from self.pages + self.table_texts
        - When you add table3, table4, page2, etc. → nothing to change here
        """
        current_page = self.current_page.get()

        # Loop over every table that exists on this page (table1, table2, table3...)
        for table_name, table_data in self.pages[current_page]["tables"].items():

            # Get the correct row label texts for this specific table
            # e.g. self.table_texts["page1"]["table1"] or ["page1"]["table2"]
            table_texts = self.table_texts.get(current_page, {}).get(table_name, {})

            keys        = table_data.get("keys", [])
            row_labels  = table_data.get("row_labels", [])

            # Update each row label using the same logic as your old _refresh_table1_rows
            for r, field_key in enumerate(keys):
                if r < len(row_labels):                                   # safety check
                    label_text = self.get_text(field_key, table_texts)    # uses your existing get_text()
                    row_labels[r].config(text=label_text)
                
    def _refresh_table_titles(self):
        """Refresh table titles when language changes.
        """
        current_page = self.current_page.get()
        current_lang = self.current_language.get()

        # Loop over every table that exists on this page (e.g. "table1", "table2", "table3"...)
        # We use self.current_presets.keys() because get_current_presets() already loaded
        # exactly the tables that belong to the current page
        for table_name in self.current_presets.keys():

            # Reuse your existing helper (exactly like in your original code)
            table_data = self._get_table(current_page, table_name)

            # Get the title config for this table from title_texts
            # Example structure: self.title_texts["page1"]["table1"]
            title_config = self.title_texts.get(current_page, {}).get(table_name, {})

            # Get the translated title text
            title_text = self.get_lan_text(title_config, current_lang)

            # Update the label widget (safe check in case title_label is missing)
            title_label = table_data.get("title_label")
            if title_label:
                title_label.config(text=title_text)

    # ===========================================================================
    # ACTIONS
    # ===========================================================================
    def clear_page(self, page_key: Optional[str] = None) -> None:
        # in python 3.10+ we can use clear_page(self, page_key: str | None = None) -> None:
        """Clears all input fields on the given page (or current page if None)."""
        if page_key is None:
            page_key = self.current_page.get()

        if page_key not in self.pages: 
            return
        # clear all entries for all tables on current page
        page_tables = self.pages[page_key]["tables"]
        for table_data in page_tables.values():
            for entry in table_data.get("entries", []):
                entry.delete(0, tk.END) 

    def apply_preset(self, event=None):
        """Apply selected preset to all available tables on current page."""
        current_selected = self.selected.get()

        reset_text = self.get_text("default_option", self.presets_texts)
        if current_selected == reset_text or current_selected == "":
            self.clear_page() # clear all fields if "Reset" is selected
            return

        self.clear_page() # clear unwanted inputs before applying preset values

        # Apply presets to all tables on this page
        for table_name, table_presets in self.current_presets.items():  # e.g. self.current_presets = {"table1": {"opt1": {"texts": {...}, "data": {...}}}}
            # Find preset key by label
            preset_key = self.preset_dict_to_keys.get(table_name, {}).get(current_selected) # e.g. preset_key = preset_dict_to_keys["table1"].get("Beijing") → "opt1" 
            if preset_key:
                preset_data = table_presets.get(preset_key, {}).get("data", {}) # e.g. preset_data = {"total_distance":...} 
                if preset_data:
                    self._apply_preset_to_table(table_name, preset_data)


    def _apply_preset_to_table(self, table_name: str, preset_data: dict) -> None:
        """Apply preset data to a specific table by populating its entries.
        
        Args:
            table_name: Name of the table (e.g., 'table1', 'table2')
            preset_data: Dictionary mapping field keys to preset values
        """
        current_page = self.current_page.get()
        table_data = self._get_table(current_page, table_name)
        
        entries = table_data.get("entries", [])
        field_keys = table_data.get("keys", [])
        
        # Use zip to iterate through entries and their corresponding field keys
        for entry, field_key in zip(entries, field_keys):
            if field_key in preset_data:
                entry.insert(0, preset_data[field_key])

    # ===========================================================================
    # HELPERS / UTILITIES
    # ===========================================================================
    def get_text(self, key, label_dict):
        """
        Get label in the currently selected language from the given dictionary.
        Falls back to default_language if missing.
        Last resort: returns the key itself.
        
        Args:
            key (str): The key to look up (e.g. "main_title", "label_text")
            label_dict (dict): Dictionary of translations, usually structured as
                            {key: {lang_code: translated_text, ...}}
                            Example: {"main_title": {"ZH": "北京", "EN": "Beijing"}}
        
        Returns:
            str: The translated text, or fallback/default, or the key itself if not found.
        
        Example:         
            current_language = "EN" → returns "Beijing"
            current_language = "ZH" → returns "北京"
            current_language = "FR" → returns "Beijing" (fallback to EN/default)
            key not found → returns "main_title" (the key itself)
        """
        lang = self.current_language.get()
        entry = label_dict.get(key, {})
        return entry.get(lang) or entry.get(default_language) or key

    def get_lan_text(self, label_dict, language):
        """
        Retrieve text from a language dictionary for the specified language.

        Falls back to default_language if the requested language is missing.
        Returns an empty string if no suitable translation is found.

        Args:
            label_dict (dict): Dictionary mapping language codes to translated strings.
                            Example: {"ZH": "北京", "EN": "Beijing", "FR": "Pékin"}
            language (str): The language code to look up (e.g. "EN", "ZH").

        Returns: 
            str: The translated text in the requested language, or fallback to
                default_language, or empty string if nothing is found.

        Examples:
            get_lan_text(label_dict, "EN")   →  "Beijing"
            get_lan_text(label_dict, "ZH")   →  "北京"
            get_lan_text(label_dict, "FR")   →  "Beijing"  (fallback to default_language)
            get_lan_text({}, "EN")           →  ""         (empty dict → empty string)
            get_lan_text({"EN": "Hello"}, "ZH") → "Hello"  (missing ZH → fallback)
        """
        return label_dict.get(language) or label_dict.get(default_language) or ""
        
    def preset_mapping(self, table_key):
        """
        Create a mapping of preset display names (translated labels) to their internal preset keys
        for the specified table, and return the list of display names for use in the dropdown.

        This method:
        - Builds a per-table mapping: display_name → preset_key
        - Adds flat entries (display_name → preset_key) to self.preset_dict_to_keys
        - Stores the full per-table mapping under self.preset_dict_to_keys[table_key]

        Args:
            table_key (str): The name of the table (e.g. "table1", "table2") whose presets
                            should be mapped.

        Returns:
            list[str]: Sorted list of translated preset display names (e.g. ["Beijing", "Shanghai"])
                    to populate the Combobox values.

        Example:
            If self.current_presets["table1"] contains:
                {"opt1": {"texts": {"EN": "Beijing", "ZH": "北京"}, "data": {...}}}
            Then after calling preset_mapping("table1") with current_language="EN":
                Returns: ["Beijing"]
                self.preset_dict_to_keys = { "table1": {"Beijing": "opt1"}}
        """

        # Create mapping: preset label text -> preset key for lookup
        if not hasattr(self, 'preset_dict_to_keys'):
            self.preset_dict_to_keys = {}      # only create once
            
        mapping = {}
        current_lang = self.current_language.get()

        for preset_key, preset_info in self.current_presets[table_key].items():
            # label_text = the human-readable name shown in the dropdown
            # Example: if current_lang = "EN" → label_text = "Beijing"
            #          if current_lang = "ZH" → label_text = "北京"
            #          if missing translation → label_text = "" (empty string)
            label_text = self.get_lan_text( 
                preset_info.get("texts", {}),               # retrieve the dict of language or empty dict if missing
                current_lang                                # get current language key (e.g. "EN")
            )
            if label_text:                                  # ← checks if the string is "truthy"
                mapping[label_text] = preset_key            # e.g. {"Beijing": "opt1"}
                self.preset_dict_to_keys[label_text] = preset_key
        self.preset_dict_to_keys[table_key] = mapping           # e.g. preset_dict_to_keys["table1"] = {"Beijing": "opt1"}

        return list(mapping.keys()) # e.g. returns:["Beijing"]
        
    
    def get_current_presets(self): # only loads presets from tables store inputs
        """Reload presets for ALL tables on the current page"""
        current_page = self.current_page.get() 
        page_data = presets.get(current_page, {}) # e.g. presets.get("page1", {}) = {"table1": {"opt1": {"texts": {...}, "data": {...}}}}
        
        # Clear old presets
        self.current_presets = {}
        
        # Loop over whatever tables exist in config for this page
        for table_name, table_presets in page_data.items(): # e.g. table_name = "table1", table_presets = {"opt1": {"texts": {...}, "data": {...}}}
            self.current_presets[table_name] = table_presets # e.g. current_presets["table1"] = {"opt1": {"texts": {...}, "data": {...}}}
            
            # Rebuild mapping for this table
            self.preset_mapping(table_name)  # e.g. preset_mapping("table1") → builds mapping for table1 = {"Beijing": "opt1"}

    def _get_table(self, page: str, table: str) -> dict:
        """Helper method to safely access table data(from self.pages).
        
        Args:
            page: Page name (e.g., 'page1')
            table: Table name (e.g., 'table1', 'table2')
            
        Returns:
            Dictionary containing table data (entries, keys, row_labels, title_label)
        """
        return self.pages.get(page, {}).get("tables", {}).get(table, {})
    # ===========================================================================
    # GETTERS / SETTERS
    # ===========================================================================

# def page1_table2(root):










