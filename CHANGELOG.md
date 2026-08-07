# Changelog

All notable changes to the `spec-tdd` skill family are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-07

First versioned release. This release hardens `grill-spec`'s routing into the verification tiers — fixing two failure modes seen in a trial run (the agent went hunting for `SKILL.md` files; the agent re-asked about delegating after the gate) and closing the seam where both `grill-spec` and the tiers claimed "write the acceptance test."

### Changed
- **`grill-spec` — routing is now explicit and tool-driven.** Phase 2 now directs the orchestrator to **INVOKE the chosen tier** (`spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`) **by name via the Skill tool**, replacing the ambiguous "route to." It explicitly forbids searching the filesystem for `SKILL.md` files or wondering "how are these skills organized?" (with a fallback read path for the rare case a name won't load).
- **`grill-spec` — the approval gate bundles the routing decision.** Phase 1, step 6 now says to present the test + grilled decisions + tier choice as a single go-ahead, so approval = proceed straight to route + delegate, with no second "should I hand this to a subagent?" ask.
- **`grill-spec` — closes the double-Phase-1 seam.** Phase 2 notes the grilled acceptance test is already written and RED, so the orchestrator skips the tier's Phase 1 and goes straight to Phase 2 (delegate).
- Two new rows in `grill-spec`'s **Common Mistakes** capture the two observed failure modes (re-asking after RED; hunting the filesystem for skill files).

### Added
- **Tier entry notes.** Each tier's Phase 1 gained a one-liner: if arrived from `grill-spec`, the acceptance test is already RED — skip to Phase 2. `spec-tdd-adversarial` additionally reminds the orchestrator to ensure the mandatory property/differential tests exist.
- This `CHANGELOG.md`.
- A version line at the top of `README.md`.

### Fixed
- Agents routing from `grill-spec` into a tier no longer fumble on skill discovery, and no longer re-ask about delegation after the gate has passed.
