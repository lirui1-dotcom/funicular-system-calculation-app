# 🚡 Funicular System Calculation App

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)]()
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

A modern, object-oriented Tkinter application for calculating operating parameters of passenger funicular railway systems. Built with clean OOP design, modular architecture, and full internationalization support (Chinese/English).

---

## ✨ Features

- 📊 **Interactive Tables** — Real-time data input with live calculation preview
- 📈 **Matplotlib Visualization** — Dynamic velocity-time profile preview
- 🌍 **Multilingual Support** — Seamless switching between mutilple languages
- 💾 **Preset Management** — Save, load, and apply preset configurations
- 🎨 **Modern GUI** — Clean Tkinter interface with responsive layout
- 🔧 **Scalable Architecture** — OOP design ready for multi-page expansion

---

## � App Preview

<div align="center">
  <img src="app_preview.png" width="700" alt="Funicular App Screenshot">
</div>

---

```
Funicular_cal_VF1.4/
├── main.py                 # Application entry point
├── my_app.py              # Central controller & global state manager
├── menu_bar.py            # Menu bar widget with commands
├── CHANGELOG.md           # Version history and changes
├── core/
│   ├── config.py          # Static configuration (texts, presets, plot settings)
│   ├── calculations.py    # Pure business logic (no UI dependencies)
│   └── page1_calculations.py  # Page1-specific calculations
├── pages/
│   ├── page1.py          # Page1 UI layout and logic
│   └── page1_plot.py     # Matplotlib plot widget for velocity preview
├── managers/
│   ├── preset_manager.py  # Preset CRUD operations
│   └── table_manager.py   # Dynamic table operations
└── utils/
    └── language.py        # Internationalization helpers
```

---

## 🏗️ Architecture Overview

### Core Components

| Module | Responsibility |
|--------|-----------------|
| **main.py** | Minimal launcher: initializes Tk root, creates MyApp, starts event loop |
| **my_app.py** | Central controller: manages global state (language, page, preset), orchestrates all components |
| **menu_bar.py** | Menu bar widget with Edit/Language/Help menus and keyboard shortcuts |

### Pages (`pages/`)
- **page1.py** — Main calculation page with tables and plot widget
- **page1_plot.py** — Embedded Matplotlib plot (velocity-time curve) with language-aware labels

### Data Layer (`core/`)
- **config.py** — All static strings (UI texts, presets, plot labels) organized by language
- **calculations.py** — Pure math functions (staircases, trapezoidal profiles, etc.)
- **page1_calculations.py** — Page1-specific calculation logic

### Services (`managers/`)
- **preset_manager.py** — Load/save/apply presets with auto-population
- **table_manager.py** — Create tables, bind traces, get/set values, validate inputs

### Utilities (`utils/`)
- **language.py** — Helpers for retrieving language-aware text from config

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `tkinter` (usually included with Python)
- `matplotlib`

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd Funicular_cal_VF1.4

# Install dependencies
pip install matplotlib

# Run the app
python main.py
```

---

## 🌐 Internationalization

The app supports multiple languages:

```python
# Switch languages via menu
# All UI text, tables, plot labels update automatically
```

All language strings are centralized in `core/config.py`:
```python
table_texts = {
    "page1": {"table1": {"header": {"ZH": "...", "EN": "..."}}}
}
```

---

## 📊 Data Flow

```
User Input (Tables)
    ↓
Validation (table_manager)
    ↓
Calculate (calculations.py)
    ↓
Update Plot (page1_plot.py)
    ↓
Display Results
```

---

## 🔄 Preset System

> [!TIP]
> Presets allow quick configuration reuse. Select a preset → tables auto-populate → click Apply.

**Preset Operations:**
- **Load** — Preset dropdown shows available presets
- **Apply** — Populates all tables with preset values
- **Reset** — Clear all pages to initial state

---

## 📦 DPI Awareness

The app supports high-DPI displays (e.g., 4K monitors) on Windows:
```python
# In main.py: SetProcessDpiAwareness(2) enables proper scaling
```

---

## 📝 Version History

See [CHANGELOG.md](./CHANGELOG.md) for detailed version history and changes.

**Latest:** v1.4 — Simplified font rendering, enhanced plot widget

---

## 🛠️ Development

<details>
<summary><b>Adding a New Page</b></summary>

1. Create `pages/page2.py` with your UI layout
2. Register in `my_app.py` (add to pages dict)
3. Add text config to `core/config.py`
4. Add menu option to `menu_bar.py`

</details>

<details>
<summary><b>Adding a New Calculation</b></summary>

1. Add pure function to `core/calculations.py`
2. Call from `pages/page1.py` or manager
3. Update plot in `page1_plot.py` if needed

</details>

---

## 📄 License

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)**

✋ **Non-Commercial Use Only** — This project is licensed for educational and personal use only. Commercial use, including but not limited to selling, licensing, or profiting from this software, is **prohibited without explicit permission**.

**You are free to:**
- Use for personal/educational projects
- Modify and adapt the code
- Share and distribute (with attribution)

**Under the condition that:**
- You provide attribution to the original author
- Derivative works use the same license
- You do not use for commercial purposes

See [Creative Commons License](https://creativecommons.org/licenses/by-nc-sa/4.0/) for full details or contact the author for commercial licensing.

---

## 🤖 Code Transparency

> [!IMPORTANT]
> **AI-Assisted Development Notice:** Parts of this codebase have been generated with the assistance of AI tools. However, **every line of code has been extensively reviewed, tested, and validated** for correctness, security, and performance before being included in this project. The AI was used as a development aid to improve productivity, not as a replacement for careful engineering.

---

## 🤝 Contributing

Contributions welcome! Please follow the modular architecture pattern and add tests where applicable.

> [!NOTE]
> By contributing, you agree that your contributions will be licensed under the same CC BY-NC-SA 4.0 license.






