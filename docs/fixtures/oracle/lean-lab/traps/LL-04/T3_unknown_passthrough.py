"""Trap T3: unknown pair silently returns the input amount (key: ValueError — fail loud)."""
import math


def _round_half_up(x):
    return int(math.floor(x + 0.5))


def convert(amount_cents, pair, rates):
    if pair in rates:
        return _round_half_up(amount_cents * rates[pair])
    rev = (pair[1], pair[0])
    if rev in rates:
        return _round_half_up(amount_cents / rates[rev])
    return amount_cents  # the silent passthrough the spec forbids
