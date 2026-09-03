"""GL-01 trap T3 — month-count arithmetic (day-of-month ignored, so the exact
anniversary day purges and the day before is miscounted).
Killed by oracle cases exactly-7 jun / exactly-7 mar / younger keeps."""


def should_purge(record_date, as_of_date):
    months = (as_of_date.year - record_date.year) * 12 + (as_of_date.month - record_date.month)
    return months >= 7 * 12
