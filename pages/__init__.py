"""
pages/
├── __init__.py
├── page1.py          # e.g. Home or MainInput page
├── page2.py          # e.g. Results or TableView
├── page3.py          # e.g. Settings or About

"""

from .page1 import Page1
from .page1_plot import Page1Plot
#from .page2 import Page2


__all__ = ["Page1", "Page1Plot"]  # Add "Page2" when it's implemented