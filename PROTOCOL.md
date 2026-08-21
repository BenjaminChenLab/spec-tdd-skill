# Spec-TDD Protocol

**Version 1.4.1**

> *A protocol for preventing correlated test/implementation failure in AI-generated software.*

The formal specification of the spec-TDD method: the **artifacts** it produces and the **invariants** those artifacts uphold. The [SKILL.md](skills/spec-tdd/SKILL.md) files are the *operational enforcement* — the exact steps an orchestrator runs; this file is the *canonical catalog* of what those steps protect.

> **Drift control — on disagreement:** when a skill and this file describe the same invariant, the **skill is authoritative for *how* to enforce it** (the executable steps), and **this file is authoritative for *what* the invariant is** (the definition). Change one, update the other.

## Artifacts

| ID | Artifact | Produced by | When |
|---|---|---|---|
| A1 | **Requirement** — the raw ask | human / grill | before Phase 1 |
| A2 | **Acceptance spec** — the behavioral, black-box acceptance test (per unit in multi-unit runs) | orchestrator | Phase 1 (before impl exists) |
| A3 | **RED evidence** — the spec fails before any impl (per unit in multi-unit runs) | orchestrator | Phase 1 |
| A4 | **SPEC-INTEGRITY snapshot** — hash of A2 at handoff (per unit spec in multi-unit runs) | orchestrator | Phase 2, before dispatch |
| A5 | **Case-list** — every branch/boundary/exception the impl will cover (coverage+ only) | implementer | Phase 2, before any impl |
| A6 | **Implementation** | implementer | Phase 2 |
| A7 | **Unit tests** — one per case, red→green | implementer | Phase 2 |
| A8 | **Coverage evidence** — per-class branch % + every uncovered line justified (coverage+ only) | implementer, re-run by orchestrator | Phase 2–3 |
| A9 | **Verification evidence** — orchestrator's own re-run (GREEN) **and** re-hash of A2 == A4 (per unit in multi-unit runs) | orchestrator | Phase 3 |
| A10 | **Adversarial report** — attempted wrong-but-green impls + per-branch hunt (adversarial only) | independent attacker | Phase 3 |
| A11 | **Final result** — A2 + evidence surfaced to the human (the test, not the impl) | orchestrator | end |
| A12 | **Test-review report** — fresh-context reviewer findings: missing case / vacuous assertion / silent interpretation / none (lite only) | independent reviewer subagent | Phase 3 (lite) |
| A13 | **Unit plan** — the units, their order/grouping, and which specs are writable now vs just-in-time (multi-unit runs) | orchestrator | before the first dispatch; gated once |

## Invariants

**I1 — Spec precedes implementation.** The acceptance spec (A2) is authored before any implementation exists. (Phase 1.)

**I2 — The spec is behavioral.** Black-box, input→output/state; tests WHAT, not HOW. Never couples to internal method shapes.

**I3 — RED before implementation.** The spec must fail before the impl exists (A3). Green-before-impl = a vacuous / over-mocked test; rewrite it. RED evidence must be **pure**: the orchestrator scans the FULL error list — every error must point at symbols the feature will create; errors about EXISTING symbols (wrong constructor arity, ambiguous overloads, unused imports) are a defect in the test itself, fixed before dispatch.

**I4 — SPEC-INTEGRITY (immutability).** The acceptance spec is immutable during implementation. The orchestrator snapshots its hash before delegation (A4) and verifies byte-for-byte on return (A9). Any change = **FAIL**, even if a re-run is GREEN — a weakened-but-green spec is the green lie. *(Binds the implementer; the orchestrator's own strengthening or SPEC-DEFECT correction is a separate, explicitly re-RED'd step.)*

**I5 — Independent verification.** The orchestrator re-runs the spec itself; never trusts the implementer's self-report.

**I6 — Case-list precedes implementation (coverage+).** The implementer declares its case-list (A5) *before* writing impl, and the orchestrator gap-checks it against the real branches — a cross-context check that stops a case-list quietly mirroring the impl.

**I7 — Coverage is evidence, not a percentage.** Branch % (not line %) per new/changed class, with every uncovered line justified. The **case-list is the gate**, not the % — a % gate incentivizes low-value tests.

**I8 — Independence for critical paths (adversarial).** A correctness-critical path gets a *third* context — an independent attacker that tries to write a wrong-but-green impl and hunts uncovered branches. Independence is the one thing a diligent same-context agent cannot give itself. The attack loop is **bounded by an attack-loop circuit breaker** (mirrors I9): STOP after 3 rounds, or when the same missing case re-fails on any two rounds (judge by the acceptance-test case, not the attacker's rephrased description); if a residual hole remains at the breaker, surface it to the human rather than loop — a rich surface always has one more boundary.

**I9 — Circuit breaker.** STOP when *either* fires: 3 repair attempts, OR **the same root cause on any two attempts** (not necessarily consecutive). "Same root cause" = same failing file:line AND same failing assertion — judge by those, not by a rephrasable free-text trace or a coarse ERR tag. Each attempt must rest on a genuinely different root cause; never burn attempts re-trying one identical misdiagnosis.

**I10 — Three-bucket failure routing.** On failure — or a hole found in a GREEN test — route by root cause, three buckets only:
- **SPEC** — requirement misread / under-interrogated; the test encodes wrong behavior → **re-open the requirement**, rewrite the test, re-confirm RED, re-delegate.
- **TEST** — requirement right, executable spec weak / incomplete, or defective (a SPEC-DEFECT, per I15), or the implementer edited it → **strengthen / revert / correct the test**, re-confirm RED, re-delegate. Do NOT re-open the requirement.
- **IMPL** — spec right, code wrong → **re-delegate** with the failing case + ERR tag.
SPEC vs TEST: a defect fixable by consulting artifacts already held (the requirement/plan) is TEST; a test fix that requires deciding something the requirement doesn't decide is SPEC — the human's call (I12).

**I11 — The grill is bounded by materiality.** STOP grilling when remaining questions cannot change observable behavior, state transitions, failure semantics, data integrity, security/authorization, compatibility, or explicit NFRs. Materiality bounds the grill — not asking until exhausted.

**I12 — Human validates WHAT, agent validates HOW.** A wrong *spec* is the human's call, caught by reviewing the test (the cheap, high-signal checkpoint); a wrong *implementation* is the agent's call, caught by running it. Review the test, not the code.

**I13 — Fresh-context test review (lite).** After GREEN, exactly one dispatch to a reviewer that has seen none of the implementation reasoning. Two questions, answered with concrete cases: test-vs-impl (name a subtly-wrong impl that still passes every test) and test-vs-requirement (every requirement line has an assertion with discriminating power; the author's silent interpretations are surfaced to the human). Where no dispatch is possible, a *disclosed* degraded mode applies (mutation checks + requirement-line audit) — never a silent improvised review.

**I14 — Solo re-RED (lite).** Any acceptance-spec edit made after the impl exists must be re-confirmed RED before it counts; a strengthening that cannot go RED has no teeth and must be rewritten. The discipline replacement for I4's hash where author and implementer share a context.

**I15 — Test-defect is a distinct failure mode (SPEC-DEFECT).** The acceptance test itself can be defective (wrong constructor arity, ambiguous overload matchers, unused stubs under strict stubs, assertions contradicting the spec). The implementer's instruction is asymmetric: report SPEC-DEFECT with evidence — the correct outcome, not a failure to implement — while production changes that exist solely to accommodate a test defect count as a FAILED run; when the test is defective, the implementer's only lever is production, and it will bend it instead of reporting. The orchestrator's Phase-3 **SPEC-DEFECT sweep** diffs returned production changes against the spec: any change whose only beneficiary is the acceptance test is an accommodation → correct the orchestrator's own artifact (re-hash, note the correction — the I4 escape hatch) and restore production to the spec'd shape. RED purity (I3) is the same failure mode caught at Phase 1.

## Scope per tier

| Invariant | lite | spec-tdd | +coverage | +adversarial |
|---|:---:|:---:|:---:|:---:|
| I1–I3, I5, I10, I12 | ✅ | ✅ | ✅ | ✅ |
| I4 (SPEC-INTEGRITY hash) | via **I14** (solo re-RED) | ✅ | ✅ | ✅ |
| I15 (SPEC-DEFECT: report-not-bend + Phase-3 sweep) | ✅ via Phase-2 test-defect exception + exit-rule sweep (solo re-RED replaces re-hash) | ✅ | ✅ | ✅ |
| I6, I7 (case-list + coverage evidence) | — | — | ✅ | ✅ |
| I8 (independent attacker) | — | — | — | ✅ |
| I9 (circuit breaker) | stall breaker → promote to `spec-tdd` | ✅ | ✅ | ✅ |
| I13 (fresh-context test review) | ✅ | — | — | — |
| I11 (materiality grill) | via `grill-spec-tdd` front-end | via `grill-spec-tdd` | via `grill-spec-tdd` | via `grill-spec-tdd` |

`spec-tdd-lite` implements in-session — no implementer dispatch; its only boundary crossing is the I13 review.

In a **multi-unit run** (`spec-tdd`), I1–I5, I9, I10 and I15 apply **per unit** (I9 per unit/group), and I12's checkpoint is ONE gate on the unit plan (A13) + the specs writable now — not N gates. With no dispatch tool available, per-unit boundaries still hold via a disclosed degraded path.

## What the protocol does NOT guarantee

The agent boundary (I1–I4) is a structural guarantee **against the green lie** — the spec cannot have been reverse-engineered to mirror the impl. It does **not** guarantee the spec is *right*: a misread or under-interrogated requirement still produces a bad test. That failure mode is handled by the *other* invariants — RED-first (I3), the adversarial read, the grill (I11), and the independent attacker (I8) — not by the boundary alone.

`spec-tdd-lite` additionally trades away the fresh implementer and I4's structural hash (replaced by I14's discipline): a misread requirement can reach GREEN unchallenged except by the I13 review's test-vs-requirement question — which is why lite is scoped to one small, non-critical unit.
