"""GL-11 trap T3 — returns retries+1 delays (one entry too many).
Killed by any list-shape test (oracle: retry_delays(2,10,3) -> 3 entries vs 4)."""


def retry_delays(base_s, max_s, retries):
    return [float(min(base_s * 2 ** k, max_s)) for k in range(retries + 1)]
