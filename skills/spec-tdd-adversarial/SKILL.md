---
name: spec-tdd-adversarial
description: Use when implementing a BLAST-RADIUS-CRITICAL unit — a silent wrong result MOVES money, CHANGES authorization, or IRREVERSIBLY corrupts data (money movement, auth/permissions, data-loss/data-integrity logic itself), where a subtle bug means real loss and maximum rigor is worth the token cost. Money-adjacent is NOT money-movement — display/reporting/reference-data/internal tooling that READS the money system but cannot corrupt it routes to spec-tdd-coverage or spec-tdd instead; a pre-settlement safety net (reconciliation/monitoring/dual-control) bounds the blast radius → one tier down. The highest tier above spec-tdd and spec-tdd-coverage. Requirement still FUZZY/un-grilled? Run adversarial-grill-spec-tdd first (the grill front-end: auditor on decisions pre-gate, on the final-spec test pre-dispatch); this tier starts once the requirement is grilled/settled. Triggers on critical-path, no-cost-for-correctness, hardening acceptance tests against independent attack, "this cannot be wrong".
---

# spec-tdd-adversarial

**REQUIRED BACKGROUND:** Understand `spec-tdd` and `spec-tdd-coverage` first. This is spec-tdd-coverage with a mandatory independent ATTACKER layered on — it inherits the two-tier agent-boundary split, "must be RED first," the case-list, per-class branch coverage, and Phase-3 don't-trust-self-report.

## Overview

spec-tdd-coverage, plus: an **independent adversarial subagent** — a *third* context, not the orchestrator, not the implementer — tries to (a) write a subtly-WRONG impl that still passes the acceptance test, and (b) independently gap-check every branch of the real impl. Property/invariant tests become **mandatory**.

**Core principle: independence is the one thing a diligent same-context agent cannot give itself.** A baseline agent told "maximum rigor, spare no cost" wrote 30 scenario tests, a differential-oracle fuzz harness that caught a real bug, and an "adversarial self-review" — all excellent, all in ONE context. It never dispatched an independent attacker; that move is non-obvious. spec-tdd-coverage's Phase-3 checks run in the orchestrator's context (biased to rubber-stamp its own test), and the implementer's unit tests share context with the impl. An independent attacker removes both biases.

**The acceptance test is done when the attacker can no longer construct a wrong-but-green impl** — bounded by the **attack-loop circuit breaker** (3 rounds, or the same hole twice): a critical surface is rich enough that "no wrong-but-green impl exists" may never hold, so past the breaker you surface the residual risk to the human instead of looping. Until then, it isn't "clean done" — but it can be "done enough to ship, pending human accept".

**Attack economy — the loop's verdicts come from build runs, and the build run is the cost.** Measured on a real critical fix (~340 lines, 3 attack + 3 repair rounds): one mutant per full-suite run ≈ **27 min per file per round**; the same work batched (cross-file mutants applied together, one run, attribution by which test goes RED) closed **9 mutants in 16.5 min**; batched strengthen verification closed **20 holes at 1–2 runs per repair round**. Phase 3 steps 3–4 make batching the default — without weakening one verdict: every strengthening still proves teeth by going RED, every restoration still proves byte-exactness by hash, every re-run stays the orchestrator's own (I5).

## When to Use
- Blast-radius-critical units ONLY: a SILENT wrong result here moves money, changes authorization, or irreversibly destroys/corrupts data — money movement, auth/permissions, data-loss/data-integrity logic itself. Equivalently: the unit's spec carries an IRREVERSIBLE blast-radius tag from the grill gate (I12).
- **Money-adjacent is NOT money-movement** — the over-routing trap (observed: a fintech codebase routed nearly everything here): display / reporting / reference data / internal tooling READ the money system but cannot corrupt it → `spec-tdd-coverage` (branchy/compliance) or `spec-tdd`. A pre-settlement safety net (reconciliation, monitoring, dual-control) catches wrongness before it settles → one tier down. Multi-unit batches route PER UNIT: the payments batch's movement units here, its statement/display units coverage.
- The user says `spec-tdd-adversarial`, "no cost for correctness," or "this cannot be wrong."
- Otherwise use `spec-tdd` (general) or `spec-tdd-coverage` (coverage matters). This tier dispatches multiple agents per unit — don't burn it on glue/CRUD.
- Requirement still fuzzy/un-grilled on this blast-radius-critical surface? `adversarial-grill-spec-tdd` (the front-end) grills + audits it first, then arrives here as a grill arrival.
- **What this tier costs (measured — state it when the user is deciding):** ≈ **1 h per 60 lines** of production change; each attack-repair cycle **45–60 min**; a real ~340-line critical fix ran **6+ h across 2 contexts** (21 → 195 tests). "No cost for correctness" holds — the bet is worth it exactly when the blast radius is real, which is why the litmus above routes only true money-movement/auth/data-loss here.
- **`dryout` flag** (`/spec-tdd-adversarial dryout <feature>`): args containing the token `dryout` raise the Phase-3 dry-loop cap from 2 to 5 rounds — the ONLY difference; every other rule identical. Strip the token from the feature description.
- **`timebox` flag** (`/spec-tdd-adversarial timebox <feature>`): args containing the token `timebox` mark a time-constrained run and adopt the **degradation ladder** — (a) attack Parts A and B dispatch CONCURRENTLY (step 3), (b) the terminal dry-loop runs as ONE merged round (step 5), (c) the attack-loop cap drops 3 → 2. Each rung is disclosed in the final report; every verdict rule (RED/GREEN, hash, breaker semantics) is untouched. Strip the token from the feature description.

## Pre-flight — orchestrator tier check (I21)

Before any work, check the model THIS session runs as. A run's judgment — the test/spec, the verification, the failure routing — executes entirely in the orchestrator's own context; I19 pins every dispatch tier, but nothing can upgrade the session itself. **Top tier in use, or no higher tier exists → silent, move on.** Otherwise surface this ONE ask and stop for the answer:

> ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

Arrived from a front-end that already surfaced this check? Skip it — never re-ask (a handoff-recorded decline rides into your final-report disclosure).

## The 3 Phases (delta vs spec-tdd-coverage in **bold**)

### Phase 1 — Orchestrator writes the acceptance test
> **Arrived from `grill-spec-tdd` / `adversarial-grill-spec-tdd`?** The acceptance test is already written, RED, and encoding-audited — skip to Phase 2, but ENSURE the mandatory property/differential tests below exist (add them if the front-end didn't). Direct arrival (no front-end): run spec-tdd's Phase-1 **encoding audit** before dispatch (the Phase-3 attacker is post-GREEN and asks a different question — wrong-but-green impl — it does not replace the pre-dispatch encoding check).

As spec-tdd-coverage: ground it, behavioral black-box, MUST be RED (incl. the RED-purity check — scan the FULL error list; errors about EXISTING symbols are a defect in YOUR test), note the branch/exception surface — and spec-tdd's **spec-doc persistence prompt** applies (no spec/plan/blueprint doc → ask once, default YES; adversarial-grill arrivals already persisted the final decision spec at the gate). PLUS:
- **Property/invariant tests are MANDATORY** (money conservation, net-zero, monotonicity, no-silent-loss). Where an unbiased oracle exists (e.g. `BigInteger` for integer money), write a **differential property test**: random inputs, assert your result equals the oracle's. Oracles catch bugs hand-written cases miss.
- **Hole-class self-check (pre-dispatch)** — scan the acceptance test + its fixtures against the seven hole classes below before dispatch. Measured: on the run that produced this checklist, **13 of 20 attack-round holes were these classes** — each one costs an attack round (45–60 min) to discover late. (Rules stated tool-agnostically; examples are the Java/Mockito shapes they were measured in — instantiate for your stack.)
  1. **Mutable-state assertion** — asserting on a live object inspected AFTER the call cannot distinguish pre-call from post-call processing (an argument-captor's live reference mutates). Snapshot AT call time: deep-copy inside the stub's answer (`doAnswer`), assert on the snapshot.
  2. **Mocked-out funnel** — wrongness inside a mocked funnel passes green. Every production funnel the spec cares about gets ≥1 **wiring test** driving the REAL method (e.g. assert the state actually saved).
  3. **Entry wiring untested** — a public entry that silently drops its internal call stays green when only the package-private seam is tested. Drive the PUBLIC entry.
  4. **Fixture-shape gating** — a bare fixture lets production gates (`if (type != null)`, `if (missionId == null)`) bypass the branch under test. Fixtures are **production-shaped**: every production-required field set. The cheapest fix, the highest kill rate.
  5. **Structural equality erases identity** — `deepCopy` + `equals` cannot see aliasing. Where identity matters: `identityHashCode` / `assertNotSame`, pairwise on nested subtrees.
  6. **Property alphabet too narrow** — a generator over synthetic keys never exercises the production key names. Generators must include the real keys.
  7. **Copy depth** — a two-layer copy passes a literal deep-copy test when the spec means deeper. Recursive no-alias oracle + depth ≥3 generators.
- **Seed the attacker**: list the wrong-but-plausible impls you most fear ("silently wraps on overflow," "skips nulls and nets the rest," "accepts mixed currency"). The seven hole classes above ride as default seeds too — round 1 should try the highest-yield classes first, not rediscover them.

### Phase 2 — Delegate implementation to a subagent
Unchanged from spec-tdd-coverage: case-list BEFORE impl, acceptance test GREEN, unit tests red→green, per-class branch coverage with uncovered-line justifications — handoff carries the SPEC-DEFECT STOP clause (a defect in the TEST itself → the implementer reports SPEC-DEFECT — the correct outcome, not a failure to implement; production changes that exist solely to accommodate a test defect = a FAILED run; an arity/signature error on a symbol the requirement itself explicitly changes is NOT a test defect). The attacker is a THIRD party — not involved here.

### Phase 3 — Orchestrator verifies + dispatches the attacker
spec-tdd-coverage's checks (so SPEC-INTEGRITY holds: re-hash A2 == A4 BEFORE dispatching the attacker; the implementer must NOT edit the acceptance test, and the attacker writes a separate wrong-impl and must not edit it either; only YOU may strengthen it — always through the batch verification below), but REPLACE the orchestrator's self gap-check with an independent attacker:
1. Run the acceptance test + property tests yourself. Must be GREEN. (Property tests must have been RED before impl — else tautologies.)
2. **SPEC-DEFECT sweep** (from spec-tdd Phase 3): diff the returned production changes against the spec/plan — the subject is changes to code this dispatch did not create; the tell is a change no production behavior needs, existing only to satisfy the acceptance test (helper/compat constructors, renamed public methods, logic beyond what the spec asks for). Any accommodation → fix the acceptance test (your artifact: correct it, re-hash, note the correction) and restore production to the spec'd shape. Do this BEFORE dispatching the attacker — Part A attacks test strength and Part B hunts branches; neither diffs production against the spec.
3. **DISPATCH THE ADVERSARIAL SUBAGENT — TOP-TIER model** (independent context; review at attack grade — I19 names the top tier for every review/attack dispatch), from this template:

   ```
   TASK: Attack an acceptance suite. You are an INDEPENDENT attacker — you did not write
   the test or the impl; independence is your entire value. TWO PARTS, in order:

   PART A — TEST-ATTACK. Input: the acceptance suite + each unit's INTENT. NOT the real impl.
     Write subtly-WRONG impls that still pass the test. CONSTRUCT AND RUN each one — an
     opinion is a rubber-stamp. If one passes, report EXACTLY which missing case let it
     through (one line, the acceptance case that would kill it).

   PART B — BRANCH-HUNT. Input: the suite + the real impl.
     List every branch (if/loop/null-guard/early-return/catch/boundary); mark each
     Covered/Uncovered with its case. Report any branch with no case — and any case that
     maps to no branch (filler).

   RUN ECONOMY — the build run is the unit of cost; batch it:
     - Mutants batch ACROSS independent files/units: apply the batch, ONE build run,
       attribute by WHICH test goes RED (each mutant is paired to the one test that
       closes it — design them so). NEVER batch two mutants in the same file: they mask
       each other (a false CAUGHT or a false HOLE). Same-file mutants run sequentially.
     - Screening runs only the related 2–3 test classes (e.g. gradle --tests filters or
       your build's equivalent); a mutant that survives its screen is confirmed on the
       FULL suite before it counts as a hole.
     - Compress run output (gradle form: -q --console=plain | tail -5; use your build's
       equivalents); full output goes to your scratch log, status lines only in the report.

   HYGIENE — this tree carries uncommitted work:
     - Byte-exact restore: file-copy backup BEFORE mutating; restore by copying back.
       NEVER git write operations (stash/checkout can destroy never-committed units —
       read-only git like `git hash-object` is fine).
     - `git hash-object` after EVERY restore — it must equal the pre-mutation hash.
     - Preserve every wrong-impl + its backup under .spec-tdd/attack/round-N/ — the
       orchestrator re-applies them for batch verification.
     - Progress log: APPEND one line per experiment/unit (never rewrite the file).
     - The BUILD is the only oracle — IDE diagnostics (e.g. Lombok false positives) are
       noise, never evidence.

   RETURN: a HOLE REPORT file (.spec-tdd/attack/round-N-holes.md), one row per hole:
     id | unit/file | mutant (path + one-line description) | missing acceptance case (one
     line) | severity (critical / moderate / weak) | evidence log path
     + Part B's branch table + one status line per build run. Never pasted logs.
   ```

   - **Part ordering:** one dispatch, Part A then Part B (one grounding pass serves both). **`timebox`:** dispatch A and B as TWO CONCURRENT dispatches — A's impl-blindness is guaranteed by its INPUT (suite + intent only), not by the sequencing; the cost is one extra grounding pass, the saving is half the wall-clock.
   - **Long-dispatch visibility (I19(e)):** the attacker is the run's longest dispatch (measured round-1: ~31 min on one unit; the consolidated multi-unit attack longer). Narrate ONE line to the user AT DISPATCH — what is attacked, which round of the cap, the expected duration. Where the harness supports background dispatches, run it backgrounded and instruct it to APPEND one progress line per unit to its evidence log as it completes each unit; poll every few minutes and relay a line per unit (no background support → the narration alone stands, degradation disclosed in the final report — never a silent multi-hour block). The per-unit progress lines are also your pipelining signal — step 4.
4. **Act, then loop — bounded by an attack-loop circuit breaker (mirrors the implementer's repair cap):**
   - **Severity floor (mirrors the dry-loop's):** only a **critical/moderate** hole opens the next re-attack round. Weak / contract-nitpick / spec-letter holes ride the residual list — they never buy a round (every round is a fresh TOP dispatch; a weak hole spending 45–60 min is the measured waste). Batched holes from one round count once — the round is one unit of investment.
   - **Draft while the attack runs (pipelining):** where the attacker is backgrounded, begin DRAFTING strengthenings for units whose holes have already reported — in scratch. NEVER edit the real tree's test files while an attack dispatch is live: the attacker's screening needs a stable GREEN baseline, and a half-written test under its hands reads as a false verdict. Apply the drafts when the dispatch returns.
   - **Strengthen:** the strengthenings are yours to write — or, at **≥5 holes in a round**, dispatch a MID-tier drafting subagent (input: the hole report + the acceptance test + intent; **BLACK-BOX — never the impl**) and review every assertion before adoption. The verdict gate never leaves you: review + the batch verification below are what keep the teeth (I4's escape hatch is the re-RED'd step, not literally your keystrokes).
   - **One-shot batch verification (replaces per-hole RED→GREEN, same guarantee):** apply the round's N preserved wrong-impls TOGETHER → ONE run → expect **EXACTLY the N new/strengthened tests RED** (each mutant ↔ its closing test; that is the attribution proof). Same-file mutants apply sequentially even here — the no-same-file-batch rule is absolute (masking). A count mismatch or an unexpected cross-RED = attribution failed → fall back per-mutant for the affected file only. Then restore byte-exact (file-copy), `git hash-object` verify, and run the full suite GREEN. A strengthened test that goes RED against the REAL impl was never a test hole — it caught an impl bug: route IMPL (I10), re-delegate (batched where several). Measured: 20 holes across 3 repair rounds at 1–2 build runs each.
   - **Each re-attack is a FRESH dispatch — never a continued conversation with the previous attacker:** it has now seen your strengthenings, its context is contaminated, and round 2 of the same context goes soft with ownership bias ("they fixed my findings"). The breaker's objective standard (below) already judges "same hole" across contexts.
   - **STOP when EITHER fires:** (i) **3 attacker rounds** run (`timebox`: 2), OR (ii) **the same hole on any two rounds** — judge "same hole" objectively: the same missing acceptance-test case re-failing (the case you wrote to close it is bypassed again), NOT a rephrased wrong-impl description. Mirrors the implementer breaker's objectivity (file:line + assertion, not free text).
   - **A user-lifted cap ≠ silent unbounded grinding:** when the human lifts the round cap, every round STILL reports its trail (round #, holes found/closed, residuals, elapsed time), and a NEW critical finding mid-loop returns to the human to confirm the investment before the next round dispatches. Lifting the cap licenses more rounds, not less reporting.
   - **Done clean** = the attacker cannot construct a wrong-but-green impl (the bar) — AND the terminal dry-loop (step 5) has dried. **Done enough** = the breaker fires with a residual hole → STOP and surface to the human: test hardened across N rounds + property/differential tests + the attacker's final report + the **residual risk** (remaining hole(s) + the weak-hole residual list); the human decides accept vs. further harden. Never loop past the breaker — a correctness-critical surface always has one more boundary.
5. **Terminal dry-loop audit (fresh contexts, rotating lenses, TOP-TIER model — I19).** The attacker loop passing is NOT done: one lens misses things another lens sees (observed: a passed attack loop, then a post-run fresh audit landed two deployment-lens BLOCKERs and two test-strength MAJORs). Dispatch independent read-only auditors, ONE lens per round, rotating. Hand each auditor FILES, not pastes (I19): the spec doc path (A15 — the fidelity lens's plan of record) + the diff/scope under audit (a declined or never-written spec doc falls back to paste — I19(c)):
   - **test-strength** — wrong-but-green impls the attacker didn't construct; deleting error handlers must break something.
   - **spec/plan fidelity** — impl vs the locked plan, clause by clause; intermediate-failure and recovery promises included.
   - **deployment/ops** — migration windows (old code × new schema; new code × old schema), environment-gated components, and for EVERY runtime object: how does it come to exist in EACH target environment? Ops docs/runbook claims true?
   - **production quality** — error handling, lifecycle convergence (does every state settle or does anything poll forever?), dead code, unused mocks.
   **Dry-loop breaker:** every round is a **FRESH subagent** (one lens per round, rotating). A round with ZERO BLOCKER/MAJOR findings (deduped re-finds don't count) is **CLEAN → stop there — both modes**. Otherwise dispatch the next round, up to the cap: **2 rounds** default, **5 with the `dryout` flag** (the flag's only difference). MINORs ride the report; they never extend the loop. Every adopted finding → fix → re-run the relevant verification (strengthened test → RED→GREEN or the step-4 batch form; impl fix → repair path) → next round. A finding whose fix requires deciding something the plan doesn't decide → the human (I12), never silently. **Cap hit and not yet clean → STOP and ASK the human (both modes):** "N rounds run, findings still emerging — continue hunting or stop here?" A yes grants exactly ONE more round — if it still finds, ask again; a clean round or a decline ends it. Frame the non-convergence as a signal, never a grind: (a) fixes are superficial — each round's fix is manufacturing new issues; (b) one lens category keeps producing findings — the lens list may be missing one; (c) the unit is too big and should be split. "No auditor can find anything" is prove-a-negative and is NEVER the bar — one clean round is. Dry-loop rounds are long dispatches too — same I19(e) visibility: narrate at dispatch, background + relay where supported.
   **`timebox` merged mode:** instead of the rotation, ONE round with ONE auditor covering **deployment/ops + spec/plan fidelity** over the full diff (the two lenses the attack loop does NOT already do — test-strength is the attack loop's own job; production-quality rides as MINORs unless a critical surfaces). Same severity floor, same clean-round rule, same disclose-the-degradation.
6. Surface to the user: acceptance test + property/differential tests + the attacker's final report + the dry-loop rounds' findings and residuals (not the impl).

## Run ledger (A16) — compaction-proof state

A full attack loop outlives one orchestrator context — measured: the 6 h run survived across TWO contexts, and what survived was the ledger, not memory. Keep the batch ledger (A16) as a **run ledger**: an append-only scratch file (e.g. `.spec-tdd/run-ledger.md`), one row appended at every phase/round boundary — phase, verdict, hash, holes opened/closed, residuals, elapsed — plus the loop's standing **iron rules** verbatim (byte-exact restore, no git writes, severity floor, breaker counts, timebox rungs). Written-ahead continuously, never reconstructed at handoff: a fresh context reads it and RESUMES (a row with no verdict = in flight — re-verify, don't blindly redo). Cross-context survival is by design, not luck.

## Multi-unit batches — consolidated attack

A batch of critical units (spec-tdd's Multi-unit loop routes each unit here, per unit) does NOT run a full attack loop per unit: per-unit cycles scale badly — measured on a real 6-unit money-movement batch, sequential full cycles projected 5–8 h wall-clock (one round-1 attacker dispatch alone ran ~31 min), and rounds 2–3 per unit mostly re-tread files a fresh whole-surface attacker covers anyway.

- **Per unit, unchanged:** Phase-3 steps 1–2 (re-hash, your own re-run GREEN, SPEC-DEFECT sweep) run per unit inside the multi-unit loop — a unit merges back only on its own green evidence, in the real tree.
- **Consolidated, dispatched as the FINAL WAVE dispatches (not after it merges):** the attacker works unit-by-unit in dependency order — by the time it reaches the last wave's units they are landed + real-tree GREEN (measured: an implementer ~5 min ≪ an attacker 31 min+). A unit NOT yet landed when reached is skipped and revisited at the end — never attacked half-landed. **Part A:** the full suite + every unit's intent, NOT impls, reporting per unit; **Part B:** branch-hunt per file cluster (one attacker per serial-chain cluster, one for the disjoint islands). This is the run's longest block — I19(e) visibility applies throughout: per-unit progress lines relayed during the block, not an end-dump.
- **Breaker — same circuit breaker, judged PER HOLE:** "same hole" = the same unit's missing acceptance-test case re-failing; a hole re-failing parks THAT unit's hole as its residual — other units' holes don't burn its rounds. The 3-round cap spans the consolidated loop. Per-unit residuals surface in the batch summary.
- **The accepted trade (smaller than it was — wall-clock over earliness):** consolidation delays hole discovery until downstream units have landed on the upstream code the hole lives in; the final-wave overlap bounds that delay to wave-time rather than whole-batch-time. Repair is the normal loop — strengthen → batch-verify (step 4) → re-delegate where IMPL → GREEN — then re-run the DOWNSTREAM units' acceptance specs against the fixed code (independent oracles; usually still green). Traded knowingly.
- **Terminal dry-loop: consolidated too** — one rotation over the whole batch's diff; same lenses, same severity floor, same cap, same ask-the-human on a non-converging cap (`timebox`: the merged mode over the whole diff).

## Risk-tier
This IS the top tier: blast-radius-critical units get full phases + mandatory property/differential tests + the attacker loop until unbroken OR the attack-loop circuit breaker fires (3 rounds / same hole twice; severity-floored) — then surface residual risk. Below critical → use `spec-tdd-coverage` or `spec-tdd`; not this skill.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Orchestrator or implementer does the adversarial review itself | Independence is the entire point. It MUST be a separate agent that never saw the test or impl being written. |
| Attacker sees the real impl before test-attacking | Give ONLY test + intent for Part A; impl only for Part B. |
| Attacker opines "test looks fine" without attempting a wrong impl | Require it to construct (and run) a wrong impl, or enumerate concrete codeable wrong-impl strategies. An opinion is a rubber-stamp. |
| Property test is a tautology ("result not null") | Require a real invariant or a differential oracle. Tautologies are green lies. |
| Strengthened test not re-run RED | After any strengthening, prove teeth via the step-4 batch verification: N mutants applied → exactly N RED → restore → hash → GREEN. No run on record = not strengthened. |
| Two mutants in the same file batched together | They mask each other — one short-circuits the other (false CAUGHT / false HOLE). Batch across files/units only; same-file mutants run sequentially. |
| Mutant "survived" its focused screen and was reported as a hole | A hole is confirmed on the FULL suite first — a distant test your screen skipped may already kill it. |
| Restore "looks right", no hash on record | `git hash-object` after EVERY restore, matching the pre-mutation hash — a mutant left behind contaminates every later verdict. |
| One-shot RED count mismatch waved through | EXACTLY N tests RED is the attribution proof. A mismatch (or a cross-RED) = fall back per-mutant for the affected file. |
| Attacker restored via git stash/checkout | The tree carries uncommitted units — git write operations can destroy them. File-copy backup → copy back → hash-verify. |
| A weak / contract / spec-letter hole opens a re-attack round | Severity floor: only critical/moderate buys a round. Weak holes ride the residual list; they cost 45–60 min each as rounds (measured waste). |
| The user lifted the cap → grinding rounds silently | Every lifted-cap round reports its trail (holes/closed/residuals/elapsed); a new CRITICAL asks the human before the next dispatch. |
| Orchestrator edits the real tree's test files while the attack dispatch is live | The attacker's screening needs a stable GREEN baseline. Draft in scratch; apply when the dispatch returns. |
| Hole report arrives as pasted prose | Structured file, fixed schema (id / unit / mutant / missing case / severity / evidence) — the orchestrator reads the table. Prose reports are how a run drowns its second context. |
| Drafting dispatch handed the impl, or its output adopted unreviewed | Black-box in (hole report + test + intent); orchestrator review + one-shot batch RED out. Otherwise it's a fourth author with no gate. |
| Progressive consolidated attack reaches a half-landed unit | Skip and revisit — a unit is attacked only when landed + real-tree GREEN. |
| `timebox` rungs applied silently | Each degradation (concurrent A/B, merged dry-loop, cap 2) is disclosed in the final report. |
| IDE diagnostics treated as test evidence | The BUILD is the only oracle — an IDE's Lombok false positives flooded a real run's context with hundreds of phantom errors. |
| Attacker loop runs past 3 rounds, or re-finds the same hole | The attack-loop circuit breaker (mirrors the implementer's) caps it: 3 rounds OR same hole twice → STOP and surface residual risk + the attacker's report to the human. Don't chase a moving target on a rich surface. |
| Re-attacks by continuing the same attacker conversation | Each round is a FRESH dispatch — the previous attacker has seen your strengthenings; its independence decays and it rubber-stamps its own fixed findings. |
| "The attack loop passed — done" | Step 5's terminal dry-loop exists because one lens misses another's findings (deployment/ops BLOCKERs survived a passed attack loop). Rotate lenses; stop at one clean round (capped at 2; 5 with `dryout`). |
| Dry-loop extended by MINOR findings | Severity floor: only BLOCKER/MAJOR (not deduped re-finds) opens the next round. MINORs ride the report — otherwise you audit the auditor's taste forever. |
| Dry-loop runs unbounded "until nobody finds anything" | Prove-a-negative; that is why ONE clean round stops the loop (capped at 2; 5 with `dryout`). Bounded dry, not exhaustion. |
| Cap hit with fresh findings still coming → residuals surfaced, called "done" | STOP and ASK the human whether to continue (both modes). Non-convergence is a signal — superficial fixes / a missing lens / an oversized unit — never something to grind through or wave off. |
| Used on non-critical work — or on everything money-ADJACENT | Blast-radius-critical units only (When to Use): an always-on top tier is pure token waste AND deafens the human to its residuals (I12 — signal fatigue is how gates die). |
| Skips the SPEC-DEFECT sweep — "the attacker will catch it" | The attacker attacks the TEST (Part A) and hunts branches (Part B); neither diffs the real production changes against the spec. Sweep first — a compat ctor passing green is a bent production, not a passing spec. |
| Attacker or dry-loop auditor dispatched MID-tier "to save tokens" | I19: every review/attack dispatch is TOP-tier — the economy levers are the implementer dispatch, file-based evidence, and batched runs (I19(f)), never the verifier's tier. |
| Full attack loop + dry-loop per unit on a multi-unit batch | Consolidate: per-unit Phase-3 steps 1–2 only; the attacker + dry-loop run ONCE (dispatched as the final wave dispatches; breaker per hole). Per-unit full cycles are the measured 5–8 h trap. |
| Consolidated breaker treats the batch as one hole-space | Judge per hole: the same unit's missing case re-failing parks THAT unit's residual; other units' holes don't burn its rounds. |
| Multi-hour silent attack block — the user can't tell work from a hang (observed: 3 h read as stuck, output trickling every ~10 min) | I19(e): narrate what/round/duration at dispatch; background the attacker where supported and relay per-unit progress from its incremental log. |

## Red Flags — STOP
- Adversarial step done by the orchestrator or the implementer.
- Attacker returns a verdict with no attempted wrong-impl and no branch list.
- Property/differential tests absent or trivially tautological.
- A hole was found but the test was not strengthened and re-attacked.
- Mutants batched within one file; or a restore with no matching `git hash-object` on record.
- A strengthening adopted with no batch-verification run on record (N applied → exactly N RED → restore → hash → GREEN).
- A weak hole opened a new attack round — or a lifted cap is grinding rounds with no per-round trail.
- The attacker loop is still running past 3 rounds, or the same missing case re-failed after you closed it. (STOP — attack-loop circuit breaker; surface residual risk to the human.)
- Real-tree test files changed while an attack dispatch is still running.
- About to declare done with no terminal dry-loop on record — or the dry-loop is being extended by MINORs, or re-finding a deduped known residual — or the cap was hit with live findings and the human was never asked.
- A multi-unit batch is running (or about to run) a full attack loop + dry-loop per unit — consolidate (dispatch as the final wave dispatches) instead.
- Used on non-critical code — or on the whole fintech codebase because everything touches money.
