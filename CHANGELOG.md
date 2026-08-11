# Changelog

All notable changes to the `spec-tdd` skill family are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
