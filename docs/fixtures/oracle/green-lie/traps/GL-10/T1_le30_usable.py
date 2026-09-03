"""GL-10 trap T1 — inclusive window (`<= 30` counts as fresh).
Killed by any exactly-30 test (oracle: diff 30 -> stale vs usable)."""


def is_rate_usable(rate_ts_s, now_s):
    return 0 <= (now_s - rate_ts_s) <= 30
