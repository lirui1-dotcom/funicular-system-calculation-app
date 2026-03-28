import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config import (menu_bar_labels)

# file menu labels
menu_lable_1 = menu_bar_labels["file_menu"]
file_dropdown_labels = [
    menu_bar_labels["import_excel"],
    menu_bar_labels["export_excel"],
    menu_bar_labels["exit"]
]
# mode menu labels
menu_lable_2 = menu_bar_labels["mode_menu"]
default_mode = menu_bar_labels["default_mode"]

class MenuBar(tk.Menu):
    
    def __init__(self, parent: tk.Tk, controller=None): 
        super().__init__(parent, font=("Arial", 12), tearoff=0) # menu bar initialization
        self.parent = parent
        self.controller = controller  # optional: main app instance for shared state

        self._build_menus()

    def _build_menus(self):
        """Build all top-level menus here"""
        self._build_file_menu()
        # Mode menu (moved from page controls)
        self._build_mode_menu()

    def _build_file_menu(self):  
        file_menu = tk.Menu(self, tearoff=0, font=("Arial", 9)) # file_menu = tk.Menu(...)  # dropdown items
        self.add_cascade(label=menu_lable_1, menu=file_menu)

        file_menu.add_command(label=file_dropdown_labels[0], command=self.import_excel)
        file_menu.add_command(label=file_dropdown_labels[1], command=self.export_excel)
        file_menu.add_separator() #---------
        file_menu.add_command(label=file_dropdown_labels[2], command=self.parent.quit)   

    def _build_mode_menu(self):
        """ When a mode is chosen we update the controller's selected StringVar
        and call its apply_preset() method if provided.
        """
        mode_menu = tk.Menu(self, tearoff=0, font=("Arial", 9))
        self.add_cascade(label=menu_lable_2, menu=mode_menu)

        # Use controller's StringVar if available, else create a local one
        var = None
        if self.controller and hasattr(self.controller, 'selected'):
            var = self.controller.selected
        else:
            var = tk.StringVar(value=default_mode)
        
        # first dropdown 
        mode_menu.add_radiobutton(
            label=default_mode,           
            variable=var,
            value=default_mode,
            command=self._on_mode_change
        )

        # second dropdown 
        if self.controller and hasattr(self.controller, 'presets'):
            for name in self.controller.presets.keys():
                mode_menu.add_radiobutton(
                    label=name, 
                    variable=var, 
                    value=name, 
                    command=self._on_mode_change
                )

    # ── Command methods ────────────────────────────────────────────────────────
    # These can be called directly or overridden in subclasses
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

    # ── helpers ────────────────────────────────────────────────────────
    # Apply presets when mode selected from menu
    def _on_mode_change(self):
        try:
            # Check whether controller exists and has the apply_preset attribute/method
            if self.controller and hasattr(self.controller, 'apply_preset'):
               self.controller.apply_preset()
        except Exception: 
               # error handling can be added here
               pass




