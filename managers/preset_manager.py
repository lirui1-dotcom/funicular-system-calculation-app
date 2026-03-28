"""PresetManager: Encapsulates preset-related operations for MyApp."""

from core.config import * # import config dictions and variables (presets, presets_texts, etc.)
from utils.language import get_text, get_lan_text


class PresetManager:
    """Manages presets and preset UI for MyApp.
    
    Stores preset-specific state: current_presets, preset_dict_to_keys.
    Delegates strictly to controller for accessing MyApp state (pages, texts, language, etc).
    """
    
    def __init__(self, controller):
        """Initialize PresetManager with a reference to the MyApp controller.
        
        Args:
            controller: MyApp instance (for accessing pages, texts, current_language, etc.)
        """
        self.controller = controller
        
        # Preset state (lives here now, not in MyApp)
        self.current_presets = {}
        self.preset_dict_to_keys = {}

    def get_current_presets(self):
        """Reload presets for ALL tables on the current page"""
        current_page = self.controller.current_page.get() 
        page_data = presets.get(current_page, {}) # e.g. presets.get("page1", {}) = {"table1": {"opt1": {"texts": {...}, "data": {...}}}}
        
        # Clear old presets
        self.current_presets = {}
        
        # Loop over whatever tables exist in config for this page
        for table_name, table_presets in page_data.items(): # e.g. table_name = "table1", table_presets = {"opt1": {"texts": {...}, "data": {...}}}
            self.current_presets[table_name] = table_presets # e.g. current_presets["table1"] = {"opt1": {"texts": {...}, "data": {...}}}
            
            # Rebuild mapping for this table
            self.preset_mapping(table_name)  # e.g. preset_mapping("table1") → builds mapping for table1 = {"Beijing": "opt1"}

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
        mapping = {}
        current_lang = self.controller.current_language.get()

        for preset_key, preset_info in self.current_presets[table_key].items():
            # label_text = the human-readable name shown in the dropdown
            # Example: if current_lang = "EN" → label_text = "Beijing"
            #          if current_lang = "ZH" → label_text = "北京"
            #          if missing translation → label_text = "" (empty string)
            label_text = get_lan_text( 
                preset_info.get("texts", {}),               # retrieve the dict of language or empty dict if missing
                current_lang                                # get current language key (e.g. "EN")
            )
            if label_text:                                  # ← checks if the string is "truthy"
                mapping[label_text] = preset_key            # e.g. {"Beijing": "opt1"}
                self.preset_dict_to_keys[label_text] = preset_key
        self.preset_dict_to_keys[table_key] = mapping           # e.g. preset_dict_to_keys["table1"] = {"Beijing": "opt1"}

        return list(mapping.keys()) # e.g. returns:["Beijing"]

    def apply_preset(self, event=None):
        """Apply selected preset to all available tables on current page."""
        current_selected = self.controller.selected.get()

        reset_text = get_text("default_option", self.controller.presets_texts, self.controller.current_language)
        if current_selected == reset_text or current_selected == "":
            self.controller.table_manager.clear_inputs()
            return

        self.controller.table_manager.clear_inputs() # clear unwanted inputs before applying preset values

        current_page = self.controller.current_page.get()
        # Apply presets to all tables on this page
        for table_name, table_presets in self.current_presets.items():  # e.g. self.current_presets = {"table1": {"opt1": {"texts": {...}, "data": {...}}}}
            # Skip readonly tables
            table_data = self.controller.table_manager.get_table(current_page, table_name)
            if table_data.get("readonly", False):
                continue
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
        current_page = self.controller.current_page.get()
        table_data = self.controller.table_manager.get_table(current_page, table_name)
        
        entries = table_data.get("entries", [])
        field_keys = table_data.get("keys", [])
        
        # Use zip to iterate through entries and their corresponding field keys
        for entry, field_key in zip(entries, field_keys):
            if field_key in preset_data:
                entry.insert(0, preset_data[field_key])

    def refresh_preset_dropdown(self):
        """Refresh control labels when language changes"""
        # Update label text
        preset_label_text = get_text("label_text", self.controller.presets_texts, self.controller.current_language)
        self.controller.preset_label.config(text=preset_label_text + ":")
        
        # Refresh dropdown values to use translated preset labels
        default_mode_text = get_text("default_option", self.controller.presets_texts, self.controller.current_language)
        preset_display_values = [default_mode_text] + self.preset_mapping("table1")
        
        self.controller.preset_combo['values'] = preset_display_values
        
        # ── Fix: re-validate current selection ───────────────────────────────
        current = self.controller.selected.get()
        
        if current in preset_display_values:
            # still valid → just keep it (already shown correctly)
            self.controller.preset_combo.set(current)
        else:
            # old selection no longer exists → reset to default
            self.controller.preset_combo.set(default_mode_text)
            self.controller.selected.set(default_mode_text)   # also sync the var
