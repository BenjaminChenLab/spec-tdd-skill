"""GL-01 trap T1 — boundary `>=` (purges ON the exact 7-year anniversary).
Killed by any test asserting exactly-7 keeps (oracle: exactly-7 jun/mar)."""


def should_purge(record_date, as_of_date):
    anniversary = record_date.replace(year=record_date.year + 7)
    return as_of_date >= anniversary
