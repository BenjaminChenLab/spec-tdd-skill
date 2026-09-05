"""LL-06 reference impl (key): parens or minus = negative (never both); strict 3-digit
comma groups WHEN commas are present; at most two fraction digits (else raise); no
digits raises."""
import re

_GROUP = re.compile(r"^\d{1,3}(,\d{3})*$")
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
    if int_part:
        if "," in int_part:
            if not _GROUP.match(int_part):
                raise ValueError("bad grouping")
        elif not int_part.isdigit():
            raise ValueError("bad digits")
    if frac and not _FRAC.match(frac):
        raise ValueError("bad fraction precision")
    if not int_part and not frac:
        raise ValueError("no digits")
    cents = (int(int_part.replace(",", "")) if int_part else 0) * 100
    if frac:
        cents += int(frac) * (10 ** (2 - len(frac)))
    return -cents if (neg_paren or neg_minus) else cents
