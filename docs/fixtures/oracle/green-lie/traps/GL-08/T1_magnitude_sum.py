"""GL-08 trap T1 — magnitude sum (sides ignored, signs lost).
Killed by any mixed-side test (oracle: BUY 100 + SELL 30 -> 70 vs 130)."""


def net_amount(deals):
    return sum(amount for _, amount in deals)
