"""GL-03 trap T2 — LAST occurrence wins (overwrites instead of first).
Killed by any differing-amounts repeat test (oracle: a:10,a:99 -> 10 vs 99)."""


def process_batch(entries):
    seen = {}
    for rid, amount in entries:
        seen[rid] = amount  # overwrite: last wins
    return {
        "applied": sum(seen.values()),
        "count": len(seen),
        "duplicates_ignored": len(entries) - len(seen),
    }
