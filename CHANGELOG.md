# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Added dedicated Reset button in the footer (clears all pages globally)



## [1.4] - 2026-03-18

### Added
- Embedded Matplotlib velocity-time preview plot in right pane (Page1Plot widget)
- Language-aware text system for plot (title, labels, error messages support ZH/EN)
- `_get_plot_text()` method in Page1Plot for retrieving language-specific plot text from config
- `FONTNAME` constant for CJK and Latin character support in plot widget
- `_refresh_axes_labels()` method to update plot labels when language changes
- `plot_texts` configuration in config.py with language-aware plot labels and error messages
- Initial 150ms startup delay (`_init_resize()`) to ensure container dimensions are measured before plot sizing
- Manual resize trigger in data update path (`_canvas_resize()` in `_plot_data()`)

### Changed
- Refactored plot architecture: Page1Plot now receives `app` instance via constructor for accessing shared state
- Modified `my_app.py` to pass app reference to Page1Plot (enables language/config access)
- Updated `page1.py` to pass app instance when instantiating Page1Plot
- Fixed Y-axis label cropping: added manual `_canvas_resize()` call in `_plot_data()` before `tight_layout()`
- Simplified font handling in `page1_plot.py`: replaced `FontProperties(fname=...)` approach with direct `fontname="Microsoft YaHei"` parameter
- Plot now triggers `_refresh_axes_labels()` in `update_plot()` to handle language changes dynamically
- Error messages in plot now read from config (no_input_error_message, invalid_input_error_message)

### Removed
- Removed unnecessary imports (`font_manager`, `FontProperties`) from `page1_plot.py` 
- Removed `_FONT_PROP` global variable (replaced with simple FONTNAME constant)
- Removed event-driven-only resize limitation (plot now manually resizes on data update)


## [1.3.2] - 2026-03-09


### Added
- self.pages now specify if a table is readonly, and if so, such tables are bypassed when apply_preset, clear_page are called

### Changed
- Separated page1 UI logic into a dedicated `Pages/page1.py` file with `Page1` class for better modularity
- Updated `my_app.py` to import and instantiate `Page1` instead of building layout directly

### Removed



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
 

      