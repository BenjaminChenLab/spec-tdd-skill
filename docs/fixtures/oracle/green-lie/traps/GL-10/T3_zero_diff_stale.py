"""GL-10 trap T3 — strict lower bound excludes diff == 0 (a just-read rate is stale).
Killed by any diff-0 test (oracle: (100, 100) -> True vs False)."""


def is_rate_usable(rate_ts_s, now_s):
    return 0 < (now_s - rate_ts_s) < 30
