"""TableManager: Encapsulates all table-related operations for MyApp."""

import tkinter as tk
from tkinter import ttk
from utils.language import get_text, get_lan_text
from typing import Optional, Union, List

class TableManager:
    """Manages table building, refreshing, and variable linking for MyApp.
    
    Delegates strictly to controller for accessing state (pages, texts, language, etc).
    No independent state beyond the controller reference.
    """
    
    def __init__(self, controller):
        """Initialize TableManager with a reference to the MyApp controller.
        
        Args:
            controller: MyApp instance (for accessing pages, texts, current_language, etc.)
        """
        self.controller = controller
        self._registered_input_tables = set() # registry of tables whose inputs trigger recalculation

    # ===========================================================================
    # BUILDERS
    # ===========================================================================
    def build_table(self, parent, table_name: str):
        """Build a three cols table UI, 
           Row structure: index | label | entry
        
        Args:
            parent: The parent widget (LabelFrame) to add table rows to
            table_name: Name of the table (e.g., 'table1', 'table2')
        """
        table_texts = self.controller.table_texts.get(
            self.controller.current_page.get(), {}
        ).get(table_name, {})
        
        # Use the LabelFrame (parent) directly as the container — no inner frame.
        # column spacing (simplified: index, label, value)
        parent.grid_columnconfigure(0, minsize=40, weight=0)
        # prevent the middle (label) column from absorbing extra space — keep it natural width
        parent.grid_columnconfigure(1, minsize=80, weight=0)
        parent.grid_columnconfigure(2, minsize=80, weight=1)

        # rows start at 0 (controls are outside lf1)
        
        for r, field_key in enumerate(table_texts.keys(), start=0):
            self.controller.pages[self.controller.current_page.get()]["tables"][table_name]["keys"].append(field_key) # Store the field key from config
            label_text = get_text(field_key, table_texts, self.controller.current_language)
            
            # Row structure: index | label | entry
            table_index_font_bold = ("Arial", 12, "bold")
            table_label_font = ("Microsoft YaHei UI", 12, "normal")
            
            # create index label (1, 2, 3, ...)
            ttk.Label(parent, text=str(r + 1), font=table_index_font_bold).grid(
                row=r, column=0, padx=5, pady=4
            )
            # create field label
            row_label = ttk.Label(parent, text=label_text, font=table_label_font)
            row_label.grid(row=r, column=1, padx=5, pady=4, sticky="w")
            self.controller.pages[self.controller.current_page.get()]["tables"][table_name]["row_labels"].append(row_label)
            
            # create entry
            table_data = self.controller.pages[self.controller.current_page.get()]["tables"][table_name]
            entry_state = "readonly" if table_data["readonly"] else "normal"
            
            # ────────────────────────────────────────────────────────────────
            # StringVar for live tracing
            # ────────────────────────────────────────────────────────────────
            var = tk.StringVar()
            e = ttk.Entry(
                parent, 
                justify="right",  
                font=table_label_font, 
                width=11, 
                state=entry_state,
                textvariable=var
            )
            # align entries to the left of their column so they sit closer to labels
            e.grid(row=r, column=2, padx=5, pady=4, sticky="e")
            
            self.controller.pages[self.controller.current_page.get()]["tables"][table_name]["entries"].append(e)
            self.controller.pages[self.controller.current_page.get()]["tables"][table_name]["vars"].append(var)
            # ────────────────────────────────────────────────────────────────

    # ===========================================================================
    # REFRESH HELPERS
    # ===========================================================================
    def refresh_table_ui(self):
        self.refresh_table_titles()
        self.refresh_table_rows()

    def refresh_table_rows(self)-> None:
        """Refresh row labels for ALL tables on the current page when language changes.
        
        FULLY SCALABLE VERSION (same pattern as _refresh_table_titles):
        - No hardcoded "page1", "table1", or "table2"
        - No parameters needed
        - Automatically discovers every table from self.pages + self.table_texts
        - When you add table3, table4, page2, etc. → nothing to change here
        """
        current_page = self.controller.current_page.get()

        # Loop over every table that exists on this page (table1, table2, table3...)
        for table_name, table_data in self.controller.pages[current_page]["tables"].items():

            # Get the correct row label texts for this specific table
            # e.g. self.table_texts["page1"]["table1"] or ["page1"]["table2"]
            table_texts = self.controller.table_texts.get(current_page, {}).get(table_name, {})

            keys        = table_data.get("keys", [])
            row_labels  = table_data.get("row_labels", [])

            # Update each row label using the same logic as your old _refresh_table1_rows
            for r, field_key in enumerate(keys):
                if r < len(row_labels):                                   # safety check
                    label_text = get_text(field_key, table_texts, self.controller.current_language)    # uses module get_text function
                    row_labels[r].config(text=label_text)
                
    def refresh_table_titles(self)-> None:
        """Refresh table titles when language changes.
        """
        current_page = self.controller.current_page.get()
        current_lang = self.controller.current_language.get()

        # Loop over every table that exists on this page (e.g. "table1", "table2", "table3"...)
        # Use pages directly instead of current_presets to ensure all tables are refreshed
        for table_name, table_data in self.controller.pages[current_page]["tables"].items():

            # Get the title config for this table from title_texts
            # Example structure: self.title_texts["page1"]["table1"]
            title_config = self.controller.title_texts.get(current_page, {}).get(table_name, {})

            # Get the translated title text
            title_text = get_lan_text(title_config, current_lang)

            # Update the label widget (safe check in case title_label is missing)
            title_label = table_data.get("title_label")
            if title_label:
                title_label.config(text=title_text)

    # ===========================================================================
    # HELPERS
    # ===========================================================================
    def get_table(self, page: str, table: str) -> dict:
        """Helper method to safely access table data from self.pages.
        
        Args:
            page: Page name (e.g., 'page1')
            table: Table name (e.g., 'table1', 'table2')
            
        Returns:
            Dictionary containing table data (entries, keys, row_labels, title_label)
        """
        return self.controller.pages.get(page, {}).get("tables", {}).get(table, {})

    def clear_inputs(self, page: Optional[str] = None) -> None:
        """Clear all input fields (StringVars) on the given page, skipping readonly tables.
        
        This method clears all editable entry variables on a page, which will
        update the corresponding Entry widgets via textvariable binding.
        Readonly tables are skipped.
        
        Args:
            page: Page name (e.g., 'page1'). If None, uses current_page.
        """
        if page is None:
            page = self.controller.current_page.get()

        if page not in self.controller.pages:
            return
        
        # clear all entries for all tables on the page
        page_tables = self.controller.pages[page]["tables"]
        for table_data in page_tables.values():
            # Skip readonly tables
            # if table_data.get("readonly", False):
            #     continue
            for var in table_data.get("vars", []):
                var.set("")

    def apply_validation_colors(
        self,
        page: str,
        input_table: str,
        validity_map: dict,
        invalid_color: str = "#cc0000",
        normal_color: str = "#000000",
    ) -> None:
        """Color input entry text by validation state.

        Args:
            page: Page name (e.g. "page1").
            input_table: Table name containing editable inputs.
            validity_map: Mapping {field_key: bool}; False turns the entry red.
            invalid_color: Foreground color for invalid values.
            normal_color: Foreground color for valid values.
        """
        table_data = self.controller.pages.get(page, {}).get("tables", {}).get(input_table, {})
        keys = table_data.get("keys", [])
        entries = table_data.get("entries", [])

        for index, key in enumerate(keys):
            if index >= len(entries): # check to prevent index error if keys and entries are mismatched
                continue
            is_valid = validity_map.get(key, True) # default to True if key is missing from validity_map
            entries[index].configure(foreground=normal_color if is_valid else invalid_color) # set text color based on validity

    def apply_text_error_colors(
        self,
        page: str,
        table: str,
        error_text: str = "ERROR",
        error_color: str = "#cc0000",
        normal_color: str = "#000000",
    ) -> None:
        """Color output entry text red when the displayed value equals error_text.

        Args:
            page: Page name (e.g. "page1").
            table: Table name to scan (e.g. "table2").
            error_text: String value that marks a failed calculation.
            error_color: Foreground color applied when entry shows error_text.
            normal_color: Foreground color applied otherwise.
        """
        table_data = self.controller.pages.get(page, {}).get("tables", {}).get(table, {})
        entries = table_data.get("entries", [])
        vars_list = table_data.get("vars", [])

        for i, entry in enumerate(entries):
            value = vars_list[i].get() if i < len(vars_list) else ""
            entry.configure(foreground=error_color if value == error_text else normal_color)

    # ===========================================================================
    # CALCULATION HELPERS
    # ===========================================================================
    def link_table_vars(self, page:str, input_table:str, callback):
        """Link all StringVars of a table to a callback AND register the table.

        The trace itself does NOT define how inputs map to outputs. It only acts
        as a trigger that notifies the application that an input value has changed.
        The callback function (e.g. `_recalculate`) is responsible for:
            - Reading the input values
            - Determining how inputs map to outputs
            - Performing calculations
            - Updating the output tables or plots

        Args:
            page (str):
                The page name containing the table. e.g. "page1".
            table (str):
                The table name whose Entry variables should trigger the callback
                (e.g. "table1"). This table is automatically registered in 
                self._registered_input_tables for use by update_tables_from_inputs.

            callback (callable):
                The function to execute whenever any Entry value in the table
                changes. Typically this is a recalculation handler such as
                `_recalculate_page1`.
        Note: link one table at a time, use loop if linking multiple tables. e.g, for tbl in ["table1", "table2"]: link_table_vars(tbl, callback) 
        
        self.pages
        └── page1
                └── tables
                    └── table1
                        └── vars
                            ├── StringVar()  ← row 1
                            ├── StringVar()  ← row 2
                            ├── StringVar()  ← row 3
                            └── ...    
        """
    
        vars_list    = self.controller.pages[page]["tables"][input_table]["vars"]
  
        # Register this table as an input table for recalculation
        self._registered_input_tables.add(input_table)
        
        for var in vars_list:
            var.trace_add("write", callback)

    def read_table_inputs(self, page:str, input_table:str)-> dict:
        """Read numeric inputs from a table's Entry fields.

        Args:
            page (str):
                The page name containing the table.
            table (str):
                The table name whose Entry values should be read
                (e.g. "table1").

        Returns:
            dict:
                A dictionary mapping table field keys to numeric values.
                Example:
                    {
                        "distance": 12.5,
                        "time": None
                    }

                Keys correspond to the table's internal field identifiers
                stored in `self.controller.pages[current_page]["tables"][table]["keys"]`.
        """       
        keys         = self.controller.pages[page]["tables"][input_table]["keys"]
        vars_list    = self.controller.pages[page]["tables"][input_table]["vars"]
        
        data = {}

        for i, key in enumerate(keys):
            value = vars_list[i].get()

            try:
                data[key] = float(value)
            except ValueError:
                data[key] = None

        return data
    
    def write_table_outputs(self, page:str, output_table:str, data: dict) -> None:
        """Write display values to a table's Entry fields.

        Args:
            page (str):
                The page name containing the table.
            table (str):
                Target table whose Entry values should be updated
                (e.g. "table2").

            data (dict): 
                Mapping of field keys to calculated values.
                Example:
                    {
                        "speed": 4.5
                    }

        Notes:
            - Only keys present in the target table are updated.
            - Missing keys are ignored.
            - None values are written as blank entries.
            - Values are written only if they differ from the current Entry value
            to avoid unnecessary trace callbacks.
        """

        keys         = self.controller.pages[page]["tables"][output_table]["keys"]
        vars_list    = self.controller.pages[page]["tables"][output_table]["vars"]

        for i, key in enumerate(keys):

            value = data.get(key) # read display value
            
            # Always update if key exists in keys (the table definition).
            # If key is missing from data, it means validation failed → set to empty string
            current_value = vars_list[i].get()
            new_value     = "" if value is None else str(value) # convert to string for Entry widget, None becomes blank
            
            # Only update if value has changed to prevent unnecessary trace callbacks
            if current_value != new_value or value is None: 
                vars_list[i].set(new_value)

    def update_tables_from_inputs(
                        self,
                        page: Optional[str],
                        output_tables: Union[str, List[str]],
                        compute_method,
                    ) -> dict:
            """
                Generic recalculation method for any page/table.

                - Reads all inputs from tables registered via link_table_vars().
                - Passes inputs to the provided compute_method.
                - Writes outputs to specified output tables.

                Args:
                    page (str, optional): Page name; defaults to current_page.
                    output_tables (str or List[str]): Output table name(s). e.g. "table2" or ["table2"]
                    compute_method (callable): Function(page: str, inputs: dict) -> dict
                        Must return a dict of dicts: { "table2": {"field_key": value, ...}, ... }
                
                Note:
                    Input tables are automatically determined from self._registered_input_tables,
                    which is populated by link_table_vars().
            """
            if page is None: 
                page = self.controller.current_page.get()
                
            input_tables = self._registered_input_tables
            if isinstance(output_tables, str):
                output_tables = [output_tables]

            # Gather all inputs from all registered input tables into a single dict of dicts: { "table1": {"field_key": value, ...}, "tableX": {...}, ... }
            
            all_inputs_data = {}
            for tbl_name in input_tables:
                all_inputs_data[tbl_name] = self.read_table_inputs(page, tbl_name)

            # Pure computation
            all_outputs_data = compute_method(page, all_inputs_data) # compute_method must return a dict of dicts: { "table2": {"field_key": value, ...}, ... }

            # Write outputs one by one (with safety)
            for tbl_name in output_tables:
                output_data = all_outputs_data.get(tbl_name, {})
                self.write_table_outputs(page, tbl_name, output_data)   

            return all_outputs_data