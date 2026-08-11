# Changelog

All notable changes to the `spec-tdd` skill family are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
