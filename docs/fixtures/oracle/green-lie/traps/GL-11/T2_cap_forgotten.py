"""GL-11 trap T2 — cap never applied (delays grow unbounded).
Killed by any cap-binding test (oracle: retry_delays(2,5,3) -> [2.0,4.0,5.0] vs [2.0,4.0,8.0])."""


def retry_delays(base_s, max_s, retries):
    return [float(base_s * 2 ** k) for k in range(retries)]
