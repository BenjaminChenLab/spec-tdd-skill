---
name: grill-spec-tdd
description: Use when the user says "grill-spec-tdd", or wants to interrogate/grill requirements before a test-first delegated implementation — especially for fuzzy or high-stakes (money/auth/data) features. Triggers on requirement grilling before coding, spec-as-test, test-first-by-orchestrator, and avoiding wasted subagent runs on wrong-direction specs.
---

# grill-spec-tdd

## Overview
**The requirement-grilling front-end for the `spec-tdd` family.** Interrogate the requirement until it's unambiguous ("grill"), get a human OK on the **decision spec** — the grilled decisions — **BEFORE any test is written**, then derive the acceptance test from the **final** (gate-approved) decision spec, still before any implementation exists — THEN route to the verification tier that fits the stakes and size: `spec-tdd-lite` (one small non-critical unit — in-session), `spec-tdd` (default; multi-unit for batches), `spec-tdd-coverage`, or `spec-tdd-adversarial`. That tier carries the handoff, circuit breaker, and failure routing (lite: in-session loop + review dispatch).

**Why a separate front-end:** under pressure, agents skip grilling and hand a subagent a fuzzy spec, or collapse it to "sensible defaults." Grilling first forces every dimension (incl. NFR + security) explicit and gets a human OK on direction before tokens are burned — on the test-authoring run AND the subagent run.

**Core principle (inherited from `spec-tdd`):** the acceptance test is authored before any impl, in a different context than the implementer — so it cannot have been reverse-engineered to mirror an implementation (it can still be *wrong*; that's a different failure mode). **"Must be RED first"** is the green-lie detector. **Plus (this front-end): the gate owns the spec; the test encodes the final spec.** A test written before the gate anchors to the draft — a gate amendment then lands as a one-line tweak instead of a re-derivation, and the test encodes the draft, not what the human approved. So: no acceptance-test tokens before the gate says yes.

## When to Use
- User says `grill-spec-tdd <feature>`.
- Requirement is fuzzy, high-stakes (money / auth / data-loss), or a wrong-direction subagent run would be expensive.
- For an already-settled requirement (no grilling needed), skip this: low-stakes and you know the tier → `spec-tdd` directly; want the tier auto-picked by stakes → `spec-tdd-escalate`.
- Fuzzy requirement on a CRITICAL surface (money movement / auth-permissions / data-loss) → **`adversarial-grill-spec-tdd`** — the upgraded front-end that dispatches an independent auditor to attack the grill's decisions BEFORE the gate and the final-spec acceptance test after it (pre-dispatch).

## Phase 1 — Grill the requirement, gate the SPEC (no test yet)
1. **Ground it first**: read the relevant entities/services/repos/patterns BEFORE the first question; the decisions must fit the real architecture, and so must the test that follows. Grounding continues through the grill — a fact needed mid-round is looked up (or dispatched) on the spot, not deferred.
2. **Grill in rounds — decisions, not facts** — interrogate EVERY dimension, not just the obvious ones: business logic, boundary/edge cases, state transitions, **NFRs (perf / scale / cost)**, **security / fraud / abuse**, and **deployment/rollout** (migration windows — old code × new schema; environment-gated components; how every runtime object comes to exist in each target environment). Force an explicit decision on each. *If you can't state a decision for a dimension, you haven't grilled it.*
   - **Facts are yours; decisions are the human's.** Never ask the human a question the codebase/docs/config already answers — that is grounding skipped, not grilling. "Don't dig through the code, just ask me — I know the system" is the trap: the human knows their *intent*, not their code's actual shape. Investigate, then decide — or ask a *decision*.
   - **Every question ships its recommended answer.** Number the open decisions and attach your grounded, overridable recommendation to each — the human vetoes instead of composing ("all defaults except 3" is a valid reply). Under time pressure the recommendations are what make ONE short round enough: dropping them "to keep it short" is the failure, not the fix.
   - **Ask only what's answerable now.** Decisions hang off each other. Ask the settled frontier in one round; a question that presupposes an unsettled root is explicitly conditional ("only if Q1 = email: …") or held for the next round — never asked flat. A root overridden later moots every flat dependent the human already answered.
   - **Grilling ≠ silent defaults.** Deciding deliberately after interrogating every dimension is the grill; collapsing to "sensible defaults" without hitting NFR/security is the failure mode. A missed dimension isn't a design decision — it's an absent one (e.g. coupon fraud, lockout-DoS).
   - **The grill is self-directed.** Stakeholders unreachable tonight? You still grill — you interrogate and decide. Their reachability affects the *gate* (step 3), not the grill.
   - **STOP GRILLING when remaining open questions cannot materially change** observable behavior, state transitions, failure semantics, data integrity, security/authorization, compatibility, or explicit NFRs. The grill is bounded by *materiality*, not by asking until exhausted — a question that wouldn't change any of those is bureaucracy, not grilling. Note it and move on; don't let the grill devolve into an endless question loop.
3. **Spec gate — human OK on the decisions, BEFORE any test is written.** Surface the grilled decisions in plain language — the decision spec — bundled with the routing choice (Phase 3 — which follows these blast-radius tags: any IRREVERSIBLE decision → the adversarial tier; all reversible/costly → lighter) and the spec-doc ask (below) as ONE go-ahead. **Tag every decision with its blast radius — reversible / costly / IRREVERSIBLE** (data migration, money-movement semantics, a broken public contract, security posture): an IRREVERSIBLE decision cannot ride a bulk "all defaults" — each needs its own named confirmation or veto, and an unanswered one still parks. The short form survives everywhere else ("all defaults except 3" stays valid for reversible/costly decisions). The gate checks **direction** (is this the right spec?) so you don't burn test-authoring and subagent tokens on the wrong thing — executable tests catch *logic* bugs, not wrong-direction work, so "my tests will encode my assumptions" is **not** a substitute for the gate. Approval with amendments folded in = the **FINAL SPEC** — the single source the acceptance test is derived from.
   - **Persist the spec doc (default ON).** Write the doc — `docs/specs/YYYY-MM-DD-<feature>.md` (follow the project's convention if it has one) — holding the **requirement verbatim + the gate-approved decisions, amendments folded in** (A15 — downstream audits read this doc; a decisions-only doc silently narrows them). So later recall (SPEC-bucket re-opens, PR review, audits) doesn't depend on session memory. Bundle the ask into this gate ("persist to <path>?"); skip ONLY on an explicit decline — an unanswered ask is not a decline, persist.
   - **No human reachable?** Grill fully (it's self-directed), document + persist every decision — then **STOP at the gate**. No test tokens, no dispatch, until a human approves. The gate is **blocking**: "they'll answer eventually" is not an approval, and a slow answer never licenses proceeding on guesses — the parked decision doc is exactly what makes the eventual review a fast one. Never use "no one's reachable" to skip the grill either — the grill is what produces the artifact the gate will review.
   - **Throwaway tier** may skip the gate — the grilled decisions are then the final spec (throwaway stakes don't justify the stop). The spec-doc default (above) still applies: persist unless explicitly declined. An IRREVERSIBLE blast-radius tag voids the throwaway skip — an irreversible decision is not throwaway stakes.

## Phase 2 — Write the acceptance test FROM the FINAL SPEC
1. **Derive BEHAVIORAL acceptance tests from the final spec** — black-box, input→output/state. Test WHAT, not HOW; don't couple to internal method shapes. **Every gate amendment included** — re-derive from the final spec; there is no earlier draft to patch. **Multi-unit route:** write the specs writable NOW (bug batch: every repro test; feature split: the first unit's) — later units' specs are just-in-time at the tier, grounded in the codebase as it exists after earlier units land. Test-writing surfaces a decision neither grill nor gate made? Test-local mechanics (fixtures, naming, arrange details) are yours to decide; anything that changes observable behavior, state transitions, failure semantics, data, security, compatibility, or NFRs goes back to the human — never decided silently into the test.
2. (Domain logic only) add 1–3 **property/invariant tests** (e.g. money conservation). Properties can't become green lies.
3. **Run it — MUST be RED.** Green with no impl = fake test (vacuous / over-mocked); rewrite it. Intermittently green (fails, then green on a re-run) = same verdict — pre-impl the flake is test-side (unpinned seed/clock/dependency, suite interference); pin it.
   - **RED-purity check:** scan the FULL compiler/runner error list, not just the tail. Every error must point at symbols the feature will create. Any error about EXISTING symbols — wrong constructor arity, ambiguous method overloads, unused imports — is a defect in YOUR test, not feature absence. Exception: if the spec itself explicitly calls for changing that existing symbol (a breaking-change feature), the error points at the shape the feature will create — the RED is good. Otherwise fix the test before routing; a defective RED masquerades as "feature missing" and the tier's implementer will bend production to accommodate it. (The tier skips its Phase 1 on arrival from here — this check is the only RED audit the test gets.) Also append the acceptance-test path to the spec doc (A15's reference — the doc is what later recall reads).
4. **Encoding audit — dispatch it, TOP-TIER model (I19).** The human gated the decisions, not this test; no unaudited test crosses the agent boundary (I13). A fresh context checks the encoding before routing:
   ```
   REVIEW an acceptance test you did NOT write.
   FINAL SPEC: {spec doc path — persisted at the gate (A15); READ it. Paste the decision list only when persistence was declined}
   ACCEPTANCE TEST (+ property tests), currently RED: {file or paste}
   READ FIRST: {codebase paths}
   1. Does every decision have an assertion with discriminating power? Name a
      wrong-but-plausible reading of the spec this test still satisfies.
   2. Surface anything asserted BEYOND the spec, and every silent interpretation.
   RETURN: findings (missing decision / vacuous assertion / over-assertion /
   silent interpretation / none), each quoting what it rests on. Do NOT edit any file.
   ```
   Adopt every finding → fix the test → **re-confirm RED**. No dispatch tool? Disclose the same-context review in the handoff — degraded, never silent.

## Phase 3 — Route to the verification tier (INVOKE the skill — don't hunt for files)
The spec gate (Phase 1, step 3) was the ONE human checkpoint. Now route by INVOKING the chosen tier as a skill. **Do NOT search the filesystem for `SKILL.md` files or wonder "how are these skills organized?"** — skills are loaded BY NAME through the Skill tool. (Fallback only if a name truly won't load: read `~/.claude/skills/<name>/SKILL.md`.)

Pick by stakes and size, then call the Skill tool with the exact name:
- **Blast-radius-CRITICAL** — a silent wrong result moves money, changes authorization, or irreversibly corrupts data; equivalently, the gate's decisions carry an IRREVERSIBLE blast-radius tag → invoke **`spec-tdd-adversarial`**. Money-adjacent ≠ money-movement: display / reporting / reference data / internal-tooling units that read the money system but cannot corrupt it → **`spec-tdd-coverage`** (branchy/compliance) or **`spec-tdd`**; a pre-settlement safety net (reconciliation / monitoring / dual-control) bounds the blast radius → one tier down. Multi-unit runs route **per unit**.
- **Need branch-coverage EVIDENCE** (large/subtle branch surface: concurrency/parsing/state machines; weak unit tests; compliance proof) → invoke **`spec-tdd-coverage`**.
- **One small non-critical unit** (a single bugfix-scale item in a session you'll clear after — one dispatch costs more than it saves) → invoke **`spec-tdd-lite`** (the in-session tier; it keeps the grilled acceptance test and skips the implementer dispatch).
- **Multiple units** (a bug list, or a feature split into slices) → invoke **`spec-tdd`** as a **multi-unit run** (its Multi-unit section takes over; specs not yet writable are written just-in-time per unit).
- **Otherwise** → invoke **`spec-tdd`** (the default).

When the tier loads:
- **The grilled acceptance test is already written, RED, and encoding-audited** → SKIP the tier's Phase 1 (orchestrator-writes-test AND its encoding audit); go straight to its Phase 2 (delegated tiers: hand off to the subagent; `spec-tdd-lite`: implement in-session). Don't re-write or re-confirm the test.
- The gate already passed → execute per the tier's handoff (delegated tiers: dispatch; `spec-tdd-lite`: implement in-session). **Do NOT come back asking "should I hand this to a subagent?"** — that decision is made; you're executing it.
- Hand off the grilled acceptance test as the contract; the tier implements, it does not re-litigate decisions the grill already locked.

## Red Flags — STOP
- "The failure mode isn't a wrong design decision, so I'll skip grilling."
- "I'll just pick sensible defaults and note them." (did you hit NFR + security?)
- The human said "just ask me, don't read the code" — and you asked them facts the code answers. (Facts are yours; investigate.)
- Time pressure → questions stripped of recommendations. (Recommendations ARE the short form.)
- "No one's reachable tonight, so I'll skip the grill / proceed past the gate." (the grill is self-directed; the gate is blocking — park with decisions persisted, don't proceed)
- "I still have more questions to ask." — but none would change behavior, state, failure semantics, data, security, compatibility, or NFRs. (STOP GRILLING — materiality bounds the grill, not exhaustion)
- About to write the acceptance test and the spec gate hasn't approved the decisions. (No test tokens before the gate — the test encodes the FINAL spec, amendments included.)
- About to fold a blanket "all defaults" over an IRREVERSIBLE decision (migration / money semantics / public contract / security posture) — each needs its own named confirmation.
- "The human amended a decision — I'll adjust the matching test line and move on." (The test is derived from the final spec as a whole; a patched draft encodes the draft.)

## Common Mistakes
| Mistake | Fix |
|---|---|
| Skip the grill, hand a subagent a fuzzy spec | Grill every dimension (incl. NFR + security) first; a fuzzy spec wastes the whole subagent run. |
| Collapse the grill to "sensible defaults" | Deciding deliberately after interrogating ≠ assuming silently. |
| Asked the human a fact the environment answers ("just ask me — I know the system") | Facts are yours: investigate, then decide or ask a decision. The human knows intent, not their code's actual shape. |
| Time pressure → questions stripped of recommendations "to keep it short" | Recommendations are the short form — "all defaults except 3" beats composing answers. Stripping them is the failure mode. |
| Dependent question asked flat while its root is still open | Make it conditional ("only if Q1 = …") or hold it for the next round; a root overridden later moots its flat dependents. |
| Writes the acceptance test before the spec gate | Gate the decisions first — the gate may amend the spec, and a pre-gate test anchors to the draft. The test is derived from the FINAL spec, after the gate. |
| A test-writing question the grill/gate didn't decide, resolved silently in the test | Test-local mechanics are yours; anything that changes behavior/state/failure/data/security/compat/NFR goes back to the human. |
| Spec doc skipped because "the test file records it" | Tests are for running, docs are for recalling. Default ON; only an explicit decline skips. |
| Skip the approval gate because "tests encode my assumptions" | The gate checks direction on the decisions; tests catch logic. No human? PARK at the gate — the grill already ran and is persisted; that's what they'll review when they arrive. |
| An IRREVERSIBLE decision approved inside a bulk "all defaults" | Blast-radius tags (reversible / costly / IRREVERSIBLE — migration, money semantics, public contract, security posture): the irreversible ones demand a named confirmation each; a blanket OK does not cover them, and unanswered still parks. |
| Route everything to base `spec-tdd` | A fuzzy+blast-radius-critical feature goes to `spec-tdd-adversarial`; fuzzy+coverage-needed to `spec-tdd-coverage`. Pick the tier by stakes. |
| Route everything money-ADJACENT to the adversarial tier (the fintech trap — observed: a codebase that routed nearly everything there) | Blast-radius litmus: only silent wrongness that MOVES money / CHANGES auth / IRREVERSIBLY corrupts data goes adversarial. Display/reporting/reference/internal tooling → coverage or base; safety-net-bounded → one tier down; batches per unit. |
| Re-litigate grill decisions inside the tier | The acceptance test + grilled decisions are the contract; the tier implements, not re-decides. |
| After RED, come back and vaguely ask "hand off to a subagent?" | The gate (Phase 1, step 3) is the single checkpoint and must bundle the routing choice; once approved, INVOKE the tier — don't re-ask. |
| Hunt the filesystem for `SKILL.md` / "how are these skills organized?" to route | Invoke the tier BY NAME via the Skill tool; never search the disk for skill files. |
| Reads only the tail of the RED error list, then routes | Full-list RED-purity check: errors about EXISTING symbols (wrong ctor arity, ambiguous overloads, unused imports) = your test's defect — fix before routing (unless the spec itself explicitly changes that symbol — breaking-change feature, good RED). The tier skips its Phase 1, so no one downstream re-audits the RED. |
| Fuzzy + critical requirement ran the plain grill | The blind-spot risk sits on the decisions themselves — `adversarial-grill-spec-tdd` attacks them (pre-gate) and the final-spec test (pre-dispatch) with an independent context. |
