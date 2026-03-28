
calculator_app/
├── main.py
├── my_app.py
├── pages/
│   ├── __init__.py
│   └── page1.py
├── managers/
│   ├── __init__.py
│   ├── table_manager.py
│   └── preset_manager.py
├── core/
│   ├── __init__.py
│   ├── calculations.py
│   └── config.py
├── widgets/         # currently not implemented for simplicity
│   ├── __init__.py
│   └── menu_bar.py
├── utils/
|   ├── __init__.py
│   └── language.py
└── README.md


### Folder & File Responsibilities

- **main.py**  
  Tiny launcher: creates Tk root, instantiates MyApp, starts main loop.

- **my_app.py**  
  Thin controller / central app class: global state (language, current page, selected preset), orchestrates pages & managers, handles top-level refresh & switching.

- **pages/**  
  Page-specific UI and behavior (one file per screen).

  - **page1.py**  
    Page1 layout, calls to table builder, refresh logic, live calculation trigger.

- **managers/**  
  Reusable managers/services for specific domains.

  - **table_manager.py**  
    All table operations: building, linking traces, get/set values, clearing inputs, table helpers.

  - **preset_manager.py**  
    Preset loading, label-to-key mapping, applying presets, reset handling.

- **core/**  
  Essential non-UI logic and static data.

  - **calculations.py**  
    Pure math/business rules (no Tkinter, no state).

  - **config.py**  
    All static texts (table_texts, presets_texts, menu_texts, title_texts) + presets dictionary.

- **widgets/**  
  Custom or reusable widget classes.

  - **menu_bar.py**  
    Menu bar widget and its commands (Edit, Language, etc.).

- **utils/**  
  Small generic helpers used app-wide.

  - **language.py**  
    Internationalization helpers: get_text, get_lan_text.

- **README.md**  
  Project overview, setup, usage instructions.



### Recalculation Full Workflow
Entry change
    ↓
link_table_vars              (table_manager.py)
                             Attach trace callbacks to all Entry StringVars
                             in a table so changes trigger recalculation.
    ↓
trace_add                    (Tkinter internal)
                             Fires automatically when a StringVar value
                             changes.
    ↓
_recalculate                 (my_app.py)
                             Central dispatcher that routes the event
                             to the correct page-specific recalculation.
    ↓
_recalculate_pageX           (page1.py / page2.py)
                             Page-specific logic that:
                             - reads inputs
                             - calls calculations
                             - writes outputs
    ↓
read_table_inputs            (table_manager.py)
                             Reads Entry values from a table and converts
                             them from StringVar → float for calculations.
    ↓
compute_pageX                (calculations.py)
                             Pure calculation logic. No Tkinter code.
                             Returns results as a dictionary.
    ↓
write_table_outputs          (table_manager.py)
                             Writes calculated results back to the
                             output table's Entry StringVars.