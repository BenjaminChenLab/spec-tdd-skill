"""Trap T1: exclusive lower bound (contradicts recorded decision D1)."""


def tier_fee(notional_cents, tiers):
    if not isinstance(notional_cents, int) or notional_cents < 0:
        raise ValueError("bad notional")
    lowers = [t[0] for t in tiers]
    if len(set(lowers)) != len(lowers):
        raise ValueError("duplicate lower bound")
    match = None
    for lower, fee in tiers:
        if lower < notional_cents:  # exclusive — the D1 contradiction
            match = fee
    return match if match is not None else 0
