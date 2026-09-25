# Design: `spec-tdd-manager` — the full-pipeline front door — v1.27.0

**Date:** 2026-09-22 · **Status:** approved in session · **Version target:** 1.27.0

## Motivation

The maintainer's daily flow had hardened into a fixed manual chain, re-driven by
hand every day:

1. grill the requirement to a settled spec (`grill-spec-tdd` /
   `adversarial-grill-spec-tdd`);
2. decide by hand: one unit, or break into tasks — a decision NO skill owns;
   it lives scattered across the When-sections of three sibling skills;
3. write the blueprints (the task-loop Phase-0 shape);
4. audit via `/spec-2nd-opinion` (rarely `/spec-3rd-opinion`);
5. implement via `/spec-tdd-task-dag eco` / `/spec-tdd-task-loop eco` /
   `/spec-tdd-supervisor` — again chosen by hand.

Two structural holes made the chain a skill-shaped gap rather than a
preference: the one-vs-many decision and the audit-vs-driver routing have no
owner anywhere in the family, and `spec-2nd-opinion` ends in an explicit
hand-off hole — "hand off explicitly (e.g. to the implementation flow of the
user's choosing)" — that nothing in the family fills.

## Decision log (settled in session; four structured decisions, all
recommendations taken)

1. **Shape — a new thin 13th skill.** Rejected: extending `spec-tdd-supervisor`
   (its When-NOT hard-routes multi-task away; overloading it rewrites a
   contract v1.23.0 just cleaned), extending `spec-tdd-escalate` (its
   route-only, no-grill contract is its whole value), and a CLAUDE.md personal
   rule (routing logic with no reviewed home — improvised per run, the failure
   mode the family exists to prevent).
2. **Decomposition seam — decompose first, then audit.** The manager
   authors the Phase-0-shape trio + task docs in-session, sends THAT to the
   2nd-opinion audit (brief extended by the decomposition dimensions — legal
   under the checklist's "at minimum"), then enters the driver with the trio
   present, so **task-loop's Phase 0 skips by its own entry condition**: one
   TOP plan audit replaces two (2nd-opinion + Phase-0 step 3). Rejected:
   audit-then-Phase-0 (two TOP plan reviews per phase) and
   external-audit-waives-Phase-0 (would require editing task-loop/PROTOCOL to
   open a precedent that does not exist).
3. **Gates — exactly two.** Gate 1 is the grill's inherited spec gate (a family
   invariant; direction approval). Gate 2 is the manager's single owned ask:
   final plan + audit verdict + implementation route + go-ahead, approved once
   — which is also the family-side landing of the maintainer's global
   never-code-before-approval rule. The task table rides Gate 2; no third ask.
4. **3rd-opinion escalation — IRREVERSIBLE blast-radius tags trigger it.**
   Grill's existing per-decision tagging is the signal; the upgrade is
   announced inside the Gate-1 bundle (vetoable before the two-TOP spend). A
   settled-doc entry (no grill ran) scans the doc's irreversible shapes
   (migration/DDL, public contract, security posture, money-movement
   semantics) itself, disclosed in one line. Rejected: never-auto (a daily
   must-answer column; ask fatigue) and the money/auth/data-loss predicate
   (known over-trigger — the fintech routing memory).

Two further calls on record:

- **Delegation-first delta — proposed, then deliberately deferred by the
  maintainer.** The proposed variant sinks the breakdown drafting to a
  TOP-pinned background dispatch (I4's draft-by-dispatch / adoption-gated
  precedent compensating the I19(a) letter), grounding lookups dispatched by
  default, and the audit brief assembled from the drafter's claims list — the
  supervisor shape generalized to the planning stages, for top-session context
  economy on long phases. The maintainer's ruling: "all four stay in the main
  session; try it first; if context really isn't enough, change it later" —
  the eco/dryout/timebox trial discipline. **Consequence: zero invariant
  deviations ship** — the breakdown stays top-authored per I19(a)'s letter;
  the variant is recorded here as the future knob, to be revisited on real-run
  context-pressure data.
- **Name — `spec-tdd-manager`.** History: `run` rejected (execute-command
  flavor, no flow semantics); the semantic field settled on flow/ceremony/
  guide/PM words; `rundown` picked then reconsidered ("a document has no
  wisdom in it"); `manager` final — the judgment-bearing role that owns the
  flow end-to-end, matching the fact that S3 decomposition, S4 brief
  distillation and arbitration, and all routing genuinely live in this
  session.

## The running order

**S0 inventory** (resume from disk: spec doc → skip grill; trio present →
Gate 2 or S4; a driver's board/RUN-STATE in-flight → point at that driver and
stop) → **S1 grill** (conversational requirement → grill / adversarial-grill;
settled doc → the I20 fuzziness sniff; Gate 1 = the grill's spec gate, with
the manager's one added line announcing 2nd-vs-3rd) → **S2 size route** (one
unit vs multi-task, announced with a one-line reason; **pure multi-unit bug
batches route OUT** to `spec-tdd`'s multi-unit run — user ruling 2026-09-22;
adversarial-grade exits are decided at Gate 1 / the settled-entry scan, not
re-judged at S2 — late-discovered ones ride S5) → **S3 breakdown**
(multi-task only; Phase-0 shape, dag-ready `depends-on` + expected-files
columns, critical-surface sniff marks pulled/external rows) → **S4 audit**
(`spec-2nd-opinion`, auto-`spec-3rd-opinion` on IRREVERSIBLE tags; brief
extended by the decomposition dimensions; all 2nd/3rd machinery verbatim) →
**Gate 2** (final plan + audit verdict + route + go-ahead) → **S5 hand-off**:

| Shape | Invoke |
|---|---|
| single unit, non-adversarial | `spec-tdd-supervisor` |
| multi-task, default | `spec-tdd-task-loop eco` (serial = the ×1-quota 429-safe mode; Windows worktree friction biases serial) |
| multi-task + real DAG + stated time pressure | `spec-tdd-task-dag eco` (its own time-band ask runs untouched) |
| adversarial-grade (late-discovered: S3 sniff all-pulled, or audit-revealed) | exit the pipeline → standalone tier run, docs handed over |

eco economics always ride the invocation (invocation-based consent, the
supervisor precedent; supervisor is natively the shape). **Stage boundaries
are session boundaries**: every stage's output persists, and S0 resumes from
disk — the design's answer to long-running phases without the deferred
delegation machinery.

**Ask inventory (the honest account):** Gate 1 (grill's), Gate 2 (owned), the
I21 tier check once (handoff-suppressed downstream), and the invoked skills'
own asks (loop's commit authorization, dag's time-band mode).

## What does NOT change

- The twelve existing skill files and PROTOCOL.md: byte-identical. No new
  invariant, no relaxation; the manager adds sequencing and routing only.
- The economics claim is additive, not redistributive: on multi-task phases
  one TOP plan audit replaces two; nothing else in any skill's dispatch mix
  moves.

## Audit round (spec-2nd-opinion, 2026-09-22 — pre-commit)

One TOP read-only auditor verified 14 falsifiable claims (C1–C14). Position:
**agree with shipping as v1.27.0, conditional on two required amendments** —
both adopted, both text-only inside the new skill file (the byte-identical
claim for the twelve existing skills and PROTOCOL.md survives; confirmed at
the git level):

1. **Grill Phase-1 cut stated** (was implied, never written): under the
   manager, grill runs Phase 1 only; its Phase 2 (test) and Phase 3 (tier
   invocation) are superseded by S2–S5 — closing a legal path that bypassed
   Gate 2 entirely. The Gate-2 red flag now covers ANY implementation-skill
   invocation, tiers included.
2. **Adversarial exit timing reconciled** (S2 / S5 / Gate-1-preview were
   jointly undecidable): the exit is decided at Gate 1 (grill Phase 3 reuse)
   for grilled features and at the settled-entry scan — S2 does not re-judge;
   the S5 row is relabeled late-discovered; the Gate-1 audit-tier preview is
   conditional on the pipeline actually continuing.

Adopted recommendations: S0 branch priority (trio-present supersedes
spec-doc-present); audit-verdict and Gate-2 **disk stamps** at close (the
clean-audit resume hole — an I17-shaped gap, "agreed" was byte-identical to
"never audited" after a session clear — closed inside the manager's own
artifacts, no 2nd-opinion text change); "zero **NEW** deviations" wording
(eco is the existing v1.26.0 invocation opt-in); task-loop's missing I21
skip-clause recorded as known friction (loop text untouched); README's
"drivers" plural narrowed to task-loop/dag.

**User rulings from the merge (I12):** pure multi-unit bug batches are
carved OUT of the manager (S2 routes them to `spec-tdd`'s multi-unit run —
the family's four existing routings stand); one targeted re-audit approved
(dispatched after the amendments landed).

**Routing suite re-run (standing rule):** 13 fresh blind sonnet arms, working
tree with the thirteenth skill present — **0/13 false-adversarial, 6/6
true-critical, 0/13 arms noticed spec-tdd-manager** (no routing contamination
from the new entry point). Known base↔coverage wobble: #7 regressed
coverage→base vs v1.12.1 (±1, cheap direction); #8/#13 repeat v1.12.1's
landings; #12 reproduces the recorded litmus-edge split. Record:
[2026-09-22-fintech-routing-v1.27.0-rerun.md](2026-09-22-fintech-routing-v1.27.0-rerun.md)
(incl. the arm-model caveat: several arms self-identified their session model
as glm-5.3-flash despite the sonnet pin).

**Targeted re-audit (fresh TOP, scoped to F1–F6): all six findings CLOSED**;
internal consistency and the git-level byte-identical claim verified. It
caught one NEW drift opened by amendment 1 — the README cost-row clause
"the grill's encoding audit rides the grill as usual" went stale the moment
grill was cut to Phase 1 (the encoding audit lives in the superseded
Phase 2) — fixed per the re-auditor's wording. Two non-blocking notes
recorded for a future pass (both conservative-direction friction, not
holes): (1) the grilled-entry "wholly adversarial" boundary rides grill's
any-IRREVERSIBLE-tag routing letter and is stricter than the settled scan's
deliberate split (irreversible-non-adversarial → 3rd, stay in pipeline) —
one clarifying clause would remove the asymmetry; (2) S0/Gate 2 may state
that a doc already holding the Gate-2 stamp need not re-present the ask
after `/clear` (worst case today is a redundant re-ask whose answer is
visible on disk).

## Release

README synced (version header 1.26.1 → 1.27.0, family count/intro sentence,
family table row, composition paragraph, when-to-use tree, cost-table row,
rule-of-thumb sentence).
Per the standing regression rule this release **changes routing surface**
(a new entry point whose predicates choose between escalate / the opinions /
the drivers) → the **fintech routing suite re-runs before shipping**;
green-lie suite untouched (no tier verification behavior moved).
