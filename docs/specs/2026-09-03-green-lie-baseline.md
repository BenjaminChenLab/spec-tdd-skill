# Green-lie baseline — wrong-but-GREEN benchmark, first run (null result)

**Date:** 2026-09-03 · **Suites:** [`docs/fixtures/green-lie.md`](../fixtures/green-lie.md) (12 seeded-trap fixtures, oracles pre-registered at [`docs/fixtures/oracle/green-lie/`](../fixtures/oracle/green-lie/)) · **Scope:** docs-only experiment; no skill files touched.

## Hypothesis

The family's headline claim is that separating test-authoring from implementation (the agent boundary) prevents the green lie — GREEN-on-own-suite but wrong-on-requirement. Pre-registered (H1): same-context TDD (arm A) lands 3–6/12 wrong-but-GREEN; the spec-tdd base-tier structure (arm B) lands 0–2/12. H2: boundary traps catch A hardest. H3: B's own failures concentrate in ambiguous boundary fixtures. H4: A's suites assert fewer clauses.

## Method (summary — full runbook in the suite doc)

12 seeded-trap fixtures (boundary / subtle / fail-closed), one settled 5-line requirement each, pinned API, Python 3.7 stdlib. Arm A = ONE fresh subagent practicing same-context TDD (write test first, iterate freely). Arm B = the skill's causal structure via staged blind dispatches: B1 test-author (RED against a `NotImplementedError` stub) → B0 independent encoding audit (read-only; one strengthen round allowed) → B2 implementer (read-only contract, ERR-not-edit). Same model both arms (no pin — fairness over tier fidelity; context separation ≠ model diversity). Scoring: harness re-runs each arm's own suite, then a hidden pre-registered oracle; wrong-but-GREEN := GREEN ∧ ¬ORACLE. Oracle self-test before any dispatch: 12/12 known-good references pass, 12/12 known-trap implementations caught (one answer-key ambiguity found and amended pre-dispatch: GL-09 zero-caps per-slot shape).

## Result

**Wrong-but-GREEN: A 0/12, B 0/12 — H1 refuted; H2 refuted (boundary traps caught no A arm); H3 vacuous (B never failed); H4 half-confirmed** (B suites deeper — property/oracle sweeps on 10/12 vs A's 2/12, RED-purity scans 12/12 — but A asserted every trap clause too, so no clause-drop weakness at this scale).

48 dispatches (~1.2M subagent tokens; B ≈ 3× A's cost per fixture). All 24 own-suites GREEN on harness re-run; all 24 oracles PASS. B0 audits 12/12 PASS with zero strengthen relays; zero B2 ERR stops; circuit breakers never engaged. A self-caught two of its own wrong test expectations (GL-02, GL-06).

Run deviations disclosed in the suite doc: three 429 retries (A/GL-04's dir touched by two contexts — test from the killed dispatch, verified and kept by the retry); B1's in-skill encoding audit ran harness-side (no dispatch tool in subagent containment) with B1s disclosing same-context fallback re-reads.

## What this does and does not tell us

- **Does NOT show** that same-context TDD green-lies here — on this model, greenfield single-function units with settled, cue-bolding 5-line specs and classic seeded traps, a careful same-context TDD agent gets it right and writes genuinely discriminating tests. Any claim that the agent boundary is needed *for units like these* would overclaim this evidence.
- **The regime where the green lie lives was not reached:** long specs with unbolded buried traps, fuzzy requirements (the grill front-ends' beat), attention dilution across multi-unit batches, repair-loop pressure. That is where the family actually spends its machinery — and where a v2 of this benchmark should aim (domain-camouflaged traps, 1–2 page specs, induced repair pressure, an adversarial-tier arm).
- **What survived:** the *method* (pre-registered oracles + self-test, blind staged arms, mechanical scoring) works end-to-end and is reusable; and the structural disciplines did visibly fire — B's RED-purity scans, interpretation disclosures, undecided-contract refusals, deeper property-based suites — they bought depth, not correctness, at 3× cost on these fixtures.

## Limits

Single maintainer; single base model in both arms; N=12; traps authored by the skill's maintainer (authorship bias direction: favors finding A failures — the null therefore runs *against* that bias, which strengthens it); arms had repo access behind an explicit containment instruction (same residual risk as the routing suite); fixture language pinned to small Python units.

## Verdict

Honest null: the benchmark is valid (oracle self-test discriminates) and the machinery ran clean, but these fixtures sit below the green-lie threshold for this model. Keep the suite as the reusable harness; design v2 to attack attention and ambiguity rather than reflex-tested boundary classics.
