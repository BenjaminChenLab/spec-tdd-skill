# Spec-TDD Protocol

**Version 1.2.0**

> *A protocol for preventing correlated test/implementation failure in AI-generated software.*

The formal specification of the spec-TDD method: the **artifacts** it produces and the **invariants** those artifacts uphold. The [SKILL.md](skills/spec-tdd/SKILL.md) files are the *operational enforcement* — the exact steps an orchestrator runs; this file is the *canonical catalog* of what those steps protect.

> **Drift control — on disagreement:** when a skill and this file describe the same invariant, the **skill is authoritative for *how* to enforce it** (the executable steps), and **this file is authoritative for *what* the invariant is** (the definition). Change one, update the other.

## Artifacts

| ID | Artifact | Produced by | When |
|---|---|---|---|
| A1 | **Requirement** — the raw ask | human / grill | before Phase 1 |
| A2 | **Acceptance spec** — the behavioral, black-box acceptance test | orchestrator | Phase 1 (before impl exists) |
| A3 | **RED evidence** — the spec fails before any impl | orchestrator | Phase 1 |
| A4 | **SPEC-INTEGRITY snapshot** — hash of A2 at handoff | orchestrator | Phase 2, before dispatch |
| A5 | **Case-list** — every branch/boundary/exception the impl will cover (coverage+ only) | implementer | Phase 2, before any impl |
| A6 | **Implementation** | implementer | Phase 2 |
| A7 | **Unit tests** — one per case, red→green | implementer | Phase 2 |
| A8 | **Coverage evidence** — per-class branch % + every uncovered line justified (coverage+ only) | implementer, re-run by orchestrator | Phase 2–3 |
| A9 | **Verification evidence** — orchestrator's own re-run (GREEN) **and** re-hash of A2 == A4 | orchestrator | Phase 3 |
| A10 | **Adversarial report** — attempted wrong-but-green impls + per-branch hunt (adversarial only) | independent attacker | Phase 3 |
| A11 | **Final result** — A2 + evidence surfaced to the human (the test, not the impl) | orchestrator | end |

## Invariants

**I1 — Spec precedes implementation.** The acceptance spec (A2) is authored before any implementation exists. (Phase 1.)

**I2 — The spec is behavioral.** Black-box, input→output/state; tests WHAT, not HOW. Never couples to internal method shapes.

**I3 — RED before implementation.** The spec must fail before the impl exists (A3). Green-before-impl = a vacuous / over-mocked test; rewrite it.

**I4 — SPEC-INTEGRITY (immutability).** The acceptance spec is immutable during implementation. The orchestrator snapshots its hash before delegation (A4) and verifies byte-for-byte on return (A9). Any change = **FAIL**, even if a re-run is GREEN — a weakened-but-green spec is the green lie. *(Binds the implementer; the orchestrator's own strengthening is a separate, explicitly re-RED'd step.)*

**I5 — Independent verification.** The orchestrator re-runs the spec itself; never trusts the implementer's self-report.

**I6 — Case-list precedes implementation (coverage+).** The implementer declares its case-list (A5) *before* writing impl, and the orchestrator gap-checks it against the real branches — a cross-context check that stops a case-list quietly mirroring the impl.

**I7 — Coverage is evidence, not a percentage.** Branch % (not line %) per new/changed class, with every uncovered line justified. The **case-list is the gate**, not the % — a % gate incentivizes low-value tests.

**I8 — Independence for critical paths (adversarial).** A correctness-critical path gets a *third* context — an independent attacker that tries to write a wrong-but-green impl and hunts uncovered branches. Independence is the one thing a diligent same-context agent cannot give itself.

**I9 — Circuit breaker.** STOP when *either* fires: 3 repair attempts, OR **the same root cause on any two attempts** (not necessarily consecutive). "Same root cause" = same failing file:line AND same failing assertion — judge by those, not by a rephrasable free-text trace or a coarse ERR tag. Each attempt must rest on a genuinely different root cause; never burn attempts re-trying one identical misdiagnosis.

**I10 — Three-bucket failure routing.** On failure — or a hole found in a GREEN test — route by root cause, three buckets only:
- **SPEC** — requirement misread / under-interrogated; the test encodes wrong behavior → **re-open the requirement**, rewrite the test, re-confirm RED, re-delegate.
- **TEST** — requirement right, executable spec weak / incomplete (or the implementer edited it) → **strengthen / revert the test**, re-confirm RED, re-delegate. Do NOT re-open the requirement.
- **IMPL** — spec right, code wrong → **re-delegate** with the failing case + ERR tag.

**I11 — The grill is bounded by materiality.** STOP grilling when remaining questions cannot change observable behavior, state transitions, failure semantics, data integrity, security/authorization, compatibility, or explicit NFRs. Materiality bounds the grill — not asking until exhausted.

**I12 — Human validates WHAT, agent validates HOW.** A wrong *spec* is the human's call, caught by reviewing the test (the cheap, high-signal checkpoint); a wrong *implementation* is the agent's call, caught by running it. Review the test, not the code.

## Scope per tier

| Invariant | spec-tdd | +coverage | +adversarial |
|---|:---:|:---:|:---:|
| I1–I5, I9, I10, I12 | ✅ | ✅ | ✅ |
| I6, I7 (case-list + coverage evidence) | — | ✅ | ✅ |
| I8 (independent attacker) | — | — | ✅ |
| I11 (materiality grill) | via `grill-spec-tdd` front-end | via `grill-spec-tdd` | via `grill-spec-tdd` |

## What the protocol does NOT guarantee

The agent boundary (I1–I4) is a structural guarantee **against the green lie** — the spec cannot have been reverse-engineered to mirror the impl. It does **not** guarantee the spec is *right*: a misread or under-interrogated requirement still produces a bad test. That failure mode is handled by the *other* invariants — RED-first (I3), the adversarial read, the grill (I11), and the independent attacker (I8) — not by the boundary alone.
