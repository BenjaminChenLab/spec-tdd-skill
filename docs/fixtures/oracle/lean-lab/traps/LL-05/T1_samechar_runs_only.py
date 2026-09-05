"""Trap T1: collapses only runs of the SAME separator character (key: mixed runs
collapse to one hyphen)."""
import re


def normalize_code(s):
    if not isinstance(s, str):
        raise ValueError("code must be a string")
    trimmed = s.strip(" ")
    if re.search(r"[^A-Za-z0-9\-_ ]", trimmed):
        raise ValueError("invalid character")
    collapsed = trimmed
    for ch in "-_ ":
        collapsed = re.sub(re.escape(ch) + r"+", "-", collapsed)
    if not re.search(r"[A-Za-z0-9]", collapsed):
        raise ValueError("no code")
    return collapsed.upper()
