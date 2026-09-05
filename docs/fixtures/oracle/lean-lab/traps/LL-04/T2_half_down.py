"""Trap T2: halfway rounds DOWN (key: up / away from zero)."""
import math


def _round_half_down(x):
    if x >= 0:
        return int(math.ceil(x - 0.5))
    return -int(math.ceil(-x - 0.5))


def convert(amount_cents, pair, rates):
    if pair in rates:
        return _round_half_down(amount_cents * rates[pair])
    rev = (pair[1], pair[0])
    if rev in rates:
        return _round_half_down(amount_cents / rates[rev])
    raise ValueError("unknown pair")
