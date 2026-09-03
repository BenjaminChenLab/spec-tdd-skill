"""GL-03 trap T1 — sums ALL occurrences (double-applied money).
Killed by any duplicate-scenario test (oracle: mixed dup applied 15 vs 25)."""


def process_batch(entries):
    applied = sum(amount for _, amount in entries)
    return {
        "applied": applied,
        "count": len({rid for rid, _ in entries}),
        "duplicates_ignored": len(entries) - len({rid for rid, _ in entries}),
    }
