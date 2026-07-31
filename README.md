# spec-tdd — test-first development skills for Claude Code

A family of [Claude Code](https://claude.com/claude-code) skills for **test-first feature development delegated to a subagent**, built around one core idea:

> **The acceptance test is the spec. It is written by the orchestrator *before* any implementation exists, in a *different context* than the implementer — so it cannot mirror the implementation. "Must be RED first" is the built-in green-lie detector.**

This structurally prevents *green lies* — tests that pass only because they were written by the same agent (or in the same context) that wrote the code, mirroring its assumptions. Single-agent TDD defends against this only with timing and discipline; splitting spec-authoring and implementation across the agent boundary turns it into a structural guarantee.

Each skill was authored and pressure-tested with the TDD-for-docs process (baseline a failure mode without the skill, then write the skill to counter it).

## The family

Four skills, organized as **a verification ladder + a grilling front-end**:

| Skill | Role |
|---|---|
| [`spec-tdd`](skills/spec-tdd/SKILL.md) | The base. Orchestrator writes the acceptance test (RED), delegates to one subagent, verifies by running it. |
| [`spec-tdd-coverage`](skills/spec-tdd-coverage/SKILL.md) | `spec-tdd` + **coverage evidence**: the subagent declares a case-list *before* impl and reports per-class branch %; the orchestrator gap-checks. |
| [`spec-tdd-adversarial`](skills/spec-tdd-adversarial/SKILL.md) | `spec-tdd-coverage` + an **independent attacker** (a third agent context) that tries to write a wrong-but-green impl and hunts uncovered branches. Top tier — critical paths only. |
| [`grill-spec`](skills/grill-spec/SKILL.md) | A **front-end**: interrogate a fuzzy/high-stakes requirement ("grill"), write the acceptance test, gate it, *then route* to whichever verification tier fits. |

The ladder inherits upward: `spec-tdd` → `spec-tdd-coverage` → `spec-tdd-adversarial`. `grill-spec` is orthogonal — a Phase-1 front-end that composes with any tier, so `grill × {spec-tdd, coverage, adversarial}` are all reachable **without** duplicating skills into monolithic combos.

Every tier's handoff carries a **3-strike circuit breaker** (stop after 3 repair attempts; tag the failure `ERR-01` env/dep · `ERR-02` logic · `ERR-03` syntax, with a truncated trace) and **dual-track failure routing** (spec-flawed → fix the test; impl-flawed → re-delegate with the error tag).

## When to use which

```
Correctness-CRITICAL? (money movement / auth-permissions / data-loss)
  yes → spec-tdd-adversarial
  no  → Need branch-coverage EVIDENCE? (large/subtle branch surface, weak tests, compliance)
          yes → spec-tdd-coverage
          no  → Requirement FUZZY or high-stakes?
                  yes → grill-spec   (grills, then routes to the right tier)
                  no  → spec-tdd      (the cheap default)
```

Rule of thumb: unsure? Start with `grill-spec` — it grills the requirement and routes to the matching tier for you.

## How it relates to the `superpowers` plugin

Complementary, not redundant:

- `superpowers:test-driven-development` is single-agent atomic TDD (RED→GREEN→REFACTOR). `spec-tdd` *uses* that discipline but splits it across the agent boundary — adding the structural green-lie defense that single-agent TDD cannot provide.
- `superpowers:subagent-driven-development` verifies via a reviewer reading a *prose spec*; `spec-tdd` verifies by *running an executable spec* (the acceptance test). Different bets, and `spec-tdd` is far lighter (1 subagent vs implementer + 2 reviewers per task).

You do **not** need `superpowers` installed — `spec-tdd` is self-contained.

## Installation

Copy the skills into your personal skills directory:

```bash
# from this repo's root
cp -r skills/* ~/.claude/skills/
```

Then invoke in Claude Code with `/<skill-name> <feature>`, e.g.:

```
/grill-spec add coupon discounts to checkout (Java/Spring, Order at src/main/.../Order.java)
```

## A quick walkthrough

1. **Grill** — `grill-spec` interrogates every dimension in batches (business logic, boundaries, state transitions, NFRs, security/fraud) and forces an explicit decision on each.
2. **Write the acceptance test** — behavioral, black-box; run it to confirm RED.
3. **Gate** — the test + decisions surface for a quick human OK *before* delegating (the cheapest direction-check).
4. **Route** — `grill-spec` picks the tier by stakes (e.g. money → `spec-tdd-adversarial`).
5. **Delegate** — a subagent implements to green; the circuit breaker guards against runaway loops.
6. **Verify** — the orchestrator runs the acceptance test itself, reads it adversarially, reports.

For plain `spec-tdd`, skip the grill batch and route; the gate surfaces the test at verification time.

## Why it works

- **Agent-boundary = anti-green-lie.** A test written before the impl exists, by a different context, can't mirror it.
- **Coverage as evidence, not luck.** `spec-tdd-coverage` makes branch coverage a measured, reported artifact with a case-list to audit — not a hopeful side-effect of green tests.
- **Independence for critical paths.** `spec-tdd-adversarial` adds a third context (an attacker) that a diligent same-context agent cannot give itself.
- **Grill before you build.** `grill-spec` forces every requirement dimension explicit (incl. NFR + security) instead of collapsing to "sensible defaults" under pressure.

## License

MIT — see [LICENSE](LICENSE).
