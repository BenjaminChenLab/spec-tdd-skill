"""Trap T3: empty tier table treated as a configuration error (key: 0 — spec silent)."""


def tier_fee(notional_cents, tiers):
    if not isinstance(notional_cents, int) or notional_cents < 0:
        raise ValueError("bad notional")
    if not tiers:
        raise ValueError("empty band table")  # the open-point resolution the key rejects
    lowers = [t[0] for t in tiers]
    if len(set(lowers)) != len(lowers):
        raise ValueError("duplicate lower bound")
    match = None
    for lower, fee in tiers:
        if lower <= notional_cents:
            match = fee
    return match if match is not None else 0
