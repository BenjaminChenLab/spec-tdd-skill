# Baseline: parallel multi-unit batches — v1.14.0

**Date:** 2026-09-02 · **Status:** baseline + design approved in session · **Version target:** 1.14.0
**Source:** real production run — dtms-toolbox webhook duplicate-deal fix (6-unit money-movement batch, Tasks 1–7, plan at `doc/blueprint/fix/WebhookQtActionDuplicateDealFix-plan.md` in that repo). Improvement suggestion doc carried in-session at `B:\spec-ttd-adversarial-improvement-parallel-multi-unit.md`.

## RED — what the skill-as-written produced on a real batch

This baseline is a production run, not a synthetic arm — stronger evidence, different bias (one project, one stack: Java/Maven, single test module).

1. **Per-unit full adversarial cycles scale badly.** The multi-unit loop says a critical unit "runs its Phase 2–3 at that tier's verification depth … applied to that unit inside this loop" — on a 6-unit all-critical batch that reads as SIX sequential full cycles (implementer + attack loop ≤3 rounds + dry-loop ≤2 rounds each). Projected 5–8 h wall-clock. Measured components: one round-1 attacker dispatch ~31 min (copies the project, runs multiple `mvn` cycles to verify wrong-impls); one `mvn test -Dtest=OneClass` cycle 1–3 min; one implementer dispatch ~5 min. **The bottleneck is per-dispatch physical time × sequential full cycles — not thinking.**
2. **No parallelizability analysis anywhere.** Tasks 3/4/5 all edit `WebhookService.java` AND the same test class (a hard serial chain); Tasks 2 and 6 touch disjoint file sets — the skill serialized both alike. A13 (unit plan) has order/grouping but no file-conflict concept.
3. **The obvious parallelization tools are silent traps.** Worktree isolation branches from HEAD — under the source repo's standing never-commit rule (human commits at the end), an isolated implementer silently builds against a tree missing all prior units' code. Shared-tree concurrent builds race on `target/`. A compile-breaking RED test (the documented expected RED state for new symbols) in a single test module breaks `mvn test-compile` for every concurrently running sibling.

The run improvised past all five traps (wave-parallel scratch copies + consolidated attack, ~2–2.5 h) — the improvisation worked, which is exactly why it must be codified: the next orchestrator gets different luck.

## Counter-evidence (what the tier got RIGHT — not on the table)

Round-1 per-unit attackers caught 7 wrong-but-green impls, including a silent-swallow class that would have re-created the production incident. The adversarial tier's rigor is justified; the defect is batch COMPOSITION, not depth. Deliberately NOT adopted: parallelizing file-sharing units via merge (merge risk outweighs wall-clock), weakening the attack-loop breaker, skipping the terminal dry-loop.

## Design (approved 2026-09-02, four decisions)

- **P1 — parallelizability analysis rides the unit plan (A13):** per-unit expected file sets; **disjoint + spec-compiles-against-current-tree** (references only existing symbols — a unit needing a symbol a later unit creates is a dependency, not a sibling) → parallel wave; shared production/test file → serial chain in dependency order. Surfaced, never gated (HOW, I12); carried in the batch ledger (A16); re-checked when actual files diverge from the plan. *Decision #2:* wave membership requires current-tree-compilable specs — new-symbol units route to the serial chain under the existing just-in-time rule; NO per-copy test authoring.
- **P2 — scratch-copy isolation for parallel implementers:** one build-needed-tree copy per unit (sources/build files/configs; exclude build output, `.git`, scratch), verified to compile before dispatch — never the shared tree (build-dir races), never a worktree under uncommitted state (silent missing-work trap). Merge-back per unit, ALLOWLIST only (planned production files + own new test files; the acceptance test is real-tree-authoritative, never merged back); re-run affected tests in the REAL tree after EACH merge-back (I5 — scratch green alone proves nothing). Re-cut copies per wave so later waves include landed work.
- **P3 — ordering against compile-breaking REDs:** the wave's compilable specs are authored + RED-verified and copies cut BEFORE any compile-breaking RED enters the real tree (a serial unit's just-in-time new-symbol spec) — one broken test module breaks every sibling. Default shape: the wave lands and re-verifies green, then the serial chain's just-in-time loop runs. (Bug batches: repro specs all compile — interleaving is safe.)
- **P4 — consolidated attack, after ALL units land (decision #1: 時間大於一切 — option A, not per-wave):** per-unit Phase-3 core verify (re-hash, own re-run, SPEC-DEFECT sweep) stays per unit; the ATTACKER + terminal dry-loop run ONCE over the whole hardened batch — Part A on the full suite + every unit's intent (attacker instructed unit-by-unit in dependency order, reporting per unit), Part B branch-hunt per file cluster. Same circuit breaker, judged PER HOLE (a re-failed missing case parks that unit's hole as residual; other units' holes don't burn its rounds). Fresh TOP-tier dispatch each round. **Stated trade:** consolidation delays hole discovery until downstream units have landed on subtly-wrong upstream code; repair is the normal strengthen → re-RED → re-delegate loop, then downstream specs re-run against the fixed code (independent oracles — usually still green). Accepted for wall-clock, knowingly.
- **P5 — pre-fix baseline capture (decision #3: existing `.spec-tdd/` scratch convention):** batch landing on an already-failing suite → run the full suite ONCE before any change, persist the failure list to `.spec-tdd/` scratch (path in the ledger); final verification diffs against it — a pre-existing failure is never read as this batch's regression.

## Measured effect (6 units)

| Approach | Wall-clock |
|---|---|
| Per-unit full adversarial (skill as written) | 5–8 h projected |
| Serial + consolidated attack (improvised) | ~3 h |
| Parallel waves + consolidated attack (P1–P4, improvised) | ~2–2.5 h |

## GREEN — verification plan

Recognition-layer arms (fresh subagents, blind to hypothesis, reading the new text from the working tree): A1 multi-unit planning on a dtms-shaped synthetic batch (expects wave/chain split, scratch-copy not worktree, allowlist merge-back, baseline capture); A2 adversarial batch composition (expects consolidated attack after landing, per-hole breaker, no per-unit attack loops); A3 worktree-trap micro under an explicit "just use worktrees" temptation. Results recorded in the CHANGELOG entry.

The full behavioral path (real concurrent implementers, real merge-backs) is not arm-tested — the production run that produced this baseline IS the behavioral evidence; next real-use runs carry the trial (knobs in the project memory).
