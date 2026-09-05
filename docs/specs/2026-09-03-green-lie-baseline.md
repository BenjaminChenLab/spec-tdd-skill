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

## Retrospective trap battery (added 2026-09-03, same day)

The null result left H4 (weakening) half-answered by *spot-checks*. The **trap battery** (`oracle/green-lie/trap_battery.py`, 36 pre-registered trap impls — 3 per fixture: the Key's named trap + an adjacent variant + a clause-drop, each verified to FAIL its oracle: 36/36) converts discriminating power into a measurement: each trap is swapped into an arm's run dir and the arm's OWN acceptance test runs unchanged — KILLED = suite fails a known-wrong impl (discriminating), SURVIVED = suite passes it. An arm can be oracle-clean (correct impl) while its suite would let wrong impls through; this measures exactly that, and gives the planned adversarial arm (C) a pre-registered baseline to beat.

**Pre-registered predictions (written before any arm was run against the battery):**
- **H5:** both arms kill most traps — A ≥ 30/36, B ≥ 30/36 (the spot-checks said genuinely discriminating suites); no separation predicted — the battery's first job is measurement, not contrast.
- **H6:** SURVIVED traps concentrate in T2/T3 (adjacent variants, clause-drops) over T1 (the Key's named trap — every suite explicitly targets it).
- **H7:** survived traps cluster in the boundary fixtures (GL-01/05/10), where adjacent-boundary variants are subtlest.

Scoring runs after this paragraph was committed to the working tree; results appended below.

**Result — another ceiling: A 36/36, B 36/36 trap-kill, zero SURVIVED, zero INFRA (every restore sha256-verified; post-battery oracle re-check 24/24 both arms).** H5 confirmed at ceiling (both ≥ 30/36 — in fact both perfect); H6/H7 vacuous (no survivors to distribute). Read with the null result: on this model, small settled units with bolded classic traps produce fully discriminating suites in BOTH modes — same-context TDD and the structured tier are indistinguishable on correctness AND on mutation-kill at this difficulty. The battery's value is therefore not A/B contrast but **a mechanical floor for the standing regression rule**: any future skill change that weakens delivered suites shows up as trap-kill < 36/36 (or wrong-but-GREEN > 0) with zero judgment calls. The separating instruments must come from v2 fixtures in the untested regime (long specs, buried unbolded traps, repair pressure, multi-unit attention dilution) — where this suite already documents its own limits.

## Arm C pilot — adversarial tier end-to-end (2026-09-03, 3 fixtures: GL-01/GL-04/GL-11)

First execution of the tier's machinery as specified (C1 adversarial-grade Phase 1 → C0 → C2 → C3 attacker r1 → C1′ strengthen → harness batch-verify → fresh C3′ r2). 18 dispatches, ≈785k subagent tokens (~262k/fixture).

**Scores against the pre-registered predictions:**
- **H8 ✓** — C trap-kill 9/9 on the pilot subset (strengthened suites retain full battery discrimination).
- **H9 ✓ exceeded** — predicted ≥3/12 fixtures with ≥1 critical/moderate round-1 hole; observed **3/3**: GL-01 ×2 (bounded-purge-window moderate + pre-1970 gap weak), GL-04 ×3 (first-entry-per-user shadowing, NFC folding, str-coercion — all moderate), GL-11 ×2 (shared-`[]`-singleton moderate + int-typing weak). **7 holes, every one OUTSIDE the 36-trap battery's alphabet** — novel wrong-impls nothing else in the program caught (C0 audits passed, property tests passed, battery killed all its known traps).
- **H10 ✓** — the harness-side one-shot batch verification attributed **7/7 exactly**: each survivor's RED set fell entirely within its named closing tests, zero cross-RED into original tests, restores hash-verified, suites GREEN. (One environment note: a Unicode failure message crashes cp950 console printing AFTER the assertion fires — the kill is real, the summary line is lost; run `PYTHONIOENCODING=utf-8` to see it.)
- **H11 ✗ refuted** — measured ≈3–4× B's per-fixture cost (predicted 1.7–2.5×).

**Round 2 (fresh attackers):** GL-01 **CLEAN at the severity floor** (0 new critical/moderate; weak residuals ride); GL-04 and GL-11 NOT clean (3 new moderates each — None/`""` entry-side wildcards; retries-depth, precision, 4-buffer aliasing) — under the cap, each buys round 3; the pilot stops here by design, residuals disclosed. One GL-11 round-2 finding indicts the REAL impl too (float base overflows at retries ≥ 1025 — an IMPL-bucket finding, left as a disclosed residual in the pilot).

**The headline finding — first separation in the program.** The adversarial loop finds test-strength holes invisible to every other layer: two attackers independently reported "branch-complete but input-space holes — branch metrics cannot see them" (both suites were 100% branch-covered with zero filler). The hole shapes match the v1.15.0 taxonomy (aliasing/singleton → B1-class; narrow alphabet → B6-class; fixture-shape gaps). The A/B null measured DELIVERY (impls were correct); the attacker layer measures what the delivery score cannot: how much wrongness the suite would silently tolerate. On blast-radius-critical work that latent tolerance IS the product the tier buys.

**SPEC-DEFECT fired live (GL-04):** the C2 implementer stopped with ERR on a self-contradictory property test written by C1 (its "unrelated grants" fixture contained the probed pair, contradicting the spec's own allow rule) — production never bent; the harness (orchestrator role) corrected the test fixture, noted the correction, and the pipeline resumed. Also notable: the C0 encoding audit had passed that same test — the contradiction was internal to the fixture, invisible to spec-encoding review. I15's asymmetric instruction worked exactly as designed, end to end.

**Run deviations (disclosed):** all dispatches are harness-side stand-ins (subagents cannot dispatch subagents — same as the A/B runs); C3's Part A/B input control is enforced by sequencing discipline inside one context, not by separate dispatches; the dry-loop was out of scope per the Arm C spec; the pilot ran the base session's model, no tier pin (same fairness-over-fidelity choice as A/B).
