"""Trap T2: below-first-band notionals pay the first band's minimum (key: no band, no fee — 0)."""


def tier_fee(notional_cents, tiers):
    if not isinstance(notional_cents, int) or notional_cents < 0:
        raise ValueError("bad notional")
    if not tiers:
        return 0
    lowers = [t[0] for t in tiers]
    if len(set(lowers)) != len(lowers):
        raise ValueError("duplicate lower bound")
    for lower, fee in tiers:
        if lower <= notional_cents:
            last = fee
    # fallback: below every band -> the first band's minimum applies anyway
    return last if notional_cents >= tiers[0][0] else tiers[0][1]
