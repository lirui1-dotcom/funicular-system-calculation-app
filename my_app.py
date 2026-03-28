import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional

from sympy import root, var

from menu_bar import MenuBar
from core import *
from pages import *
from managers import *
from utils import *


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
        
        # ── 0 DPI Detection (must come EARLY so fonts scale correctly) ────────────
        # Detect screen DPI: Windows defines 96 DPI = 100% scaling, 120 DPI = 125%, etc.
        # self.screen_dpi = parent.winfo_fpixels('1i')
        # self.dpi_scale = self.screen_dpi / 96.0  # normalized scaling factor
        
        # ── 1. State variables FIRST ────────────────────────────────────────────
        self.current_language = tk.StringVar(value=default_language)
        self.current_page = tk.StringVar(value=default_page)  
        self.selected = tk.StringVar()
        self.latest_plot_payload = None
  
        # Note: For each ttk Label, there are 2 variables: 1. field keys(to know which text to pull from config), 
        # 2. the actual Label widget (to call .config(text=...) on it)
    
        self.pages = {}
        self.pages["page1"] = {
            "tables": {
                "table1": {"keys": [],         # field keys to know which text to pull from config for each row (for refresh)
                           "entries": [],      # Entry widgets for table 1 (for data retrieval and preset application)
                           "vars" : [],         # StringVar for each entry (if needed for trace or easier access)
                           "row_labels": [],   # Row label widgets for refresh
                           "title_label": None, # Label widget for table 1 title (for refresh)
                           "readonly": False 
                       },
                "table2": {"keys": [], 
                           "entries": [], 
                           "vars": [], 
                           "row_labels": [],
                           "title_label": None, 
                            "readonly": True
                       },
            }       
        }

        # ── 2. Data / configuration ─────────────────────────────────────────────
        # Texts for UI labels (menus, table titles, row labels, dropdown)
        self.table_texts = table_texts
        self.presets_texts = presets_texts
        self.menu_texts = menu_texts 
        self.title_texts = title_texts
        self.plot_texts = plot_texts

        # ── 2.5 Managers ──────────────────────────────────────────────────────
        self.table_manager = TableManager(self)
        self.preset_manager = PresetManager(self)

        #self.p1_table1_texts = self.table_texts.get("page1", {}).get("table1", {})
        
        # Get presets and create mapping
        self.preset_manager.get_current_presets()
     
        # Set default selected value after presets_texts is available
        self.selected.set(get_text("default_option", self.presets_texts, self.current_language)) 
        
        # ── 3. Window setup (now safe to call methods) ──────────────────────────
        self._update_window_title()
        self.parent.minsize(600, 350)
        self.parent.configure(bg="#E4E2E2") 
        self.parent.geometry("1500x1020") # width x height
        
        # ── 4. Style ────────────────────────────────────────────────────────────
        style = ttk.Style(self.parent)
        style.theme_use("vista")
        #style.configure("Plot.TFrame", background="#E4E2E2")
        # style.configure(
        #     "option_menu.TCombobox",
        #     #fieldbackground="#E4E2E2", # controls the dropdown field background
        #     foreground="#000"
        # )    
        self.pack(fill="both", expand=True)  # Make this frame fill its parent                        
        # ── 5. Build UI ─────────────────────────────────────────────────────────
        self._build_menu() # menu bar 
        self.page1 = Page1(self) # build page 1
        self.parent.protocol("WM_DELETE_WINDOW", self._on_app_close)

        # ── 6. Data binding ───────────────────────────────────────────────────────
        self.link_input_to_output()  # link all inputs to outputs

    def _build_menu(self):
        # create MenuBar after state exists
        self.menu_bar = MenuBar(self.master, controller=self)
        self.master.config(menu=self.menu_bar)


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
        # Page-specific UI refresh (includes table and preset dropdown refresh)
        self.page1.refresh_p1_ui()

    # update main window title based on current language
    def _update_window_title(self): 
        """Update window title based on current language"""
        title = get_text("main_title", self.title_texts, self.current_language) 
        self.parent.title(title)

    def _on_app_close(self):
        if hasattr(self, "page1") and self.page1:
            self.page1.destroy()
        self.parent.destroy()

    # ===========================================================================
    # ACTIONS
    # ===========================================================================
    def apply_preset(self, event=None):
        """Delegate to preset_manager (for Page1 binding)."""
        self.preset_manager.apply_preset(event)

    def clear_page(self, page_key=None):
        """Clear all input fields on the given page, skipping readonly tables.
        
        Delegates to table_manager. Kept for backward compatibility.
        
        Args:
            page_key: Page name (e.g., 'page1'). If None, uses current_page.
        """
        self.table_manager.clear_inputs(page_key)

    # ===========================================================================
    # GETTERS / SETTERS
    # ===========================================================================

    def link_input_to_output(self):
        """Link all inputs to outputs."""
        current_page = self.current_page.get()
        if current_page == "page1":
            # link table1 inputs
            self.table_manager.link_table_vars(current_page, "table1", self._on_input_change)
     

    def _on_input_change(self, *args):
        """Callback when table inputs change - triggers recalculation."""
        current_page = self.current_page.get()
        if current_page == "page1":
            # 1) Read current table1 inputs and color invalid fields red
            table1_inputs = self.table_manager.read_table_inputs("page1", "table1")
            table1_validity = validate_input("page1", "table1", table1_inputs)
            self.table_manager.apply_validation_colors("page1", "table1", table1_validity)

            # 2) Compute and update output tables
            all_outputs = self.table_manager.update_tables_from_inputs(
                page="page1",
                output_tables="table2",
                compute_method=compute_outputs
            )

            # 2.5) Update right-pane preview plot from computation payload
            table1_vars = self.pages["page1"]["tables"]["table1"]["vars"] # get StringVar list for table1
            has_any_input = any(var.get().strip() for var in table1_vars)
            if not has_any_input:
                self.latest_plot_payload = None
                self.page1.plot.update_plot(None)
                return

            self.latest_plot_payload = (all_outputs or {}).get("plot1")
            self.page1.plot.update_plot(self.latest_plot_payload)
            
            # 3) Color output fields red if they are in error state (e.g., due to invalid inputs)
            self.table_manager.apply_text_error_colors("page1", "table2")

    # Alternative 
    # 
    # def _on_input_change(self, *args):
    #     """Callback when table inputs change - triggers recalculation."""
    #     try:
    #         current_page = self.current_page.get()
    #         if current_page == "page1":
    #             # Read input values from table1
    #             input_data = self.table_manager.read_table_inputs(current_page, "table1")
    #             # Compute outputs using the new signature
    #             output_data = compute_p1_table(current_page, input_data)
    #             # Write results to table2 if computation succeeded
    #             if output_data:
    #                 self.table_manager.write_table_outputs(current_page, "table2", output_data.get("table2", {}))
    #     except Exception as e:
    #         # Silently handle calculation errors
    #         pass
    