"""GL-02 trap T3 — floor every share, remainder silently lost (sum < total).
Killed by any conservation test (oracle: 200/3 -> [66,66,66] vs [67,67,66])."""


def split_amount(total_cents, n):
    return [total_cents // n] * n
