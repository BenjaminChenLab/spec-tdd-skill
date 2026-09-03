"""GL-09 trap T2 — negative amounts silently processed (no ValueError).
Killed by any negative-amount test (oracle: allocate(-1,[5]) must RAISE)."""


def allocate(amount_cents, caps):
    out = []
    remaining = amount_cents
    for cap in caps:
        take = min(remaining, cap) if remaining > 0 else 0
        out.append(take)
        remaining -= take
    return out, remaining
