"""GL-06 trap T3 — month arithmetic off by one (adds months-1).
Killed by any plain-addition test (oracle: 2026-06-15 + 2 -> 2026-08-15 vs 07-15)."""
import datetime as _dt


def add_months(date_str, months):
    y, m, d = (int(p) for p in date_str.split("-"))
    total = (y * 12 + (m - 1)) + (months - 1)  # off by one
    y2, m2 = divmod(total, 12)
    return _dt.date(y2, m2 + 1, d).isoformat()
