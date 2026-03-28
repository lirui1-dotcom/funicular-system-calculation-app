import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config import menu_texts, default_language, supported_languages

class MenuBar(tk.Menu):

    def __init__(self, parent: tk.Tk, controller=None): 
        super().__init__(parent, font=("Arial", 12), tearoff=0) # menu bar initialization
        self.parent = parent
        self.controller = controller  

        self.current_language = tk.StringVar(value=default_language)
        if controller and hasattr(controller, 'current_language'):
            self.current_language = controller.current_language

        self._build_menus()

    # ===========================================================================
    #  Build Menus
    # ===========================================================================
    def _build_menus(self):
        """Build all top-level menus here"""
        self._build_file_menu()
        # Edit menu
        self._build_edit_menu()
        # Language menu on the right
        self._build_language_menu()
    
    # ── file menu ────────────────────────────────────────────────────────
    def _build_file_menu(self):  
        file_menu = tk.Menu(self, tearoff=0, font=("Arial", 9))
        file_label = self.controller.get_text("file", menu_texts) 
        self.add_cascade(label=file_label, menu=file_menu)
        #drop down 1
        file_menu.add_command(
            label=self.controller.get_text("import_excel", menu_texts), 
            command=self.import_excel
            )
        #drop down 2
        file_menu.add_command(
            label=self.controller.get_text("export_excel", menu_texts), 
            command=self.export_excel
            )
        # ---- separator ----
        file_menu.add_separator()
        # drop down 3
        file_menu.add_command(label=self.controller.get_text("exit", menu_texts), command=self.parent.quit)   
    
    # ── edit menu ────────────────────────────────────────────────────────
    def _build_edit_menu(self):
        """Edit menu with Reset option"""
        edit_menu = tk.Menu(self, tearoff=0, font=("Arial", 9))
        edit_label = self.controller.get_text("edit", menu_texts)
        self.add_cascade(label=edit_label, menu=edit_menu)

        # Reset option
        reset_label = self.controller.get_text("reset", menu_texts)
        edit_menu.add_command(
            label=reset_label,           
            command=self._on_reset
        )

    # ── language menu ────────────────────────────────────────────────────────
    def _build_language_menu(self):
        """Build language selection menu on the right side"""
        lang_menu = tk.Menu(self, tearoff=0, font=("Arial", 9))
        lang_label = self.controller.get_text("language", menu_texts)
        self.add_cascade(label=lang_label, menu=lang_menu)
        
        for lang_code in supported_languages:
            lang_menu.add_radiobutton(
                label=lang_code,
                variable=self.current_language,
                value=lang_code,
                command=self._on_language_change
            )

    # ===========================================================================
    #  Action/Command methods 
    # ===========================================================================

    # ── file menu commands ────────────────────────────────────────────────────────
    def import_excel(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not path:
            return
        messagebox.showinfo("Import", f"Excel selected:\n{path}")
        # Hook point: pandas.read_excel(path)
        # If you have shared data in the main app:
        # if self.controller:
        #     self.controller.load_excel(path)

    def export_excel(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not path:
            return
        messagebox.showinfo("Export", f"Export to:\n{path}")
     
    # ── edit menu command ──────────────────────────────────────────────────────── 
    # Reset when called from menu
    def _on_reset(self):
        try:
            # Check whether controller exists and has the clear_page attribute/method
            if self.controller and hasattr(self.controller, 'clear_page'):
               self.controller.clear_page()
        except Exception: 
               # error handling can be added here
               pass

    # ── language menu command ────────────────────────────────────────────────────
    def _on_language_change(self):
        """Refresh UI when language changes"""
        try:
            if self.controller and hasattr(self.controller, 'refresh_ui'):
                self.controller.refresh_ui()
        except Exception:
            pass           


    # ===========================================================================
    #  Helpers
    # ===========================================================================
  
