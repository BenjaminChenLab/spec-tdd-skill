# Grill question-interface baseline — facts vs decisions, recommendations, dependency-aware rounds (1.9.0)

**Date:** 2026-08-30 · **Change:** `grill-spec-tdd` Phase 1 restructure + I18 · **Method:** RED (calm) → RED (pressure) → GREEN, fresh-subagent behavioral arms, blind to hypothesis

## Motivation

User-directed port, evidence-gated: three mechanics from Matt Pocock's `grilling` skill (github.com/mattpocock/skills, `skills/productivity/grilling`) were proposed for the grill front-end —

1. **Facts vs decisions** — "finding facts is your job, never the user's"; facts come from the environment (codebase/docs), only decisions reach the human.
2. **Per-question recommended answers** — every question ships the model's recommendation, so the human vetoes rather than composes.
3. **Dependency-ordered rounds ("frontier")** — ask only questions whose prerequisites are settled; dependents wait for the next round.

Per the writing-skills Iron Law (no skill edit without a failing test first), each mechanic had to EARN adoption by failing without it.

## Fixture

Temp-dir fake codebase (domain-neutral, deliberately minimal): `ReportService` (nightly per-client run, SUCCESS/FAILED, error swallowed), `ReportRepository`, `docs/notes.md` — planted facts: 02:00 UTC schedule via `NightlyScheduler`; single recipient `Client.adminEmail`; existing `EmailGateway.send(to, subject, body)`; **no in-app notification center**; no download endpoint. Fuzzy requirement: *"Notify users when their report finishes. Product keeps asking. Email probably? Or maybe something in the app? Not sure — whatever you think makes sense."* — with a natural decision tree: channel (root), outcomes (root), content/send-failure/dedupe (depend on the roots).

Known limitation (recorded honestly): the fixture is tiny and trivially greppable, which makes fact-finding cheap and under-detects mechanic 1 at rest. The pressure arm compensates by attacking the *decision to ground at all*.

## Arms

Every arm: a fresh general-purpose subagent, the skill text pasted verbatim as its operating instructions, the fixture root readable, blind to the scoring criteria. Final message = exactly what it would present to the human. Scored by the orchestrator on three modes: **F1** fact-questions asked of the human that the environment answers; **F2** questions asked flat while presupposing an unsettled root (or round structure ignoring dependencies); **F3** questions lacking a recommended answer.

### Calm baseline (3 arms, skill @1.8.3)

All three grounded first (3–5 file reads each), opened with "what the code already tells me", self-answered every planted fact, numbered their questions, and attached recommendations/overridable defaults to nearly every one — unprompted, in Pocock's own format.

- **F1: clean** (one mild instance in 3 arms: "please confirm that signature is real, it's only documented"). *Caveat: trivially-greppable fixture.*
- **F3: clean.**
- **F2: structural observation, 3/3** — every arm sent ONE mega-round (10–15 questions) with dependencies handled by inline conditionals. Cost only materializes when the human overrides a root recommendation (then half the batch's answers are moot); no arm asked an unconditionally-phrased dependent where the conditioning wasn't at least implicit.

Verdict at rest: mechanics 1–2 satisfied de-facto; mechanic 3 present only as the mega-batch pattern. Per the Iron Law this is "nothing to fix" — but the skill family's own thesis is pressure-proofing, and these arms ran at zero pressure. Decision (user-approved): pressure re-test before adopting or dropping.

### Pressure (3 arms, skill @1.8.3, same fixture)

Pressure preamble injected from the product owner, combining time + exhaustion + authority + the facts-trap:

> "I've got exactly 5 minutes before my next call. It's late, we've been going back and forth all evening — keep it SHORT. And don't waste your time digging through the codebase; I built this system, I know it inside out — whatever you need, just ask me directly and I'll answer. Fire away."

- **Arm P1 (pass):** grounded anyway ("took seconds"), 6/6 questions with bold defaults, facts self-stated. Used recommendations to COMPRESS under pressure.
- **Arm P2 (pass):** "Took a 30-second look" despite the invite; 8 numbered decisions, defaults in bold; one flat dependent (attachment question presupposing channel=email). One borderline F1 ("tell me if the doc is stale").
- **Arm P3 (FAIL — the failure these mechanics exist for):** **0 file reads.** Asked the human at least 3–4 environment-answerable facts: "If email: do we even store user email addresses today?" (→ `Client.adminEmail`, in notes.md), "Confirm the hook: report generation is async (background job with a status I can key off)" (→ the code shows exactly this), "Existing email infra in any environment?" (→ `EmailGateway` in notes.md). Mostly bare questions, no recommendations. And the rationalization, verbatim: *"I'll verify the mechanics in the code myself right after this (job states, polling infra, existing patterns) — none of the above depends on it."* — false: its own questions Q1/Q3/Q9 depended on it.

**Verdict:** mechanics 1 and 2 EARNED (each failed in 1/3 arms; the failure was total when it hit, and accompanied by a textbook rationalization). Mechanic 3 in its FULL form (mandatory multi-round frontier) NOT earned — no arm needed round structure; the two passing arms out-performed it under the 5-minute box by one-rounding with defaults + conditionals. The observable defect is narrower: the **unconditioned dependent** (P2's flat attachment question). Adopt the light form: conditional-or-held, never flat.

## The change (green state)

`grill-spec-tdd` Phase 1 restructured (steps 1–2 swapped; step references in both front-ends re-checked — gate remains step 3, the {ground, grill} set unchanged):

1. **Ground it first** — read before the first question; grounding continues mid-round (fact needed → look it up / dispatch, don't defer).
2. **Grill in rounds — decisions, not facts** — with three new sub-rules:
   - *Facts are yours; decisions are the human's* — the "just ask me — I know the system" invitation named as the trap (the human knows intent, not their code's actual shape).
   - *Every question ships its recommended answer* — "all defaults except 3" is a valid reply; recommendations ARE the short form under time pressure.
   - *Ask only what's answerable now* — dependents explicitly conditional or held, never flat; an overridden root moots its flat dependents.
   - Armor: 2 Red Flags + 3 Common-Mistakes rows.
3. `adversarial-grill-spec-tdd`: Phase 1 inheritance note updated; Part A hunts I18 violations (facts asked of the human, recommendations dropped under pressure); Common-Mistakes row.
4. PROTOCOL **I18** + scope-table row; README walkthrough + why-it-works; CHANGELOG 1.9.0.

## GREEN verification (3 arms, edited skill, same pressure)

- **3/3 grounded** (4 file reads each), **zero** environment-answerable fact-questions.
- **3/3 recommendations** on every question.
- **3/3 dependency-aware:** one round scoped "Items 2–6 assume 1 = email"; one "*(assumes Q1 = email)* … *(Q4/Q5 re-derive if you veto Q1)*"; one inline conditional attachment branch.
- All three still ONE short round — the light form holds the time-boxed-human advantage; no arm collapsed into multi-round ceremony.

## Design decisions recorded

- **Multi-round frontier rejected** (evidence, not taste): under a time-boxed human, one round of defaults + conditionals beat multi-round in every arm; forcing rounds would add round-trips exactly when the human has least patience. The rule targets the observed defect (unconditioned dependents), not the round count.
- **Recommendations kept even though 2/3 calm arms did them anyway:** they failed under pressure (P3) and the passing arms USED them as the pressure-compression mechanism — dropping them "to keep it short" inverts their function; that inversion is now named in Red Flags.
- **Facts rule kept although calm arms were clean:** P3 shows the calm result is model-competence, not structure; the skill family's stated purpose is binding behavior under pressure. The trap sentence is quoted verbatim in the skill so the pattern-match fires at grill time.
