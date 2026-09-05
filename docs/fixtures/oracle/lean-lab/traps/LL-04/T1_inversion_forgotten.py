"""Trap T1: the inverse fallback multiplies by the reversed pair's rate directly
(forgets the 1/r inversion)."""
import math


def _round_half_up(x):
    return int(math.floor(x + 0.5))


def convert(amount_cents, pair, rates):
    if pair in rates:
        return _round_half_up(amount_cents * rates[pair])
    rev = (pair[1], pair[0])
    if rev in rates:
        return _round_half_up(amount_cents * rates[rev])  # inversion forgotten
    raise ValueError("unknown pair")
