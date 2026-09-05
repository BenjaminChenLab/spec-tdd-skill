"""LL-02 reference impl (key): D1 inclusive lower; below-first -> 0; empty table -> 0."""


def tier_fee(notional_cents, tiers):
    if not isinstance(notional_cents, int) or notional_cents < 0:
        raise ValueError("bad notional")
    lowers = [t[0] for t in tiers]
    if len(set(lowers)) != len(lowers):
        raise ValueError("duplicate lower bound")
    match = None
    for lower, fee in tiers:
        if lower <= notional_cents:
            match = fee
    return match if match is not None else 0
