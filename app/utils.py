# app/utils.py

import re
import unicodedata
from datetime import datetime

def sanitize_filename(filename: str) -> str:
    """Remove illegal characters from filenames."""
    filename = unicodedata.normalize("NFKD", filename)
    return re.sub(r'[<>:"/\\|?*]', "", filename)

def generate_slug(text: str) -> str:
    """Convert text to lowercase slug format."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def get_current_timestamp() -> str:
    """Return current timestamp string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
