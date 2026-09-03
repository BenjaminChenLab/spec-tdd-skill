"""GL-06 trap T2 — no clamp at all (raises on clamp-day, spills on others).
Killed by any clamp test (oracle: 2027-01-31 + 1 raises vs 2027-02-28)."""
import datetime as _dt


def add_months(date_str, months):
    y, m, d = (int(p) for p in date_str.split("-"))
    total = (y * 12 + (m - 1)) + months
    y2, m2 = divmod(total, 12)
    return _dt.date(y2, m2 + 1, d).isoformat()  # ValueError on clamp days
