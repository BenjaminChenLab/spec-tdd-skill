"""Trap X1 (cross-cutting): functionally correct on every value, but MEMOIZES the
inverse rate back into the caller's rates dict — a batch reusing one table across
a whole book gets its mapping rewritten underneath it. Invisible to value-only
tests; fails the oracle's purity checks."""
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
        inv = 1.0 / rates[rev]
        rates[pair] = inv  # the mutation — key says the table is the caller's
        return _round_half_away(amount_cents * inv)
    raise ValueError("unknown pair")
