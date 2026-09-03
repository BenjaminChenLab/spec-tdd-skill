"""GL-01 trap T2 — fixed 7*365-day count (ignores calendar years / leap days).
Killed by any test spanning a leap-day interval near the boundary
(oracle: exactly-7 jun/mar — both spans cross a Feb 29)."""
import datetime as _dt


def should_purge(record_date, as_of_date):
    age = _dt.date(as_of_date.year, as_of_date.month, as_of_date.day) - record_date
    return age.days >= 7 * 365
