"""Language utilities for text lookup and translation."""

from core.config import default_language


def get_text(key, label_dict, current_language_var):
    """
    Get label in the currently selected language from the given dictionary.
    Falls back to default_language if missing.
    Last resort: returns the key itself.
    
    Args:
        key (str): The key to look up (e.g. "main_title", "label_text")
        label_dict (dict): Dictionary of translations, usually structured as
                        {key: {lang_code: translated_text, ...}}
                        Example: {"main_title": {"ZH": "北京", "EN": "Beijing"}}
        current_language_var (tk.StringVar): The current language selection variable
    
    Returns:
        str: The translated text, or fallback/default, or the key itself if not found.
    
    Example:         
        current_language = "EN" → returns "Beijing"
        current_language = "ZH" → returns "北京"
        current_language = "FR" → returns "Beijing" (fallback to EN/default)
        key not found → returns "main_title" (the key itself)
    """
    lang = current_language_var.get()
    entry = label_dict.get(key, {})
    return entry.get(lang) or entry.get(default_language) or key


def get_lan_text(label_dict, language):
    """
    Retrieve text from a language dictionary for the specified language.

    Falls back to default_language if the requested language is missing.
    Returns an empty string if no suitable translation is found.

    Args:
        label_dict (dict): Dictionary mapping language codes to translated strings.
                        Example: {"ZH": "北京", "EN": "Beijing", "FR": "Pékin"}
        language (str): The language code to look up (e.g. "EN", "ZH").

    Returns: 
        str: The translated text in the requested language, or fallback to
            default_language, or empty string if nothing is found.

    Examples:
        get_lan_text(label_dict, "EN")   →  "Beijing"
        get_lan_text(label_dict, "ZH")   →  "北京"
        get_lan_text(label_dict, "FR")   →  "Beijing"  (fallback to default_language)
        get_lan_text({}, "EN")           →  ""         (empty dict → empty string)
        get_lan_text({"EN": "Hello"}, "ZH") → "Hello"  (missing ZH → fallback)
    """
    return label_dict.get(language) or label_dict.get(default_language) or ""


__all__=["get_text", "get_lan_text"]