"""Trap T3: drops the comma-group validation (any comma placement accepted)."""
import re

_FRAC = re.compile(r"^\d{1,2}$")


def parse_amount(s):
    if not isinstance(s, str):
        raise ValueError("amount must be a string")
    t = s.strip()
    neg_paren = t.startswith("(") and t.endswith(")") and len(t) >= 2
    if neg_paren:
        t = t[1:-1].strip()
    neg_minus = t.startswith("-")
    if neg_minus:
        t = t[1:]
    if neg_paren and neg_minus:
        raise ValueError("double sign")
    if "." in t:
        int_part, frac = t.split(".", 1)
        if "." in frac:
            raise ValueError("two points")
    else:
        int_part, frac = t, ""
    # group-length check skipped entirely — the dropped clause
    if frac and not _FRAC.match(frac):
        raise ValueError("bad fraction precision")
    if not int_part and not frac:
        raise ValueError("no digits")
    cents = int(int_part.replace(",", "")) * 100 if int_part else 0
    if frac:
        cents += int(frac) * (10 ** (2 - len(frac)))
    return -cents if (neg_paren or neg_minus) else cents
