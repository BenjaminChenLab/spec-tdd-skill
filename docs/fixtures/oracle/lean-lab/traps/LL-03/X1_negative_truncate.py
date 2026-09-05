"""Trap X1 (cross-cutting): positives match the key exactly; NEGATIVES truncate toward
zero instead of mirroring away from zero. Invisible to delta-only tests (the sign
contract lives in the caller/old surface); fails the oracle's mirror cases."""


def round_fee(cents):
    if cents >= 0:
        return (cents * 2 + 10) // 20 * 10
    return -((-cents) // 10) * 10  # toward zero — the cross-cutting divergence


def settle_total(cents_list):
    return sum(round_fee(c) for c in cents_list)
