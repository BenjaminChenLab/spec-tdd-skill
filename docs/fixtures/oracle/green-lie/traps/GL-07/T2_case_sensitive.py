"""GL-07 trap T2 — whitespace-normalizes but never case-folds.
Killed by any case-insensitivity test (oracle: 'acme corp' vs 'ACME CORP')."""


def _norm(name):
    return " ".join(name.split())


def same_counterparty(name_a, name_b):
    return _norm(name_a) == _norm(name_b)
