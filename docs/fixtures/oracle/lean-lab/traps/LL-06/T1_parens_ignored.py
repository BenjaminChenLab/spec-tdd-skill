"""Trap T1: parentheses stripped but the negative sign lost (key: parens = negative)."""
import re

_GROUP = re.compile(r"^\d{1,3}(,\d{3})*$")
_FRAC = re.compile(r"^\d{1,2}$")


def parse_amount(s):
    if not isinstance(s, str):
        raise ValueError("amount must be a string")
    t = s.strip()
    if t.startswith("(") and t.endswith(")") and len(t) >= 2:
        t = t[1:-1].strip()  # sign lost here
    neg = t.startswith("-")
    if neg:
        t = t[1:]
    if "." in t:
        int_part, frac = t.split(".", 1)
        if "." in frac:
            raise ValueError("two points")
    else:
        int_part, frac = t, ""
    if int_part and not _GROUP.match(int_part):
        raise ValueError("bad grouping")
    if frac and not _FRAC.match(frac):
        raise ValueError("bad fraction precision")
    if not int_part and not frac:
        raise ValueError("no digits")
    cents = (int(int_part) if int_part else 0) * 100
    if frac:
        cents += int(frac) * (10 ** (2 - len(frac)))
    return -cents if neg else cents
