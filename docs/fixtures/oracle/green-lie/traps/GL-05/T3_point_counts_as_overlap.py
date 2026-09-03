"""GL-05 trap T3 — point-in-range test (a zero-length interval "overlaps").
Killed by any zero-length test (oracle: (10,10,10,20) -> False vs True)."""


def overlaps(a_start, a_end, b_start, b_end):
    return (a_start <= b_start < a_end) or (b_start <= a_start < b_end)
