"""Trap T2: rounds to the nearest 5 instead of the nearest 10."""


def round_fee(cents):
    if cents >= 0:
        return (cents * 2 + 5) // 10 * 5
    return -((-cents * 2 + 5) // 10 * 5)


def settle_total(cents_list):
    return sum(round_fee(c) for c in cents_list)
