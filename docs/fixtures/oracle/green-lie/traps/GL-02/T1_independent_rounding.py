"""GL-02 trap T1 — round each share independently (conservation drift).
Killed by any conservation-asserting test (oracle: 100/6 -> sum 102 vs 100)."""


def split_amount(total_cents, n):
    return [int(round(float(total_cents) / n)) for _ in range(n)]
