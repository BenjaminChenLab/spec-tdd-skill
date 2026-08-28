# spec-tdd — test-first development skills for Claude Code

**Version 1.8.2** · [Protocol](PROTOCOL.md) · [Changelog](CHANGELOG.md) · [License](LICENSE)

A family of [Claude Code](https://claude.com/claude-code) skills enforcing **a protocol for preventing correlated test/implementation failure in AI-generated software** (the technical name for the *green lie*). Executable specifications, agent-boundary isolation, and independent verification for agentic TDD.

## The problem: the green lie

Let one agent write both the tests and the code and you get the **green lie** — tests that pass only because the same mind wrote both, so they mirror the implementation's assumptions, skip the edges it forgot, and assert tautologies. The suite goes green; the code is still wrong. **You let the same brain be both referee and player.**

Most TDD guidance fights this with *prompting* — exhorting the agent to stay objective. Same agent, same context, trying not to fool itself. Under pressure, it loses.

## The fix: an agent boundary

`spec-tdd` doesn't persuade; it changes the **structure**. One agent (the orchestrator) writes the acceptance test — the spec — *before any implementation exists*, then hands it to a *different* agent (the implementer) as the contract. Written before the impl, by a different context, the test cannot have been reverse-engineered to mirror it (it can still be *wrong* — see below):

> **"Must be RED first" is the built-in green-lie detector.**

This isn't a new religion — it's established software engineering (black-box testing, contract / seam-driven design, independent verification) ported to agent orchestration. The agent boundary turns "don't fool yourself" from a discipline into a structural guarantee **against the green lie** — the test cannot have been reverse-engineered to mirror the impl. It does not guarantee the spec is *right* (a misread requirement still makes a bad test); that failure mode is handled by other mechanisms — RED-first, the Phase-3 adversarial read, the grill, and the independent attacker.

Each skill was authored and pressure-tested with the TDD-for-docs process (baseline a failure mode without the skill, then write the skill to counter it).

## Architecture & Agent Boundaries

The anti-green-lie guarantee comes from **separating spec-authoring and implementation into different agent contexts**; `spec-tdd-adversarial` adds a third, independent context (an attacker) for critical paths; `spec-tdd-lite` crosses the boundary exactly once — for the review — and implements in-session. Two views — the core principle, then the complete flow.

### Core — why the agent boundary matters

```mermaid
flowchart LR
    subgraph O["Orchestrator context"]
        A["Write acceptance test (the spec)"]
        V["Re-run it to verify"]
    end
    subgraph I["Implementer subagent"]
        W["Write impl to pass (GREEN)"]
    end
    A ==>|"hand off as contract; must be RED first"| W
    W --> V
    V --> D(("Done"))
```

The acceptance test is written in the orchestrator's context *before* the impl exists, then handed to a different context (the implementer) as the contract. Crossing that boundary is what stops the test from mirroring the impl — the whole point.

### Complete flow

```mermaid
flowchart TD
    subgraph F["Front-ends (optional)"]
        GR["grill-spec-tdd — grill requirement: business, edges, state, NFR, security"]
        AG["adversarial-grill-spec-tdd — fuzzy+critical: grill + independent auditor (decisions pre-gate, test pre-dispatch)"]
        ES["spec-tdd-escalate — route settled req by stakes (no grill, no gate)"]
    end

    subgraph O["Orchestrator context"]
        GT{"Gate: human OK on the SPEC (grilled decisions)?"}
        T["Write acceptance test from FINAL spec (RED)"]
        RT["Route to tier by stakes"]
        V["Re-run acceptance test + adversarial read (+ gap-check)"]
        P{"Pass and valid?"}
    end

    subgraph I["Implementer subagent"]
        IM["Minimal impl + own unit tests"]
        IC{"Green?"}
        ERR(["STOP: ERR-01/02/03 + trace"])
    end

    subgraph ADV["Adversarial context (spec-tdd-adversarial)"]
        ATK["Independent attacker: wrong-but-green impl + branch hunt + terminal dry-loop audit (rotating lenses)"]
    end

    subgraph LT["spec-tdd-lite (in-session tier)"]
        LT1["Write acceptance test (RED)"]
        LT2["Implement in-session (inner loop)"]
        LT3["One fresh-context test review"]
    end

    GR --> GT
    AG --> GT
    GT -->|"approve (amendments = final spec, persisted) — no answer = PARK"| T
    T --> RT
    ES --> RT
    RT -.->|"one small unit / non-critical"| LT1
    LT1 --> LT2
    LT2 --> LT3
    LT3 --> DONE
    RT -->|"tier writes its own Phase-1 test (RED) on non-front-end arrivals"| IM
    IM --> IC
    IC -->|"no, repair"| IM
    IC -.->|"3 failed"| ERR
    IC -->|yes| V
    V -.->|"adversarial tier only"| ATK
    ATK -->|"harden test / add cases"| T
    V --> P
    P -->|Yes| DONE(["Done"])
    P -->|"SPEC (re-open req)"| T
    P -->|"TEST (fix test)"| T
    P -->|"IMPL (re-delegate)"| RT
```

- **Orchestrator → Implementer** is the delegation handoff (acceptance test = contract); the **circuit breaker** caps the implementer's repair loop — STOP after 3 attempts OR the same root cause on any two attempts — and tags `ERR-01 env · ERR-02 logic · ERR-03 syntax`.
- **Verification is orchestrator-run** ("don't trust the subagent's self-report"): it re-hashes the acceptance test to prove the implementer didn't edit it (**SPEC-INTEGRITY**), then **routes by root cause** — three buckets: SPEC (re-open the requirement) → rewrite the test; TEST (requirement right, test weak/incomplete) → strengthen the test; IMPL (code wrong) → re-delegate.
- **No unaudited test crosses the boundary.** Before any implementer dispatch, a fresh-context reviewer checks the acceptance test encodes its spec — every line asserted with discriminating power, wrong-but-plausible readings named, over-assertion and silent interpretations surfaced (**I13**, family-wide; lite reviews post-GREEN; adversarial-grill's Part B is this audit at adversarial grade).
- **Context3 (attacker)** is `spec-tdd-adversarial` only. `grill-spec-tdd` gates the **spec** (the grilled decisions) *before* the acceptance test is written — the test is derived from the **final**, gate-approved spec — then routes to the matching tier; `spec-tdd-escalate` is the no-grill sibling — it routes a settled requirement straight to the matching tier, and that tier writes the test in its own Phase 1.
- **`spec-tdd-lite`** stays in the orchestrator's context: acceptance test (RED) → in-session inner loop → ONE fresh-context review dispatch → done (stall → promote to `spec-tdd`).

## The family

Seven skills, organized as **a verification ladder + three front-ends** — `grill-spec-tdd` (grill a fuzzy requirement, gate the spec, then route), `adversarial-grill-spec-tdd` (fuzzy **+ critical**: grill, independent auditor attacks the decisions before the gate and the final-spec test before dispatch), and `spec-tdd-escalate` (route a settled requirement, no grilling):

| Skill | Role |
|---|---|
| [`spec-tdd-lite`](skills/spec-tdd-lite/SKILL.md) | The in-session entry tier. Acceptance test (RED) → implement it yourself → **one fresh-context review dispatch**. For ONE small/non-critical unit in a session you'll clear after. |
| [`spec-tdd`](skills/spec-tdd/SKILL.md) | The base. Orchestrator writes the acceptance test (RED), gets a fresh-context **encoding audit**, delegates to one subagent, verifies by running it. **Multi-unit runs**: a bug list or task-split feature loops the phases per unit — the agent boundary is per unit. |
| [`spec-tdd-coverage`](skills/spec-tdd-coverage/SKILL.md) | `spec-tdd` + **coverage evidence**: the subagent declares a case-list *before* impl and reports per-class branch %; the orchestrator gap-checks. |
| [`spec-tdd-adversarial`](skills/spec-tdd-adversarial/SKILL.md) | `spec-tdd-coverage` + an **independent attacker** (a third agent context) that tries to write a wrong-but-green impl and hunts uncovered branches, then a **terminal dry-loop audit** — fresh auditors rotating lenses (test-strength / plan fidelity / deployment-ops / production quality); stops on 2 consecutive clean rounds, capped at 4 (5 with the `dryout` flag — the only difference); a cap hit with live findings asks the human whether to continue. Top tier — critical paths only. |
| [`grill-spec-tdd`](skills/grill-spec-tdd/SKILL.md) | A **front-end**: interrogate a fuzzy/high-stakes requirement ("grill"), gate the SPEC (the grilled decisions) with a human **before any test is written**, derive the acceptance test from the **final** spec, *then route* to whichever verification tier fits. |
| [`adversarial-grill-spec-tdd`](skills/adversarial-grill-spec-tdd/SKILL.md) | The **critical-grade front-end**: grill-spec-tdd plus an **independent grill-auditor** dispatched twice — the decisions (incl. materiality stops) attacked BEFORE the gate, the final-spec acceptance test attacked after it (pre-dispatch) — independence at the cheapest moments (no impl tokens spent). Fuzzy + critical (money/auth/data-loss) only. |
| [`spec-tdd-escalate`](skills/spec-tdd-escalate/SKILL.md) | A **front-end** for SETTLED requirements: skips grilling and auto-routes to whichever verification tier fits the stakes — full-auto, no gate. |

`spec-tdd-lite` is the entry rung — in-session (no implementer dispatch, one review dispatch). Above it the ladder inherits upward: `spec-tdd` → `spec-tdd-coverage` → `spec-tdd-adversarial`. `grill-spec-tdd` and `spec-tdd-escalate` are orthogonal front-ends: `grill-spec-tdd` grills a fuzzy requirement then routes; `spec-tdd-escalate` routes a settled one with no grilling. `adversarial-grill-spec-tdd` is grill's critical-grade upgrade (fuzzy + critical only; typically routes onward to `spec-tdd-adversarial`). Front-ends compose with the tiers — `{grill, escalate} × {lite, spec-tdd, coverage, adversarial}` plus `adversarial-grill × {spec-tdd, coverage, adversarial}` (never lite: a critical surface doesn't go in-session) — all reachable **without** duplicating skills into monolithic combos.

Every **delegated** tier's handoff carries a **circuit breaker** (STOP after 3 repair attempts OR the same root cause on any two attempts; tag the failure `ERR-01` env/dep · `ERR-02` logic · `ERR-03` syntax, with a truncated trace) and **three-bucket failure routing** — SPEC (re-open the requirement) → rewrite the test; TEST (requirement right, test incomplete) → strengthen the test; IMPL (code wrong) → re-delegate with the error tag. `spec-tdd-lite` has no handoff: its in-session stall breaker (same trip rules) promotes to `spec-tdd` instead.

## When to use which

```
Requirement SETTLED and you want the tier picked for you?
  yes → spec-tdd-escalate   (auto-routes by stakes; no grilling, no gate)

Otherwise pick the tier yourself:
Requirement FUZZY or high-stakes?
  yes → Critical surface? (money movement / auth-permissions / data-loss)
          yes → adversarial-grill-spec-tdd   (grill + independent audits: decisions pre-gate, test pre-dispatch — then it routes to the tier)
          no  → grill-spec-tdd   (grill + gate the spec, then routes to the right tier)
  no  → Correctness-CRITICAL? (money movement / auth-permissions / data-loss)
          yes → spec-tdd-adversarial
          no  → Need branch-coverage EVIDENCE? (large/subtle branch surface, weak tests, compliance)
                  yes → spec-tdd-coverage
                  no  → How many units?
                          ONE small unit (bugfix-scale, non-critical,
                          session cleared after)
                            → spec-tdd-lite   (in-session: test → implement → one review)
                          MULTIPLE units (bug list / feature split)
                            → spec-tdd       (multi-unit run: boundary per unit)
                          otherwise → spec-tdd      (the cheap default)
```

Rule of thumb: requirement already settled and you just want it routed? Use `spec-tdd-escalate`. Fuzzy, or you want to interrogate it first? Start with `grill-spec-tdd` — it grills and routes to the matching tier for you. Fuzzy AND on a money/auth/data-loss surface? `adversarial-grill-spec-tdd` — an independent auditor attacks the grill itself before anything is built. One small unit and a session you'll clear after? `spec-tdd-lite`. Several units — a bug list, a split feature? `spec-tdd` as a multi-unit run.

## How it relates to the `superpowers` plugin

Complementary, not redundant:

- `superpowers:test-driven-development` is single-agent atomic TDD (RED→GREEN→REFACTOR). `spec-tdd` *uses* that discipline but splits it across the agent boundary — adding the structural green-lie defense that single-agent TDD cannot provide.
- `superpowers:subagent-driven-development` verifies via a reviewer reading a *prose spec*; `spec-tdd` verifies by *running an executable spec* (the acceptance test). Different bets, and `spec-tdd` is far lighter (1 subagent vs implementer + 2 reviewers per task). `spec-tdd`'s multi-unit runs close the cadence gap — per-unit dispatch with between-unit verification — without giving up the executable oracle.
- `spec-tdd-lite` is the self-contained in-session option: a distilled red-green-refactor loop inline, plus the one fresh-context test review that single-agent TDD cannot give itself.

You do **not** need `superpowers` installed — `spec-tdd` is self-contained.

## Installation

Copy the skills into your personal skills directory:

```bash
# from this repo's root
cp -r skills/* ~/.claude/skills/
```

Then invoke in Claude Code with `/<skill-name> <feature>`, e.g.:

```
/grill-spec-tdd add coupon discounts to checkout (Java/Spring, Order at src/main/.../Order.java)
```

## A quick walkthrough

1. **Grill** — `grill-spec-tdd` interrogates every dimension in batches (business logic, boundaries, state transitions, NFRs, security/fraud) and forces an explicit decision on each.
2. **Gate the SPEC** — the grilled decisions (plain language, amendments welcome) + the tier choice surface for ONE human OK **before any test is written**; the approved + amended decisions are the **final spec**, persisted as a doc by default (`docs/specs/…` — say the word to skip).
3. **Write the acceptance test** — derived from the final spec; behavioral, black-box; run it to confirm RED; an independent **encoding audit** (fresh context) checks it before routing.
4. **Route** — `grill-spec-tdd` picks the tier by stakes (e.g. money → `spec-tdd-adversarial`).
5. **Delegate** — a subagent implements to green; the circuit breaker guards against runaway loops.
6. **Verify** — the orchestrator runs the acceptance test itself, reads it adversarially, reports.

For plain `spec-tdd`, skip the grill batch and route — tiers run **after** the spec is final, so they add no human gate of their own; if the spec isn't a doc (settled only in the conversation) it asks once whether to persist one (default yes); the test surfaces to the human at verification time. For fuzzy **+ critical** requirements, `adversarial-grill-spec-tdd` dispatches an independent auditor twice: after the grill (attacking the decisions and materiality stops, pre-gate) and after the test is written from the final spec (pre-dispatch) — the family's independence principle moved to the cheapest moments. For `spec-tdd-escalate`, skip the grill entirely — give it a settled requirement and it auto-routes to the right tier (no gate; the tier writes the test in its own Phase 1). For `spec-tdd-lite`, there is no delegation: acceptance test RED → implement in-session → one review dispatch → surface the test + findings. For a batch — a bug list or a split feature — `spec-tdd` runs multi-unit: unit plan (surfaced, not gated — the spec is already final) → the phases per unit (grouped dispatches where modules overlap) → batch summary.

## Why it works

- **Agent-boundary = anti-green-lie.** A test written before the impl exists, by a different context, can't have been reverse-engineered to mirror it (it can still be *wrong* — handled by the mechanisms below).
- **In-session without going bare.** `spec-tdd-lite` keeps acceptance-test-first and adds a fresh-context review — the two cheap structural defenses — for ONE small unit in a session you'll clear after.
- **Human validates WHAT, agent validates HOW.** The pipeline separates the two failure modes a same-agent flow conflates: a *wrong spec* is the human's call — in the grill front-ends, a gate on the **decision spec before any test is written** (amendments fold into the final spec the test then encodes); in the tiers, reviewing the surfaced **test** — and a *wrong implementation* is the agent's call — caught by **running** the test. Review WHAT, not HOW.
- **Coverage as evidence, not luck.** `spec-tdd-coverage` makes branch coverage a measured, reported artifact with a case-list to audit — not a hopeful side-effect of green tests.
- **Independence for critical paths.** `spec-tdd-adversarial` adds a third context (an attacker) that a diligent same-context agent cannot give itself.
- **Grill before you build.** `grill-spec-tdd` forces every requirement dimension explicit (incl. NFR + security) instead of collapsing to "sensible defaults" under pressure.
- **Independence at the cheapest moments, for fuzzy-critical work.** `adversarial-grill-spec-tdd` moves the family's independence principle as far forward as it can go: an independent auditor attacks the grill's decisions (incl. materiality stops) **before the gate**, and the final-spec acceptance test **before dispatch** — zero implementation tokens spent either way. Re-reading is not the fix — only independence is.
- **Spec docs persist by default.** When no spec/plan/blueprint doc exists, the run persists one (`docs/specs/YYYY-MM-DD-<feature>.md`) — the final decision spec at the grill gate, or the requirement + interpretation decisions + test path at tier Phase 1 — so later recall (requirement re-opens, PR review, audits) never depends on session memory. Only an explicit decline skips it.
- **Auto-route when decided.** `spec-tdd-escalate` picks the tier for you when the requirement is already settled — no grilling, no gate, route-only.

## License

MIT — see [LICENSE](LICENSE).
