"""GL-05 trap T2 — one-sided strict comparison (misses reversed touching).
Killed by a reversed back-to-back test (oracle: touching reversed)."""


def overlaps(a_start, a_end, b_start, b_end):
    return a_start <= b_end and b_start < a_end
