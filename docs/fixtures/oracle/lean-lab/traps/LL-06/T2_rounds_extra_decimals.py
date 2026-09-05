"""Trap T2: more than two fraction digits rounds to two (key: ValueError — no rounding)."""
import re

_GROUP = re.compile(r"^\d{1,3}(,\d{3})*$")


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
        if len(frac) > 2:  # rounds instead of raising — the dropped strictness
            frac = "%02d" % round(int(frac) / (10 ** (len(frac) - 2)))
    else:
        int_part, frac = t, ""
    if int_part and not _GROUP.match(int_part):
        raise ValueError("bad grouping")
    if not int_part and not frac:
        raise ValueError("no digits")
    cents = (int(int_part) if int_part else 0) * 100
    if frac:
        cents += int(frac) * (10 ** (2 - len(frac)))
    return -cents if (neg_paren or neg_minus) else cents
