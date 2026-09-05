"""Trap T3: settle_total rounds the SUM once (key: rounds per item, then sums)."""


def _round10(x):
    if x >= 0:
        return (x * 2 + 10) // 20 * 10
    return -((-x * 2 + 10) // 20 * 10)


def round_fee(cents):
    return _round10(cents)


def settle_total(cents_list):
    return _round10(sum(cents_list))
