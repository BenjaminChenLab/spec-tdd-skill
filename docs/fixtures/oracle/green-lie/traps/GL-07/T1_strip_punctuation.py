"""GL-07 trap T1 — aggressive normalization (strips punctuation, merges names).
Killed by any punctuation-significance test (oracle: 'ACME Corp.' vs 'ACME Corp')."""
import re


def _norm(name):
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-z ]", "", name.lower())).strip()


def same_counterparty(name_a, name_b):
    return _norm(name_a) == _norm(name_b)
