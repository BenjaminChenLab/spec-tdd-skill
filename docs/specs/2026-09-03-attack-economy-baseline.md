# Attack-economy baseline — batched runs, parallel loops (v1.15.0)

**Source run:** RFI split-approval sibling-reset marker fix (branch `dev`, 2 orchestrator contexts, 3 attack rounds + 3 repair rounds, 2026-09-03). Outcome: 20 wrong-but-green holes all closed; 195 tests / 13 classes GREEN; one precise RED counter-example per hole. The run validated the adversarial tier's DEPTH (fresh-context attackers found holes a same-context flow never would) while exposing its COST shape — this document records that shape and the rules it produced.

## Measured cost anatomy

| Item | Measured |
|---|---|
| Production change | main fix 3 files +124/−16; follow-up 4 files +106/−0 (~340 lines total) |
| Tests | 21 → 195 / 13 classes (attack hardening +69 tests / 6 new files) |
| Wall-clock | ~6+ h (context #1 ≈ 3.7 h + context #2 ≈ 2.5 h+) |
| Rate | ≈ 1 h per 60 lines of production change; 45–60 min per attack-repair cycle |
| **One mutant per full-suite run** | R1/R2 ≈ 27 min per file per round |
| **Cross-file batched mutants** | R3: 9 mutants in 16.5 min |
| **Batched strengthen verification** | 20 holes / 3 repair rounds at 1–2 build runs per round |

The build run — not the reasoning — is the attack loop's unit of cost. Batched runs cut it ~3–5× without touching a verdict rule.

## Hole taxonomy (the 7 classes → Phase-1 self-check + attacker seeds)

| # | Hole class | Instance from the run | Guard rule |
|---|---|---|---|
| B1 | Mutable-state assertion | R1 H2/H3/H4 (a captor's live reference cannot tell pre-call from post-call processing) | Assert only on a deep-copy snapshot taken at call time inside the stub (`doAnswer`) |
| B2 | Mocked-out funnel | R2 EXP-1 critical (strip logic inside the service passes green) | ≥1 wiring test per production funnel driving the REAL method (save-time snapshot) |
| B3 | Entry wiring untested | R3 M7 critical (public entry drops its internal call, still green) | Drive the public entry, not only the package-private seam |
| B4 | Fixture-shape gating | R3 M1/M2 critical (`if(type!=null)` / `if(missionId==null)` gates bypass the bare builder fixture) | Fixtures are production-shaped (all production-required fields set) — cheapest, highest kill rate |
| B5 | Structural equality erases identity | R2 EXP-15, R3 M3 (`deepCopy`+`equals` cannot see aliasing) | `identityHashCode`/`assertNotSame`, pairwise on nested subtrees |
| B6 | Property alphabet too narrow | R2 EXP-16, R3 M4 (synthetic keys vs the real `rfiHistory` keys) | Generators must include the production key names |
| B7 | Copy depth | R3 M5 (two-layer copy passes a literal deep-copy test) | Recursive no-alias oracle + depth ≥3 generators |

13 of the 20 holes were these classes — a Phase-1 self-check against this list prevents them at zero attack-round cost. All three rounds' holes lived in the NEWLY STRENGTHENED tests (old seams: zero recurrence) — fresh-context attackers earn their dispatch.

## Rules adopted (v1.15.0)

- **A1 — attacker run economy** (dispatch template): cross-file mutant batches, one run, attribution by which test goes RED; never two mutants in the same file (masking → false CAUGHT/HOLE); screening on focused test classes, full-suite confirmation for candidate holes; quiet output (`-q --console=plain | tail -5` form).
- **A2 — one-shot strengthen verification** (replaces per-hole RED→GREEN): N preserved wrong-impls applied together → exactly N new tests RED (the attribution proof) → byte-exact restore → `git hash-object` re-verified → full GREEN. Mismatch → per-mutant fallback for the affected file.
- **A3 — cost disclosure** (When-to-Use): the measured table above, so the human sizes the bet before routing.
- **B1–B7** — Phase-1 hole-class self-check + default attacker seeds.
- **C1 — severity floor for attack rounds**: only critical/moderate holes buy a round; weak/contract/spec-letter holes ride the residual list.
- **C2 — lifted cap ≠ silent grind**: every round reports its trail; a new critical asks the human to confirm investment.
- **C3 — `timebox` merged dry-loop**: one round, deployment+fidelity over the full diff (test-strength is the attack loop's own job).
- **C4 — run ledger (A16)**: append-only state + verdicts + iron rules, written-ahead — cross-context survival by design.
- **C5 — attacker hygiene**: file-copy backup restores (never git write ops), `git hash-object` after every restore, append-only progress log, preserved wrong-impls for batch verification, build as the only oracle (IDE Lombok false positives burned real context).

## Parallel levers added beyond the source document

The source doc batched RUNS but left the loop serial. Six parallel/wall-clock levers were added at design review:

1. **Draft-while-attacking (pipelining)** — strengthenings for already-reported units draft in scratch while a backgrounded attack continues; never mid-attack edits to real-tree test files (the attacker's screening needs a stable GREEN baseline).
2. **Concurrent Part A / Part B (`timebox`)** — A's impl-blindness is guaranteed by its input, not the sequencing.
3. **Progressive consolidated dispatch (multi-unit)** — the consolidated attacker dispatches as the final WAVE dispatches (implementers run minutes; the attacker runs 31 min+); units reached only when landed + real-tree GREEN; not-yet-landed → skip and revisit. Shrinks the v1.14.0 accepted trade (discovery delay bounded to wave-time).
4. **Drafting dispatch at ≥5 holes** — MID-tier black-box drafting (hole report + test + intent; never the impl), adoption gated on orchestrator review + the one-shot batch re-RED. I4's escape hatch refocused: the VERDICT gate stays with the orchestrator; mechanical drafting may be delegated.
5. **`timebox` degradation ladder** — concurrent A/B + merged dry-loop + attack cap 3→2, each rung disclosed.
6. **Structured hole-report file** — fixed schema (id/unit/mutant/missing case/severity/evidence), extending I19(b) to the attacker's RETURN; prose reports are how runs drown their second context.

## Observations that rode along

- **SPEC-DEFECT STOP validated**: the implementer caught a lambda effectively-final TEST bug — the asymmetric instruction works. Test-code compile health is a whole-pipeline stop point: make property-test loop variables effectively-final up front.
- **IDE diagnostics are noise**: hundreds of Lombok false positives per edit burned subagent context — "gradle is the only oracle" now rides the dispatch template.
- **Context #2 survival was luck-shaped**: the handoff worked because a state+verdicts+iron-rules brief happened to exist — C4 makes it the artifact, not the accident.

## Deliberately NOT adopted

- **Continuing the same attacker conversation** across strengthenings (independence decays — I8 unchanged).
- **Batching same-file mutants** (masking).
- **Skipping the terminal dry-loop** or extending it past its cap on non-clean rounds.
- **Weakening any verdict rule**: RED-first, exact-count attribution, hash-verified restore, orchestrator re-run (I5) all stand — the economy is in HOW runs are grouped, never in WHAT a run must prove.
- **Pinning specific gradle flags as protocol**: the flags stay examples ("your build's equivalent") — the invariant is the batching + attribution + hygiene, not the tool.

## Trial status

Text-level recognition arms: see CHANGELOG. Behavioral evidence: the source run itself (A1/A2/B/C shapes were its improvisations); next real-use runs carry the trial — watch: batched-mutant attribution accuracy at scale, drafting-dispatch review load at ≥5 holes, progressive-dispatch skip/revisit frequency, timebox rung sufficiency.
