---
name: adversarial-grill-spec-tdd
description: Use when a FUZZY requirement sits on a CRITICAL surface (money movement / auth-permissions / data-loss) and a wrong grill decision or defective acceptance test would burn a full top-tier run — grill-spec-tdd upgraded with an independent grill-auditor dispatched TWICE: Part A attacks the grill's decisions BEFORE the spec gate, Part B attacks the final-spec acceptance test AFTER the gate (pre-dispatch); more tokens, bought safety. NOT the spec-tdd-adversarial verification tier (settled-critical implementation, attacker at Phase 3) — this attacks the grill and the test BEFORE any implementation exists. Triggers on fuzzy+critical, grill-decision attack, wrong-direction cost, pre-dispatch test audit.
---

# adversarial-grill-spec-tdd

**REQUIRED BACKGROUND:** Understand `grill-spec-tdd` first. This is grill-spec-tdd with a mandatory independent **grill-auditor** dispatched TWICE — **Part A** attacks the grill's decisions before the spec gate, **Part B** attacks the final-spec acceptance test after the gate, before routing. It inherits the materiality grill, grounding, the gate-before-test ordering (no acceptance-test tokens before the gate; the test is derived from the FINAL decision spec), must-be-RED + RED-purity, the gate, and tier routing.

## Overview

grill-spec-tdd, plus: an **independent adversarial subagent attacks the grill itself** — Part A (pre-gate): the decisions, the dimension coverage, the materiality stops; Part B (post-gate, pre-dispatch): the acceptance test derived from the gate-approved final spec. Fuzzy + critical only (money movement / auth-permissions / data-loss — verbatim `spec-tdd-adversarial`'s predicate). Lower stakes → plain `grill-spec-tdd`; the audit's tokens buy nothing there.

**Core principle: re-reading is not the fix — only independence is.** Observed baseline: an adversarial audit caught a categorical clause defect present in FIVE files that the author had just re-read line-by-line, twice. A diligent same-context author cannot see its own blind spots — so "re-read my decisions" is not a compliance move here. The family already knows this (I8) but applies independence only AFTER impl exists (the adversarial tier's attacker runs post-dispatch, at Phase 3). This front-end moves an attacker to the cheapest moments: **before the gate (the decisions) and before the implementer dispatch (the test)** — zero implementation tokens spent either way.

**Honest coverage claim:** Part A (decision/dimension coverage) is NEW — no other artifact in the family attacks the grill's decisions. Part B (test strength, SPEC-DEFECT classes) is the coverage the adversarial tier's Phase 3 also provides — its value here is timing/cost only: caught before the implementer dispatch and the tier run burn. It runs POST-gate by design, not omission: the test is authored from the gate-approved final spec (grill-spec-tdd's gate-before-test ordering), so that is the earliest moment it exists to attack.

## When to Use
- Requirement is FUZZY **AND** the surface is critical: money movement / auth-permissions / data-loss.
- The user says `adversarial-grill-spec-tdd`.
- A wrong grill decision or defective final-spec test would cost a full top-tier run or a wrong critical behavior.

**When NOT to use:**
- Requirement SETTLED (any stakes) → `spec-tdd-escalate` (auto-route) or the tier directly.
- Fuzzy but NOT critical → plain `grill-spec-tdd` — don't tax it with this machinery.
- You are past the gate, implementing → that's a verification TIER (`spec-tdd-adversarial` for critical), not this front-end.

> **Not to be confused:** `spec-tdd-adversarial` = the verification TIER (attacker at Phase 3, after impl exists). THIS = the front-end (auditor before the gate on decisions, and pre-dispatch on the test — no impl exists). Fuzzy+critical → run THIS first; it routes into that tier.

## The 4 Phases

### Phase 1 — Grill the requirement (as grill-spec-tdd Phase 1, steps 1–2; NO test yet)
As grill-spec-tdd: materiality-bounded grill (every dimension incl. NFR + security; STOP GRILLING by materiality), ground it in the real architecture. Write down every interpretation of ambiguous wording. **Do NOT write the acceptance test yet** — gate-before-test ordering holds here too: the test is derived from the FINAL spec, after the gate.

### Phase 2 — Dispatch the grill-auditor, Part A: attack the decisions (pre-gate)
```
ATTACK a grill you did not conduct. You are independent: hunt what the author cannot see.

REQUIREMENT (verbatim, do not paraphrase): {paste}
GRILLED DECISIONS + the STOP-GRILLING calls (what was deemed immaterial): {list}
READ FIRST (grounding — quote it or it didn't happen): {codebase paths}

PART A — grill-coverage attack:
- Hunt UN-GRILLED dimensions that would materially change behavior, state, failure
  semantics, data integrity, security, compatibility, or NFRs (materiality, not exhaustion).
- Attack EVERY decision, including the materiality stops themselves — "if this stop is
  wrong, what breaks?" The cheapest place for a catastrophic miss is a dimension declared
  immaterial.
- Surface silent interpretations the author made that a human should confirm.

RETURN: findings, each severity-tagged (BLOCKER / MAJOR / MINOR / OK), each QUOTING the
actual text it rests on. An "OK" must describe the attack you ATTEMPTED and why it failed —
an opinion with no attempted counterexample is a rubber-stamp.
End with a verdict: proceed / proceed-with-changes / redo. Do NOT edit any file.
```

**Reconcile (before the gate):**
- Adopt every BLOCKER/MAJOR: re-grill that dimension. Pre-gate, your decisions re-open freely — the grill is self-directed; self-directed means you decide, not that you decide *unexamined*. A fix that requires deciding something the **requirement** doesn't decide → surface it at the gate; don't decide it silently.
- The auditor REFUTES a grill conclusion → downgrade it honestly and proceed.
- Substantial revision → ONE re-audit. **Bound: audit + at most one re-audit** — if findings are unchanged or all adopted, stop auditing and carry the residuals to the gate.
- **No dispatch tool available?** Disclose at the gate that independence was NOT obtained — a self-audit is worthless by this skill's own thesis — and surface the grill decisions for the deeper human read. Never a silent improvised self-audit.

### Phase 3 — Gate the SPEC (as grill-spec-tdd Phase 1, step 3)
ONE human OK bundling: the grilled decisions + Part A findings + residuals + the routing choice + the spec-doc ask (default ON — persist the final spec; only an explicit decline skips). Amendments fold in → **FINAL SPEC**. No human reachable? Grill-spec-tdd's rule: document + persist the decisions and Part A findings, then **STOP at the gate** — no test, no dispatch, until a human approves. Grill's throwaway gate-skip does NOT carry over — this front-end exists because the surface is critical; there is no gate-skip here.

### Phase 4 — Write the test FROM the final spec, audit it, route
1. **Derive the acceptance test from the FINAL spec** (as grill-spec-tdd Phase 2): behavioral black-box, property/invariant tests for domain logic, every gate amendment included; a decision neither grill nor gate made goes back to the human, never silently into the test. **Run it — MUST be RED with the full-list RED-purity check** (incl. the breaking-change exception).
2. **Dispatch the grill-auditor, Part B: attack the test** (independent context, read-only; still zero implementation tokens):
```
ATTACK an acceptance test you did not write. You are independent: hunt what the author cannot see.

REQUIREMENT (verbatim, do not paraphrase): {paste}
FINAL SPEC (gate-approved decisions, amendments included): {list}
ACCEPTANCE TEST (+ property tests) and its recorded RED error list: {file or paste}
READ FIRST (grounding — quote it or it didn't happen): {codebase paths}

PART B — test attack (no impl exists):
- Name a wrong-but-plausible reading of the FINAL SPEC this test would still satisfy —
  or behavior the test asserts BEYOND it.
- Assertions with no discriminating power; property tests that are tautologies.
- SPEC-DEFECT classes against the REAL codebase: constructor arity vs actual constructors,
  ambiguous overloads vs real signatures, unnecessary stubs, assertions contradicting
  the final spec.
- RED purity of the recorded error list (errors about EXISTING symbols the spec doesn't change).

RETURN: findings, each severity-tagged (BLOCKER / MAJOR / MINOR / OK), each QUOTING the
actual file/test text it rests on. An "OK" must describe the attack you ATTEMPTED and why
it failed — an opinion with no attempted counterexample is a rubber-stamp.
End with a verdict: proceed / proceed-with-changes / redo. Do NOT edit any file.
```
3. **Reconcile:** adopt every BLOCKER/MAJOR → fix the TEST, and re-confirm RED (full-list purity) after EVERY edit. A finding that requires deciding something the requirement/gate didn't decide is a **SPEC-level residual** → surface it to the human (the gate approved an ambiguous spec — a follow-up ask, never a silent decision); test-level residuals ride the tier handoff. Substantial revision → ONE re-audit (same bound: audit + one re-audit), then stop and carry residuals.
   - **No dispatch tool available?** Disclose in the handoff that the test audit was not independent — the tier's own Phase 3 (the attacker) is the backstop. Never a silent self-audit.
4. **Route** (as grill-spec-tdd Phase 3): invoke the tier BY NAME (fuzzy+critical typically → `spec-tdd-adversarial`; never `spec-tdd-lite` on a critical surface). The tier treats you as a grill arrival — it skips its Phase 1 (expect the adversarial tier's property-test check) and does not re-litigate locked decisions. Hand off: the test + the final spec + Part B residuals.

**Scope note (multi-unit):** Part A covered the grilled decisions (pre-gate — there is no unit plan yet: the tier writes A13 after routing, and it is HOW, surfaced not gated). Part B covers the specs the front-end wrote post-gate (writable NOW); later just-in-time specs are covered by the tier's own Phase 3 (the adversarial attacker, where the unit routes there) — not by I16. In the degenerate case no spec was written, Part B has no subject — say so; the tier's Phase 3 is the coverage.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Orchestrator audits its own grill or its own test | Independence is the entire point; a same-context re-read is the documented baseline FAILURE (the author missed it twice, line-by-line). Dispatch a fresh context — twice: Part A and Part B. |
| Writes the acceptance test before the spec gate | Inherited from grill-spec-tdd: gate-before-test. Part B exists precisely to attack the FINAL-spec test, which only exists after the gate. |
| Auditor returns all-OK with no attempted counterexamples | An OK must name the attack tried and what excluded it. An opinion is a rubber-stamp. |
| Findings without quotes | Grounding = quoting the actual file/test text. No quote, no finding. |
| Materiality stops left un-attacked | "We decided X doesn't matter" is a decision — Part A attacks the stops themselves. |
| Audit loops while findings evolve | Audit + at most ONE re-audit per part; then residuals move on (Part A → the gate; Part B → the human for spec-level, the handoff for test-level). |
| Used on settled or non-critical work | Settled → `spec-tdd-escalate`; fuzzy+low-stakes → `grill-spec-tdd`. The predicate is fuzzy AND critical — verbatim the adversarial tier's. |
| Test strengthened after Part B but RED not re-confirmed | Every post-audit test edit re-runs RED (full-list purity). |
| No-dispatch mode silently self-audited | Never. Disclose non-independence (Part A at the gate; Part B in the handoff). |
| Part B sold as new coverage | Part B = the adversarial tier's Phase-3 coverage at pre-dispatch cost (timing). Part A is the novel part — don't oversell. |
| Part B finding needs a spec decision, resolved by editing the test | SPEC-level residual → the human decides (follow-up ask). The test encodes decisions; it doesn't make them. |

## Red Flags — STOP
- About to gate with no Part A dispatch on record (or an undisclosed self-audit) on a fuzzy+critical requirement.
- About to write the acceptance test before the spec gate has approved the decisions.
- The auditor's report has no quotes and no attempted counterexamples.
- A materiality stop survived un-attacked.
- The gate is about to route a critical surface to `spec-tdd-lite`.
- Part B findings still being re-litigated past one re-audit, or a spec-level residual decided silently.
