# Multi-unit batches — consolidated attack — spec-tdd-adversarial (progressive reference)

Part of `spec-tdd-adversarial` (v1.36.0 progressive split — the SKILL.md's flow pointers load this file on demand). **Read it when the adversarial tier runs over a BATCH of critical units** (spec-tdd's multi-unit loop routes each unit here). A single-unit run never reads it.

---

## Multi-unit batches — consolidated attack

A batch of critical units (spec-tdd's Multi-unit loop routes each unit here, per unit) does NOT run a full attack loop per unit: per-unit cycles scale badly — measured on a real 6-unit money-movement batch, sequential full cycles projected 5–8 h wall-clock (one round-1 attacker dispatch alone ran ~31 min), and rounds 2–3 per unit mostly re-tread files a fresh whole-surface attacker covers anyway.

- **Per unit, unchanged:** Phase-3 steps 1–2 (re-hash, your own re-run GREEN, SPEC-DEFECT sweep) run per unit inside the multi-unit loop — a unit merges back only on its own green evidence, in the real tree.
- **Consolidated, dispatched as the FINAL WAVE dispatches (not after it merges):** the attacker works unit-by-unit in dependency order — by the time it reaches the last wave's units they are landed + real-tree GREEN (measured: an implementer ~5 min ≪ an attacker 31 min+). A unit NOT yet landed when reached is skipped and revisited at the end — never attacked half-landed. **Part A:** the full suite + every unit's intent, NOT impls, reporting per unit; **Part B:** branch-hunt per file cluster (one attacker per serial-chain cluster, one for the disjoint islands). This is the run's longest block — I19(e) visibility applies throughout: per-unit progress lines relayed during the block, not an end-dump.
- **Breaker — same circuit breaker, judged PER HOLE:** "same hole" = the same unit's missing acceptance-test case re-failing; a hole re-failing parks THAT unit's hole as its residual — other units' holes don't burn its rounds. The 3-round cap spans the consolidated loop. Per-unit residuals surface in the batch summary.
- **The accepted trade (smaller than it was — wall-clock over earliness):** consolidation delays hole discovery until downstream units have landed on the upstream code the hole lives in; the final-wave overlap bounds that delay to wave-time rather than whole-batch-time. Repair is the normal loop — strengthen → batch-verify (step 4) → re-delegate where IMPL → GREEN — then re-run the DOWNSTREAM units' acceptance specs against the fixed code (independent oracles; usually still green). Traded knowingly.
- **Terminal dry-loop: consolidated too** — one rotation over the whole batch's diff; same lenses, same severity floor, same cap, same ask-the-human on a non-converging cap (`timebox`: the merged mode over the whole diff).
