"""GL-06 trap T1 — clamps February to 28 unconditionally (leap years ignored).
Killed by any leap-clamp test (oracle: 2024-01-31 + 1 -> 2024-02-29 vs 02-28)."""
import datetime as _dt


def add_months(date_str, months):
    y, m, d = (int(p) for p in date_str.split("-"))
    total = (y * 12 + (m - 1)) + months
    y2, m2 = divmod(total, 12)
    m2 += 1
    day = d
    if m2 == 2 and day > 28:
        day = 28  # wrong: ignores leap years
    return _dt.date(y2, m2, day).isoformat()
