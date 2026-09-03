"""GL-10 trap T2 — abs() difference (future timestamps read as fresh).
Killed by any future-timestamp test (oracle: (100, 95) -> False vs True)."""


def is_rate_usable(rate_ts_s, now_s):
    return abs(now_s - rate_ts_s) < 30
