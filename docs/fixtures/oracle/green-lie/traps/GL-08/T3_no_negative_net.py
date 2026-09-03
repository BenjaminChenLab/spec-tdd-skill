"""GL-08 trap T3 — clamps the net at zero (a negative position "can't happen").
Killed by any net-negative test (oracle: all sells -> -75 vs 0)."""


def net_amount(deals):
    total = 0
    for side, amount in deals:
        total += amount if side == "BUY" else -amount
    return max(0, total)
