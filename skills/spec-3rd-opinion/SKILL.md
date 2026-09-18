---
name: spec-3rd-opinion
description: Use when the user says "spec-3rd-opinion", or a settled plan needs maximum pre-commit scrutiny — same flow as spec-2nd-opinion plus a SECOND concurrent auditor on an adversarial brief (assume the plan flawed, hunt what the standard lens misses). The final plan is presented only when ALL THREE agree: orchestrator + standard auditor + adversarial auditor.
---

# spec-3rd-opinion

**REQUIRED BACKGROUND:** You MUST know `spec-2nd-opinion` first — this skill is that entire flow (preconditions, the I21 pre-flight, brief discipline, dispatch rules incl. the no-dispatch stop and the dead-dispatch re-dispatch, merge gate, final-plan format incl. the doc write-back, Common Mistakes, Red Flags all apply unchanged) **plus one more auditor and a harder gate**. Only the deltas are written here.

## Overview

Two independent eyes are better than one — unless both share a lens. `spec-3rd-opinion` dispatches **two auditors concurrently with deliberately different briefs**: a **standard verifier** (verify the claims, check drift, judge the ordering — `spec-2nd-opinion`'s audit) and an **adversarial hunter** (assume the plan is flawed until proven otherwise; its value is finding what everyone else missed). The plan ships only when **all three positions agree** — yours, the verifier's, the hunter's.

**Core principle: lens diversity, concurrent dispatch.** The two auditors never see each other, never run sequentially (a second brief written after reading the first report inherits its blind spots through you), and never share a template. What stays correlated is what gets asked in the first place — the adversarial brief exists to widen exactly that.

## The flow — deltas from spec-2nd-opinion

### Step 1 — Distill TWO briefs, not one
- **Brief A (standard verifier)**: exactly `spec-2nd-opinion`'s Step-1 brief.
- **Brief B (adversarial hunter)**: same background and same plan-under-audit (identical raw material — different questions). Its checklist is reframed adversarially:
  - "Assume the plan is flawed until proven otherwise."
  - Hunt hidden risks, blueprint-vs-reality drift, unstated assumptions — especially ones the planner has no incentive to check (fields the plan's predicates depend on being reliably populated; watermarks/queues/state another item silently mutates; a skip-flag colliding with a force-requeue).
  - **Argue the strongest case AGAINST the ordering, then state whether it survives.**
  - **Deliver at least one interaction risk nobody listed** — or state honestly, after N genuinely distinct attempts, that none was found (a forced fake finding is worse than none).
  - Same evidence rules: per-item VERDICT + `file:line`; every "OK" names the attack attempted.

### Step 2 — Dispatch BOTH, concurrently, in the same turn
Both read-only, both **TOP tier** (I19(a)), both background. Dispatch them together — a hunter briefed after the verifier's report lands is just an echo with angrier adjectives. Announce both lenses to the user; **report nothing until BOTH notifications have arrived** (a partial merge is a biased merge — you'll rationalize the missing opinion toward the one you've read). One notification lands, the other's dispatch dead or stalled → re-dispatch the dead **lens** fresh, never both (the arrived verdict is real output), disclosed; spec-2nd-opinion's coarse bound applies.

### Step 3 — Merge three positions (the gate hardens)
- **All three agree** (and no critical claim refuted by either auditor) → final plan.
- **Any disagreement** → lay out a **point × opinion matrix** (claim, your position, verifier's, hunter's, each with evidence). Then:
  - Points where the auditors **split** are the valuable ones — arbitrate with evidence and stated reasons, or escalate to the user when it's genuinely their call (I12).
  - Amend the plan → **ONE targeted re-audit round** on the amended points only, **fresh context** for both lenses (the bound is I16's audit-plus-one; the fresh auditors are spec-2nd-opinion's stated deviation — never loop, never let a re-audit turn into negotiation).
- Disagreement is not failure — it's the product. A hunter that finds nothing and a verifier that confirms everything is a valid outcome, but it must be earned: the final plan discloses what each lens attacked.

### Step 4 — The final plan (same format as spec-2nd-opinion, plus)
Attribute amendments to their source lens ("per the standard audit: …", "per the adversarial audit: …"); state each lens's final position in one line. Three-way agreement recorded → present, write back to the persisted doc (attribution per lens, spec-2nd-opinion's Step 4), and stop.

## Common Mistakes — beyond spec-2nd-opinion's
| Mistake | Fix |
|---|---|
| Two auditors, same brief | Different lenses is the whole point — a duplicated brief buys a second opinion that thinks it's independent. |
| Dispatching the hunter after reading the verifier's report | Dispatch both in the same turn, before either result exists in your context. |
| Merging on the first notification while the second still runs | Wait for both. A partial merge bends toward whichever report you've read. |
| Counting two "partially agree" as agreement | The gate is three explicit endorsements. Partial = resolve or disclose as a residual. |
| Rewarding the hunter for volume (finding something, anything) | A forced fake finding wastes a re-audit round; "searched honestly, found none" is a legitimate verdict — the brief says so explicitly. |
| Letting the adversarial mandate leak into re-litigating user decisions | Adversarial applies to facts/risks/ordering — the WHAT stays the human's (I12). |

## Red Flags — STOP (beyond spec-2nd-opinion's)
- About to merge verdicts with only one auditor's notification on record.
- About to soften the gate because "two of three basically agree" — the gate is all three, or the disagreement is disclosed and arbitrated.
- The hunter's report agrees with everything and names no attempted attack — that's a rubber stamp wearing a scary brief; demand the evidence or re-dispatch.
- About to write Brief B by editing Brief A's text lightly — rewrite the questions, not the adjectives.
