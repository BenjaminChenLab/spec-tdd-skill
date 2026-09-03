"""GL-11 trap T1 — exponent off by one (first delay is 2x base).
Killed by any first-delay test (oracle: retry_delays(2,5,3) -> [2.0,...] vs [4.0,...])."""


def retry_delays(base_s, max_s, retries):
    return [float(min(base_s * 2 ** k, max_s)) for k in range(1, retries + 1)]
