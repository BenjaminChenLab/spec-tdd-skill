"""LL-03 reference impl (key): nearest 10, halfway up positive, mirrored about zero."""


def round_fee(cents):
    if cents >= 0:
        return (cents * 2 + 10) // 20 * 10
    return -((-cents * 2 + 10) // 20 * 10)


def settle_total(cents_list):
    return sum(round_fee(c) for c in cents_list)
