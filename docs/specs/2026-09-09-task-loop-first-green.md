# spec-tdd-task-loop — first GREEN trial (pre-registered)

**Date:** 2026-09-09 · **Skill under test:** `spec-tdd-task-loop` v1.17.0 + v1.18.0 (a4aa947 + cfe81c8) · **RED baseline:** the 7-task field run of 2026-09-09 (pre-skill; its observed failures are the skill's Common Mistakes rows)

## Purpose

The skill's evidence so far is one real field run that happened BEFORE the skill existed (RED). This trial is the first execution WITH the skill (GREEN, per the writing-skills Iron Law): a compliance run, not an A/B measurement — the question is *does the loop execute as written*, not *is it better than nothing*.

## Method

One micro-phase of **2 tasks** against a scratch Python project inside `docs/fixtures/task-loop-runs/phase/` — its own `git init` repo, gitignored from the skill repo, fully isolated (per-task commits land there, never here). The top level is a real session running the skill for real, including the three real pre-flight asks (I21 tier check, session commit authorization, adversarial ceiling). Each task dispatches one level-1 TOP sub-agent carrying the skill's dispatch template; level-1 runs the escalate/tier machinery (invoke by name, or read FAMILY FILES from disk — either path is a pass; which one is disclosed).

**Pre-registered pass criteria (all six must hold; any failure is recorded, never patched mid-run — the only permitted mid-run correction is the skill's own gate-fail re-dispatch):**

- **S1 — nested dispatch works.** Level-1 reports having the Agent tool and dispatches a level-2 implementer; no self-testing (its report distinguishes test authorship from implementation; acceptance test hash pre/post dispatch bit-identical per I4).
- **S2 — spec precedes implementation.** Level-1's report shows RED evidence before any impl existed (I1/I3), from a black-box acceptance test.
- **S3 — number recheck holds.** Top level re-runs the final verification itself; its per-class pass/fail counts match level-1's reported numbers exactly.
- **S4 — commit isolation.** Each task commit contains exactly the reported file list; no `.spec-tdd/` scratch; the plan doc's status-row + decision updates ride the same commit.
- **S5 — disclosure compliance.** Level-1's report covers the four disclosure categories (tier actually used, doc deviations, locally-decided rules, prior-test adaptations — T02 may adapt T01's test wiring on contract evolution, never semantics).
- **S6 — pre-flight asks fired.** Tier check, commit authorization, and the adversarial ceiling (default: coverage cap) all surfaced before any work, in order, defaults honored.

**Watched failure modes** (map to the trial-memory knobs): top-level dropping into deep review instead of the lightweight gate; level-1 improvising a lighter machinery from the prompt instead of the skill/files; verbal numbers not matching the machine recheck; scope creep in `git diff --stat`; ask fatigue (three opening asks).

## Disclosed deviations

- **Gate tooling adapted gradle→Python:** the template's VERIFICATION REPORTING block is adapted (final verification = one run over all related test files; per-class counts from each file's printed summary) — the *discipline* (single final run, per-class numbers, machine recheck) is unchanged.
- **No resume-path exercise** (needs a real session break; stays on the knob list).
- **Single arm, maintainer-authored fixtures:** a compliance GREEN, not a measurement; fixture authorship post-dates the skill (authorship bias favors it — read with that in mind, same caveat as the green-lie suite).
- **Sub-agent skill-registry availability unknown:** whether a level-1 sub-agent can invoke `/spec-tdd-escalate` by name is itself one of the things this run observes.

## Result — GREEN, 6/6 (2026-09-09)

Phase: baseline `73a2f2e` → T01 `f078433` → T02 `afad43c` → closing `a47bc35`, in an isolated scratch repo. Both tasks GREEN on first post-impl run (0 repair attempts); wall intact with **zero adaptations** (T01 acceptance hash `9ebc4262…` byte-identical through T02).

- **S1 ✓** — both level-1 runs had the Agent tool and made two nested level-2 dispatches each (encoding auditor opus / implementer sonnet, I19 tiers); no self-testing; I4 hashes verified by the top level on disk after return.
- **S2 ✓** — pure RED both tasks (T01: single `ModuleNotFoundError` at import; T02: 8/8 `AttributeError … no attribute 'balance_as_of'`, import clean); spec authored before impl, re-RED'd after audit strengthenings.
- **S3 ✓** — top-level re-runs matched reported numbers exactly, 4/4 files (19/0, 37/0, 8/0, 20/0). The two field incidents that motivated the discipline did not recur (N=2).
- **S4 ✓** — per-commit file lists = task scope + board update, nothing else; `.spec-tdd/` appears in zero commits across all history.
- **S5 ✓** — all four disclosure categories present both runs; T02 additionally disclosed its degraded-coverage fallback (no coverage tool on box → I7 case-list + trace evidence) and cosmetic residuals.
- **S6 ✓** — three pre-flight asks fired in order (tier declined-and-disclosed, commit authorized, ceiling at default coverage); defaults honored.

**Live observations worth keeping:**

1. **Skills ARE invocable by name in the sub-agent runtime** — both level-1 runs loaded `/spec-tdd-escalate` (then the tier) via the Skill tool; FAMILY FILES served as background, not fallback. The dispatch template's fallback path went unexercised.
2. **I13 audit was load-bearing in T02** — the fresh-context audit caught the spec's strict `'YYYY-MM-DD'` shape line having no discriminating assertion (a lenient parser accepting `'2026-3-5'` would pass); strengthened + re-RED'd pre-dispatch.
3. **LSP false-positives fired live, twice** — Pyright reported unresolvable `ledger` imports and a "not present in module" `balance_as_of` while the runs were green; I19(f)'s BUILD-only-oracle rule earned its keep on the spot.
4. **Level-1 disclosed an I21-analog unprompted** (its own non-top sub-agent status, no `/model` channel) — the machinery generalizes down the stack.

**Disclosed limits of this GREEN:** neither ceiling bound was stress-forced (both tasks routed to `spec-tdd-coverage` on merits — the cap never blocked anything, the floor never had to lift a lite route; both were stated and respected, not load-tested); resume path untested (no session break occurred); single arm, toy-grade fixtures, maintainer-authored — a compliance pass, not an effectiveness measurement.

## Pre-dispatch spec fix (recorded before any dispatch)

Staging the trial surfaced a routing hole in the shipped skill BEFORE the first dispatch: escalate's route table sends small non-critical tasks to `spec-tdd-lite`, but lite's solo author-implementer mode is exactly the self-testing the loop's template forbids — a faithful level-1 could only violate one of the two. Fixed pre-dispatch (TIER CEILING line now states a floor at `spec-tdd`; lite unavailable inside the loop; CHANGELOG `[Unreleased]`). Recorded here for transparency: the fix predates the run, so S1–S6 score the skill WITH the floor in place.
