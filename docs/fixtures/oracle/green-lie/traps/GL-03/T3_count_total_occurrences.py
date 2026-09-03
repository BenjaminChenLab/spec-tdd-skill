"""GL-03 trap T3 — dedupes money correctly but `count` counts every occurrence.
Killed by any test asserting count == unique ids (oracle: mixed dup count 2 vs 3)."""


def process_batch(entries):
    seen = {}
    for rid, amount in entries:
        if rid not in seen:
            seen[rid] = amount
    return {
        "applied": sum(seen.values()),
        "count": len(entries),  # wrong: total occurrences, not unique
        "duplicates_ignored": len(entries) - len(seen),
    }
