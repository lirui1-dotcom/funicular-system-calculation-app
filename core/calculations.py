from typing import Callable, Dict

__all__ = ["compute_outputs", "compute_page1", "validate_input"]

# ==========================================================================================
# ERROR class definition
# ==========================================================================================
# ERROR automatically returns ERROR, so formulas stay pure math.
class _Error:
    """
    Singleton "poison value" that propagates through arithmetic operations.
    
    This class creates a single instance (ERROR) that acts as an error sentinel.
    Any arithmetic operation involving ERROR returns ERROR itself, allowing
    errors to propagate silently through chains of calculations without raising
    exceptions or requiring explicit None-checks everywhere.
    
    Intended for pure numerical computations where you want failure to "infect"
    downstream results automatically.
    
    Example:
        result = (ERROR + 5) * 2 / 3    # → ERROR
    """
    #class body execution, only runs once when the class is defined
    __slots__ = ()                      # Prevent __dict__ creation → minimal memory usage
    _instance = None                    # Class-level storage for the singleton instance
  
    def __new__(cls):
        """
        Implement the singleton pattern.
        Ensures only one instance of _Error ever exists.

        Analogy 
        cls = "the school" (the class _Error)
        cls._instance = "the principal office" (shared by the whole class)
        The school itself has one official principal office
        → Every time someone asks "who is the principal?", the school checks its own office
        → If empty → hire one and put them there
        → Next time → just point to the same office
        """
        if cls._instance is None: 
            cls._instance = super().__new__(cls) # First time: actually create the object
        return cls._instance                     # Every time: return the same one

    # ───────────────────────────────────────────────────────────────
    # Arithmetic operator overrides – all return self (i.e. ERROR)
    # This creates the "propagation" behavior for pure math code.
    # ───────────────────────────────────────────────────────────────

    # addition, subtraction
    def __add__(self, other):           # ERROR + x → ERROR
        return self

    __radd__ = __add__                  # x + ERROR → ERROR (reflected addition)
    __sub__  = __add__                  # ERROR - x → ERROR
    __rsub__ = __add__                  # x - ERROR → ERROR

    # multiplication
    def __mul__(self, other):           # ERROR * x → ERROR
        return self

    __rmul__ = __mul__                  # x * ERROR → ERROR

    # division
    def __truediv__(self, other):       # ERROR / x → ERROR
        return self

    __rtruediv__ = __truediv__          # x / ERROR → ERROR

    # negation (unary minus)
    def __neg__(self):                  # -ERROR → ERROR
        return self

    # ───────────────────────────────────────────────────────────────
    # Representation – makes debugging obvious
    # ───────────────────────────────────────────────────────────────

    def __repr__(self):
        """Official string representation – used in REPL/debuggers."""
        return "ERROR"

    def __str__(self):
        """User-friendly string representation – used by print()."""
        return "ERROR"


# Public singleton instance – this is what you import and use
ERROR = _Error()


# ==========================================================================================
# Validation rules registry
# Each page-specific module (e.g. page1_calculations.py) registers its own rules here.
# ==========================================================================================

VALIDATION_RULES: dict = {} # Do NOT add rules directly here — add them in the corresponding pageN_calculations.py.

def _validate_range(value, min_val=None, max_val=None, expected_type=(int, float)):
    """
    Validate numeric value.
    Returns True if valid, False otherwise.
    """
    if value is None:
        return False
    
    if expected_type is int:
        # 1. Reject bools explicitly
        #    (True/False are subclasses of int in Python — this is the #1 gotcha)
        #    Without this, True would be accepted as int. Almost never wanted.
        if isinstance(value, bool):
            return False

        # 2. Only allow numbers (int or float), reject everything else (str, list, None, etc.)
        #    Rejects strings, lists, None, custom objects, etc.
        #    Without this, "5", [1,2,3], etc. would wrongly pass the next check.
        if not isinstance(value, (int, float)):
            return False

        # 3. Only accept floats that are actually whole numbers
        #    (5.0 → ok, 5.3 → reject)
        #    This is the line that makes "strict int" actually strict.
        #    Without it, 5.3 would be accepted because it passed check #2.
        if not float(value).is_integer():
            return False

    elif expected_type is float:
        # 1. Same bool rejection as above
        #    (We don't want True/False accepted when float was requested)
        if isinstance(value, bool):
            return False

        # 2. Only allow numbers (int or float)
        #    This is correct: ints are valid floats.
        #    Rejects everything else (strings, objects, etc.)
        if not isinstance(value, (int, float)):
            return False

        # No third check needed for float — any numeric value is fine

    # 4. Default case for all other types (str, list, dict, custom classes, etc.)
    #    Classic strict isinstance check.
    #    This only runs when expected_type is NOT int and NOT float.
    elif not isinstance(value, expected_type):
        return False

    # If we reached here → everything passed
    # (implicit return True in the original function)

    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True


def validate_input(page: str, table: str, table_data: dict) -> dict:
    """Return per-field validation status for any page/table with rules.

    Args:
        page: Page name. e.g. "page1"
        table: Table name. e.g. "table1"
        table_data: Mapping of field keys to numeric values or None.

    Returns:
        dict: {field_key: bool} where False means invalid.
    """
    rules = VALIDATION_RULES.get(page, {}).get(table, {})
    validity = {}
    for key, (min_val, max_val, expected_type) in rules.items():
        validity[key] = _validate_range(
            table_data.get(key),
            min_val,
            max_val,
            expected_type,
        )
    return validity

# ==========================================================================================
# Helper functions for calculations (e.g., rounding, unit conversions) can go here
## ==========================================================================================
def _round(val, decimals: int):
    """
    Round a numeric value to the specified number of decimals.
    If val is None or an instance of _Error, return "ERROR" string instead.
    This allows the output tables to show "ERROR" for invalid inputs without crashing.

    Args:
        val: Numeric value to round, or None, or _Error.
        decimals: Number of decimal places to round to (default 2).

    Returns:
        Rounded value, or "ERROR" string if input was invalid.

    Example:
            _round(3.14159) → 3.14
            _round(None) → "ERROR"
            _round(ERROR) → "ERROR"
    """
    if val is None or isinstance(val, _Error):
        return "ERROR"
    return round(val, decimals)

def _format_table_value(data, decimals: int = 3):
    """Apply _round to every value in a dictionary.
    
    Args:
        data (dict[str, float | None | _Error]): Dictionary or mapping of keys to numeric values (or None/_Error).
        decimals (int): Number of decimal places to round to.

    Returns:
        dict[str, float | str]: Dictionary with rounded values or "ERROR" strings.

    """
    return {key: _round(value, decimals) for key, value in data.items()}


# ==========================================================================================
# Calculation methods for page 1
# ==========================================================================================

from .page1_calculations import compute_page1 

 
_COMPUTE_DISPATCH: Dict[str, Callable[[str, dict], dict]] = {
    "page1": compute_page1,
}

def compute_outputs(page: str, input_data: dict) -> dict:
    """Dispatch computation to the registered page-specific compute method."""
    compute_method = _COMPUTE_DISPATCH.get(page)
    if compute_method is None:
        raise ValueError(f"No compute method registered for page: {page}")
    return compute_method(page, input_data)

