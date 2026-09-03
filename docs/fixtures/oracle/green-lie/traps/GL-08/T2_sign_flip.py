"""GL-08 trap T2 — signs flipped (SELL positive, BUY negative).
Killed by any net-sign test (oracle: BUY 100 + SELL 30 -> +70 vs -70)."""


def net_amount(deals):
    total = 0
    for side, amount in deals:
        total += amount if side == "SELL" else -amount
    return total
