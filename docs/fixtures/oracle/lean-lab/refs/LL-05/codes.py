"""LL-05 reference impl (key): trim; mixed separator runs -> one hyphen; uppercase fold;
strict alphabet; empty/separator-only raises."""
import re


def normalize_code(s):
    if not isinstance(s, str):
        raise ValueError("code must be a string")
    trimmed = s.strip(" ")
    if re.search(r"[^A-Za-z0-9\-_ ]", trimmed):
        raise ValueError("invalid character")
    collapsed = re.sub(r"[-_ ]+", "-", trimmed)
    if not re.search(r"[A-Za-z0-9]", collapsed):
        raise ValueError("no code")
    return collapsed.upper()
