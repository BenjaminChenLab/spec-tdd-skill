"""GL-05 trap T1 — closed-interval comparison (touching counts as overlap).
Killed by any back-to-back test, either direction (oracle: touching cases)."""


def overlaps(a_start, a_end, b_start, b_end):
    return a_start <= b_end and b_start <= a_end
