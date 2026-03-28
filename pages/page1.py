# pages/page1.py
"""
Page 1 specific UI builder (OOP version).

This class:
- Builds the entire UI for page1
- Registers all widgets into the shared self.pages registry in MyApp
- Delegates refresh to your existing scalable methods in MyApp
- Supports future page switching with .destroy()

No refresh logic is duplicated here — your _refresh_preset_dropdown(),
_refresh_table_titles(), and _refresh_table_rows() remain untouched.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

from utils.language import get_text, get_lan_text
from pages.page1_plot import Page1Plot


class Page1:
    """
    Create page 1 UI.

    OOP refactor of previous procedural version:
    - Encapsulates page-specific widget creation
    - Owns references for clean refresh and destruction
    - Keeps MyApp clean and focused on coordination
    """

    def __init__(self, app):
        """
        Args:
            app: The main MyApp instance (controller) — gives access to
                 shared state, configs, helpers, and the pages registry.
        """
        self.app = app # self.app is the self passed in from MyApp, which has all the shared state and methods we need
        self.preset_label: Optional[ttk.Label] = None
        self.preset_combo: Optional[ttk.Combobox] = None
        self.table_frames: dict = {}   # "table1": lf1, "table2": lf2, ...
        self.plot: Optional[Page1Plot] = None
        self._build()
        

    # ===========================================================================
    # BUILDERS (build page1 UI and register widgets in MyApp.pages for refresh)
    # ===========================================================================
    def _build(self):
        """
        Builds the entire page1 layout.
        This replaces the old _build_layout() method that was inside MyApp.
        """
        # ===============================================================
        # LAYOUT STRUCTURE (your original comment preserved)
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
        paned = ttk.PanedWindow(self.app, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        # ── LEFT PANE: Tables and controls ─────────────────────────────────────────────────────
        LEFT_PANE_WEIGHT = 20

        self.app.left_pane = ttk.Frame(paned, padding=12)
        paned.add(self.app.left_pane, weight=LEFT_PANE_WEIGHT)

        # Grid configuration inside left pane
        self.app.left_pane.grid_rowconfigure(0, weight=0)    # controls row (preset dropdown)
        self.app.left_pane.grid_rowconfigure(1, weight=0)    # table 1 (fixed height)
        self.app.left_pane.grid_rowconfigure(2, weight=1)    # table 2 (expands)
        self.app.left_pane.grid_columnconfigure(0, weight=1)  

        # ── Controls row (preset dropdown) ─────────────────────────────────────────────────────
        # ├─ control frame (grid row 0, expand)
        #     └─ preset_frame (holds preset label and dropdown)
        #          ├─ preset_label (pack)
        #          └─ preset_combo (pack)
        ctrl_frame = ttk.Frame(self.app.left_pane)
        ctrl_frame.grid(row=0, column=0, sticky="ew") # left_pane frame row 0, col 0, horizontal stretch, some bottom padding
        ctrl_frame.grid_columnconfigure(0, weight=1) # Column 0 = spacer that grows (this pushes everything to the right, so preset is right aligned)

        preset_frame = ttk.Frame(ctrl_frame)
        preset_frame.grid(row=0, column=1, sticky="e")

        # Preset label (left of dropdown)
        preset_label_text = get_text("label_text", self.app.presets_texts, self.app.current_language)
        self.preset_label = ttk.Label(preset_frame, text=preset_label_text + ":", font=("Arial", 9, "bold"))
        self.preset_label.pack(side="left", padx=(0, 8)) # a little padding to the right of the label--------------<- label pack

        # Store reference for preset_manager refresh
        self.app.preset_label = self.preset_label 

        # Preset dropdown
        default_mode_text = get_text("default_option", self.app.presets_texts, self.app.current_language)
        preset_display_texts = [default_mode_text] + self.app.preset_manager.preset_mapping("table1")

        self.preset_combo = ttk.Combobox(
            preset_frame,
            values=preset_display_texts,
            textvariable=self.app.selected,
            state="readonly",
            font=("Arial", 9),
            width=10,
            style="option_menu.TCombobox"
        )

        self.preset_combo.pack(side="left")# ------------------------------------------------<- dropdown pack

        self.preset_combo.bind("<<ComboboxSelected>>", self.app.apply_preset)
        self.preset_combo.set(default_mode_text)
        self.app.preset_combo = self.preset_combo   # for preset_manager refresh

        # ── Table 1 ────────────────────────────────────────────────────────────────────────────
        title1_text = get_lan_text(
            self.app.title_texts.get("page1", {}).get("table1", {}),
            self.app.current_language.get()
        )
        title1_label = ttk.Label(
            self.app.left_pane,
            text=title1_text,
            font=('Segoe UI', 16, 'bold')
        )
        self.app.pages["page1"]["tables"]["table1"]["title_label"] = title1_label # store reference for refresh
        left_pane_tab1_frame = ttk.LabelFrame(self.app.left_pane, labelwidget=title1_label, padding=10)
        left_pane_tab1_frame.grid(row=1, column=0, sticky="nsew") # row 1, col 0, stretch in all directions
        self.table_frames["table1"] = left_pane_tab1_frame

        self.app.table_manager.build_table(left_pane_tab1_frame, "table1") # build table 1 

        # – Table 2 ──────────────────────────────────────────────────────────────────────────────
        title2_text = get_lan_text(
            self.app.title_texts.get("page1", {}).get("table2", {}),
            self.app.current_language.get()
        )
        title2_label = ttk.Label(
            self.app.left_pane,
            text=title2_text,
            font=('Segoe UI', 14, 'bold')
        )
        self.app.pages["page1"]["tables"]["table2"]["title_label"] = title2_label # store reference for refresh
        left_pane_tab2_frame = ttk.LabelFrame(self.app.left_pane, labelwidget=title2_label, padding=10)
        left_pane_tab2_frame.grid(row=2, column=0, sticky="nsew")
        self.table_frames["table2"] = left_pane_tab2_frame
        self.app.table_manager.build_table(left_pane_tab2_frame, "table2") # build table 2

        # ── RIGHT PANE: Main content / plots ───────────────────────────────────────────────────
        RIGHT_PANE_WEIGHT = 100 - LEFT_PANE_WEIGHT

        # Keep pane padding symmetric so left/right top borders align.
        self.app.right_pane = ttk.Frame(paned, padding=12)
        paned.add(self.app.right_pane, weight=RIGHT_PANE_WEIGHT)
        self.plot = Page1Plot(self.app.right_pane, self.app) # pass app for access to shared state and methods, if needed
        
        # ── Footer ─────────────────────────────────────────────────────────────────────────────
        # self.app.footer = ttk.Frame(self.app)
        # self.app.footer.pack(fill="x", pady=(10, 0))

    # ===========================================================================
    # REFRESH METHODS (for page-specific UI refresh)
    # ===========================================================================
    def refresh_p1_ui(self):
        """
        Refresh all page1-specific UI elements (tables only).
        
        Preset refresh is handled by MyApp.refresh_ui() before calling this.
        No duplication — just table management.
        """
        self.app.table_manager.refresh_table_ui()
        self.app.preset_manager.refresh_preset_dropdown()
        if self.plot: # check if plot exists before trying to update it (it should, but just in case)
            self.plot.update_plot(getattr(self.app, "latest_plot_payload", None))

    # ===========================================================================
    # CLEANUP (for page switching)
    # ===========================================================================
    def destroy(self):
        """Clean up all widgets when switching away from this page."""
        if self.plot:
            self.plot.destroy()
            self.plot = None 

        if self.preset_label and self.preset_label.winfo_exists():
            self.preset_label.destroy()
        if self.preset_combo and self.preset_combo.winfo_exists():
            self.preset_combo.destroy()

        for frame in self.table_frames.values():
            if frame and frame.winfo_exists():
                frame.destroy()

        self.table_frames.clear()