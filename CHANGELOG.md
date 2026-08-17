# Changelog

All notable changes to the `spec-tdd` skill family are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2026-08-17

Multi-unit runs: the agent boundary moves from per-feature to **per unit**. A bug batch (lite ×N in-session) drowns the main context one inner loop at a time; a mega-dispatch moves the drowning into the implementer and makes the circuit breaker all-or-nothing. The fix is not a new tier — `spec-tdd` loops its existing 3 phases per unit, and routing becomes honest about single-unit vs multi-unit. Invariants don't change; their granularity does.

### Added
- **`spec-tdd` — Multi-unit runs section.** Unit = one independently-testable behavioral slice (bug: its repro test = the acceptance spec; feature: vertical slices — standalone infra units are forbidden, they have no black-box spec; pure refactor = one unit with characterization tests). One gate up front on the unit plan + specs writable now (bug batch: all repro tests RED — a control case asserting still-correct behavior may pass pre-fix; feature split: first unit's — later specs just-in-time); gate defers (not skips) when running as a subagent; escalate stays no-ask. Loop per unit/group: Phase 1 → dispatch (hash per unit spec) → Phase 3 verify; a critical/branchy unit runs its phases at the higher tier's verification depth inside the loop. Breaker per unit — a stuck unit parks, the batch continues; a tripped grouped dispatch gets split. Disclosed no-dispatch degraded path: per-unit spec/RED then **fix one unit → its spec GREEN → next** ("tiny disjoint fixes" is the rationalization, not the exception); solo re-RED replaces the hash. Baseline-confirmed (a fresh agent on a 5-bug batch, v1.3.0: no skill owns the batch → improvised a spec-tdd/lite hybrid, ONE mega-edit for all five fixes, one monolithic suite, hash recorded post-implementation) and verify-confirmed over three refactor rounds — round 1 exposed a recognition failure (the section existed, the agent never engaged it: batch → "one feature"), closed by a When-to-Use count rule, a Phase-1 mega-collapse tripwire, and a section-opening "more than one bug/fix = you are here"; rounds 2–3 tightened per-unit green into a sequence and counters for the combined-edit excuse; the dispatch path (unit plan → per-unit RED+hash → grouped dispatch → re-hash/re-run/diff-scan → batch summary) was executed end-to-end with zero improvisation.
- **`spec-tdd` — Phase-2 no-dispatch fallback** (single unit → the `spec-tdd-lite` pattern; a batch → the Multi-unit degraded path — don't improvise a protocol), and **Phase-3 constants-correction rule** (an expected-value correction is legitimate only justified against the requirement, never "to match what the impl returns"; disclose it).
- **`PROTOCOL.md`**: artifact **A13** (unit plan — units, order/grouping, which specs writable now vs just-in-time), per-unit column notes on A2/A3/A4/A9, and a multi-unit scope note (I1–I5, I9, I10 per unit; I12 = one gate on the unit plan). No new invariant — granularity change only.
- `spec-tdd` Common Mistakes: the batch row (mega-dispatch / lite ×N → per-unit loop) and the combined-edit row ("tiny and disjoint" → per-unit green is the boundary).

### Changed
- **Routing honesty at three sites.** "bugfix-scale → lite (delegation overhead would dominate)" was true only for an isolated single unit — a repro-test-first bug dispatch is cheap (failing test + trace = minimal grounding). `grill-spec-tdd`'s route list, `spec-tdd-escalate`'s route table, and `spec-tdd`'s When-to-Use now split **one small unit** (→ lite, session cleared after) from **multiple units** (→ `spec-tdd` multi-unit). `spec-tdd-escalate` mistakes table gains the bug-list row.
- **`spec-tdd-lite` re-scoped honestly.** ONE unit in a session you'll clear/compact after; a SECOND unit → switch to `spec-tdd` multi-unit. The gives-up ledger now names the third cost: the inner loop stays in the main context. Common Mistakes gains the lite ×N row.
- README: version, family table, decision tree (one unit vs multiple), rule of thumb, walkthrough batch line, and the SDD comparison (multi-unit closes the cadence gap at executable-verification strength).

## [1.3.0] - 2026-08-17

Adds `spec-tdd-lite` — the in-session entry tier: acceptance-test-first written **and implemented in the same session**, then **one fresh-context review dispatch**. Fills the gap between bare TDD and full delegated `spec-tdd`: small/non-critical work where delegation is overkill but shallow same-context tests are still a risk. Zero `superpowers` dependency — a distilled red-green-refactor loop is inlined.

### Added
- **`spec-tdd-lite`** (skill). Phase 1: acceptance test, must-be-RED (a not-yet-existing module erroring is a valid first RED), interpretation notes taken. Phase 2: in-session inner loop — RED verified personally (an unverified ordering *claim* is the baseline failure), minimal GREEN, fix code not test. Phase 3: ONE dispatch to a reviewer that saw none of the implementation reasoning, answering two questions with concrete cases — test-vs-impl ("name a subtly-wrong impl that still passes") and test-vs-requirement (requirement pasted verbatim; silent interpretations surfaced to the human). Exit rules: **solo re-RED** (any post-impl test edit re-confirms RED — the discipline replacement for the hash), **stall breaker** (3 attempts / same root cause twice → promote to full `spec-tdd` or ask the human), **surface WHAT**. Disclosed degraded mode where no dispatch tool exists (mutation checks + requirement-line audit) — never a silent improvised review. Grill-arrival note: skip Phase 1 when routed from `grill-spec-tdd`. Baseline-confirmed (a diligent plain-TDD agent shipped a 6/6-green suite with an unverifiable RED claim, a self-approved silent spec interpretation, and a mutation-confirmed vacuous assertion — deleting the never-below-0 guard kept it green) and verify-confirmed (with the skill: RED reported with reason, both interpretations surfaced for human confirmation, the same vacuous guard caught, proven unreachable via the public API, and hardened with a sweep property test).
- **`PROTOCOL.md`**: invariants **I13** (fresh-context test review) and **I14** (solo re-RED), artifact **A12** (test-review report), a `spec-tdd-lite` column in the scope-per-tier matrix (I4 via I14; I9 as stall-breaker→promote), and a lite paragraph in "what the protocol does NOT guarantee".
- **Front-ends route to lite.** `spec-tdd-escalate` gains the fourth tier row (small, non-critical → lite) and its mistakes/red-flags now say "one of the four"; `grill-spec-tdd`'s routing list gains the same option; `spec-tdd` cross-references lite for work too small to delegate.
- README: six skills, ladder + decision tree + walkthrough + mermaid flow updated for lite; version 1.3.0.

### Changed
- `spec-tdd` SKILL.md's PROTOCOL pointer now cites artifacts A1–A12 and invariants I1–I14.

## [1.2.1] - 2026-08-12

Patch: bounds the `spec-tdd-adversarial` attack loop, which was unbounded (asymmetric with the implementer's capped repair loop).

### Fixed
- **Attack-loop circuit breaker (adversarial).** The attacker loop had no numeric cap — its only stop condition ("attacker cannot construct a wrong-but-green impl") is prove-a-negative and may never hold on a boundary-rich surface, so a diligent attacker could force a non-terminating loop. Added a circuit breaker mirroring the implementer's repair cap: STOP after 3 rounds, or when the same hole appears on any two rounds; if a residual hole remains at the breaker, surface it + the attacker's report to the human rather than loop. Baseline-confirmed (the unbounded loop was reproduced) and verify-confirmed.

## [1.2.0] - 2026-08-12

The **prompt-discipline → protocol-discipline** release. Hardens the family's invariants from prose rules into enforceable procedures, and formalizes the method as a protocol. Each behavioral change was baseline-confirmed (RED — watched an agent fail under the old rule) and verify-confirmed (GREEN — watched it comply under the new one) via subagent pressure tests.

### Added
- **`PROTOCOL.md`** — the canonical spec of the method: artifacts (A1–A11) and invariants (I1–I12), with a drift-control statement (skills own *how* to enforce; PROTOCOL owns *what* the invariant is), a scope-per-tier matrix, and a "what the protocol does NOT guarantee" section. `spec-tdd` links to it.
- **SPEC-INTEGRITY (invariant I4).** The acceptance test is now hashed before delegation and verified byte-for-byte on return; any change = FAIL, even on a GREEN re-run. Closes the hole where a *silent* implementer edit slipped through — re-run proved GREEN, not UNCHANGED.
- **Three-bucket failure routing (invariant I10).** Replaces the binary spec-flawed/impl-flawed with **SPEC** (re-open the requirement) / **TEST** (requirement right, executable spec weak or incomplete — strengthen it, do NOT re-open the requirement) / **IMPL** (re-delegate). Baseline showed the binary mis-routed a "requirement-right-but-test-incomplete" case to "re-ask the human"; now routes to TEST.
- **Same-root-cause early stop (invariant I9).** The circuit breaker also fires when the same root cause (same failing file:line + assertion) appears on any two attempts — no longer burns all 3 attempts re-trying one identical misdiagnosis.
- **Grill materiality stop (invariant I11).** `grill-spec-tdd` now stops when remaining questions can't materially change behavior / state / failure-semantics / data / security / compatibility / NFRs — bounds the grill by materiality, not exhaustion.
- README link to `PROTOCOL.md` and a technical subtitle.

### Changed
- **Softened the core claim (README + `spec-tdd`).** "Structural guarantee" is now explicitly scoped as a guarantee *against the green lie* (the test cannot have been reverse-engineered to mirror the impl) — NOT a guarantee the spec is *right*. A misread requirement still makes a bad test; that is a different failure mode handled by RED-first, the adversarial read, the grill, and the attacker.
- **README foregrounded "Human validates WHAT, agent validates HOW"** as a core principle.
- **Base `spec-tdd` Phase 3**: after the orchestrator strengthens the acceptance test, it must re-confirm RED against the impl and re-delegate to restore GREEN (previously implicit — the adversarial tier did this, the base tier didn't spell it out).
- README circuit-breaker wording → "3 attempts OR same root cause twice"; README failure-routing wording → the three buckets.

### Fixed
- **Drift: README's failure routing** (the mermaid diagram + two body sections) no longer carries the superseded two-bucket `spec-flawed` / `impl-flawed` labels; it now matches the skills' SPEC/TEST/IMPL taxonomy.
- **The "re-run to confirm the test is unchanged" non-sequitur** — re-running proved GREEN, not UNCHANGED; replaced by the SPEC-INTEGRITY hash check.

## [1.1.0] - 2026-08-12

Adds `spec-tdd-escalate` — a second front-end for the case `grill-spec-tdd` was overkill: the requirement is already settled and you just want the right tier picked for you.

### Added
- **`spec-tdd-escalate`** — the no-grill front-end. Reads a settled requirement, picks the verification tier by stakes (correctness-critical → `spec-tdd-adversarial`; needs branch-coverage evidence → `spec-tdd-coverage`; else → `spec-tdd`), and invokes it by name. **Route-only:** it does not grill, write the acceptance test, delegate, or gate — the invoked tier runs its own Phase 1. Full-auto (no gate): escalate exists for "you decide for me"; if you wanted to decide, you'd invoke a tier directly. Authored with the TDD-for-docs process (baseline the failure modes → write the skill → close the "brief-the-tier" loophole).
- README updated: the family is now five skills; "When to use which" and the rule of thumb cover `spec-tdd-escalate`.

### Changed
- **`grill-spec-tdd` — cross-links `spec-tdd-escalate`.** "When to Use" now points to `spec-tdd-escalate` as the skip-grill alternative for an already-settled requirement (keeping `spec-tdd` direct for low-stakes). Discovery-only edit; no behavior change.
- **Renamed `grill-spec` → `grill-spec-tdd`.** Brings the grilling front-end into the family naming (directory + `name:` field + every cross-reference, synced in this repo and the installed `~/.claude/skills` copy). **Breaking:** invoke as `/grill-spec-tdd` now (was `/grill-spec`).

## [1.0.0] - 2026-08-07

First versioned release. This release hardens `grill-spec-tdd`'s routing into the verification tiers — fixing two failure modes seen in a trial run (the agent went hunting for `SKILL.md` files; the agent re-asked about delegating after the gate) and closing the seam where both `grill-spec-tdd` and the tiers claimed "write the acceptance test."

### Changed
- **`grill-spec-tdd` — routing is now explicit and tool-driven.** Phase 2 now directs the orchestrator to **INVOKE the chosen tier** (`spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`) **by name via the Skill tool**, replacing the ambiguous "route to." It explicitly forbids searching the filesystem for `SKILL.md` files or wondering "how are these skills organized?" (with a fallback read path for the rare case a name won't load).
- **`grill-spec-tdd` — the approval gate bundles the routing decision.** Phase 1, step 6 now says to present the test + grilled decisions + tier choice as a single go-ahead, so approval = proceed straight to route + delegate, with no second "should I hand this to a subagent?" ask.
- **`grill-spec-tdd` — closes the double-Phase-1 seam.** Phase 2 notes the grilled acceptance test is already written and RED, so the orchestrator skips the tier's Phase 1 and goes straight to Phase 2 (delegate).
- Two new rows in `grill-spec-tdd`'s **Common Mistakes** capture the two observed failure modes (re-asking after RED; hunting the filesystem for skill files).

### Added
- **Tier entry notes.** Each tier's Phase 1 gained a one-liner: if arrived from `grill-spec-tdd`, the acceptance test is already RED — skip to Phase 2. `spec-tdd-adversarial` additionally reminds the orchestrator to ensure the mandatory property/differential tests exist.
- This `CHANGELOG.md`.
- A version line at the top of `README.md`.

### Fixed
- Agents routing from `grill-spec-tdd` into a tier no longer fumble on skill discovery, and no longer re-ask about delegation after the gate has passed.
