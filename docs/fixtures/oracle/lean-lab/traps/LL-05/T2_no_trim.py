"""Trap T2: forgets the trim — outer spaces become hyphens instead of disappearing."""
import re


def normalize_code(s):
    if not isinstance(s, str):
        raise ValueError("code must be a string")
    if re.search(r"[^A-Za-z0-9\-_ ]", s):
        raise ValueError("invalid character")
    collapsed = re.sub(r"[-_ ]+", "-", s)
    if not re.search(r"[A-Za-z0-9]", collapsed):
        raise ValueError("no code")
    return collapsed.upper()
