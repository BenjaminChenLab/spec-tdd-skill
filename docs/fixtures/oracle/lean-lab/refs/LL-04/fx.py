"""LL-04 reference impl (key): direct/inverse conversion, half-up away from zero,
ValueError on unknown pair, never mutates the rates mapping."""
import math


def _round_half_away(x):
    if x >= 0:
        return int(math.floor(x + 0.5))
    return -int(math.floor(-x + 0.5))


def convert(amount_cents, pair, rates):
    if pair in rates:
        return _round_half_away(amount_cents * rates[pair])
    rev = (pair[1], pair[0])
    if rev in rates:
        return _round_half_away(amount_cents / rates[rev])
    raise ValueError("unknown pair")
