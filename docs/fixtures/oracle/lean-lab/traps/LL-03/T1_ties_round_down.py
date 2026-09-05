"""Trap T1: halfway cases round DOWN (key: up / away from zero)."""


def round_fee(cents):
    if cents >= 0:
        return (cents * 2 + 9) // 20 * 10
    return -((-cents * 2 + 9) // 20 * 10)


def settle_total(cents_list):
    return sum(round_fee(c) for c in cents_list)
