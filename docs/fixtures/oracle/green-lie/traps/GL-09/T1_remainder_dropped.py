"""GL-09 trap T1 — allocates correctly but returns remainder 0 (lost funds).
Killed by any remainder test (oracle: allocate(10,[3,3,3]) -> remainder 1 vs 0)."""


def allocate(amount_cents, caps):
    out = []
    remaining = amount_cents
    for cap in caps:
        take = min(max(remaining, 0), cap)
        out.append(take)
        remaining -= take
    return out, 0  # remainder silently dropped
