# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Added dedicated Reset button in the footer (clears all pages globally)

## [1.3.1] - 2026-02-26

### Added
- Reset action in menu bar: Edit → Reset All Pages
- preset_mapping: auto mapping, e.g. returns:["Beijing","Shanghai"]
- get_current_presets: auto loads presets
- _get_table: Helper method to safely access table data.

### Changed
- Redesigned preset selection:
  - Removed mode bar / mode selector
  - Replaced it with a visible Preset dropdown in the header

- Refactored text configuration(config.py):
  - Replaced `p1_text_titles`, `p1_table1_texts` etc. with nested dictionaries accessed via `text_titles["page1"]` (and similar for other categories)
  - Improved scalability for multi-page support

- Renamed get_text_from_dict to get_lan_text

- apply_preset now auto apply presets
  FULLY SCALABLE VERSION (same pattern as apply_preset + get_current_presets):
    - No hardcoding of "page1", "table1", or "table2"
    - Automatically refreshes **every table** on the current page
    - When you add table3, table4, etc. → nothing to change here

- 



### Fixed
- **Preset combobox shows stale text after language change**  
  **Problem**: When switching languages, the preset dropdown (ttk.Combobox) kept displaying the old-language preset name (e.g. "Beijing") even after the `values` list was correctly updated to the new language (e.g. ["请选择", "北京", "上海", "广州"]).  
  This happened because:

  - The refresh logic only reset the displayed value when `self.selected.get() == ""`  
  - After a user selects any real preset, `self.selected.get()` is never empty again  
  - ttk.Combobox does **not** automatically clear/invalidate the displayed text when the new `values` list no longer contains the old selected string  
  - Result: visually stuck on old-language text until user manually re-selects something

  **Example sequence that reproduced the bug**:
  1. App starts in English: options = `["Please select", "Beijing", "Shanghai", "Guangzhou"]`
  2. User selects "Beijing" → `self.selected.get() == "Beijing"`
  3. User switches to Chinese → options updated to `["请选择", "北京", "上海", "广州"]`
  4. Refresh checks `if self.selected.get() == ""` → `"Beijing" != ""` → **no reset happens**
  5. Combobox still visually shows "Beijing" (invalid in new list)

  **Root cause**: Overly narrow condition `self.selected.get() == ""` only protected the initial/empty state, not the common case where a preset was already chosen.

  **Fixed by**: Replacing the narrow check with proper validation:
  - After updating `['values']`, check if the current selection still exists in the new list
  - If yes → keep it
  - If no → reset to the translated default option ("Please select" / "请选择" etc.)
  - Also sync `self.selected` variable to avoid future drift

  **Related code changed**:
  - `MyApp._refresh_preset_dropdown()`


### Removed




## [1.3.0] - 2026-02-26

### Added
- Pages in my_app to make it scalable

### Changed
- Reset action now clears **all pages** (global reset behavior across the entire application) 
- Some methods are now more generic not restricted to page 1

### Removed
- All hard-coded keys like "Reset" inside preset dropdown (cleaner separation of intents)
 

      