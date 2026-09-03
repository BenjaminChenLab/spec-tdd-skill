"""GL-09 trap T3 — empty caps return zero remainder (funds lost on the empty path).
Killed by any empty-caps test (oracle: allocate(10,[]) -> ([], 10) vs ([], 0))."""


def allocate(amount_cents, caps):
    if not caps:
        return [], 0  # wrong: the full amount must come back as remainder
    out = []
    remaining = amount_cents
    for cap in caps:
        take = min(max(remaining, 0), cap)
        out.append(take)
        remaining -= take
    return out, remaining
