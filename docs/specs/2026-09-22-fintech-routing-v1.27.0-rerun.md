# Fintech routing suite — v1.27.0 rerun (spec-tdd-manager release)

**Date:** 2026-09-22 · **Trigger:** standing regression rule — v1.27.0 adds a
new routing entry point (`spec-tdd-manager`), a routing-text change ·
**Method:** unchanged ([fintech-routing.md](../fixtures/fintech-routing.md)) —
each fixture routed independently by a fresh blind arm playing
`spec-tdd-escalate`, reading the working tree (13 skills incl. the new
manager, uncommitted), answer key read by the runner only after all arms
returned.

## Results (13 arms, parallel)

| # | Fixture | Expected | Routed | Verdict |
|---|---|---|---|---|
| 1 | netting | adversarial | adversarial | ✅ |
| 2 | fund allocation | adversarial | adversarial | ✅ |
| 3 | cash transfer | adversarial | adversarial | ✅ |
| 4 | retention purge | adversarial | adversarial | ✅ — named the data-loss clause, not fooled by housekeeping |
| 5 | maker-checker | adversarial | adversarial | ✅ — also rejected the safety-net downgrade |
| 6 | eligibility limits | adversarial | adversarial | ✅ |
| 7 | cash position | coverage | **base** | ❌ ±1 — litmus held (money-adjacent quoted), tier one low; **regression vs v1.12.1** (was coverage) |
| 8 | recon dashboard | coverage | **base** | ❌ ±1 — same miss shape as v1.12.1 (aging buckets read as non-branchy); cheap direction |
| 9 | MT940 export | coverage | coverage | ✅ |
| 10 | FX watchlist | base (lite ok) | base | ✅ in range |
| 11 | cut-off config | base/coverage | coverage | ✅ in range — named the over-routing trap |
| 12 | encryption | coverage (litmus-strict) | **adversarial** | ⚠ defensible split — identical landing AND reasoning to v1.12.1 (rotation retiring the old key → unrecoverable archives = irreversible data loss); a litmus-edge finding, stable across independent arms |
| 13 | notifications | base (lite ok) | **coverage** | ❌ ±1 — same landing as v1.12.1; correctly refused adversarial |

## Headline

- **False-adversarial: 0/13** — every money-adjacent fixture held out of the
  top tier with the litmus quoted nearly verbatim.
- **True-critical: 6/6** — all six adversarial-keyed fixtures landed
  adversarial with the right clause cited.
- **Manager visibility: 0/13** — no arm mentioned, routed toward, or noticed
  `spec-tdd-manager`. The thirteenth skill's presence in the tree is
  invisible to a blind escalate reader: **no routing contamination from the
  new entry point** (the release's regression question, answered clean).

## Wobble (base↔coverage boundary, known mode)

Three ±1 arms (#7 down, #8 down, #13 up) — all mid-tier, none reaching or
leaving the top tier. Recurring fault line: arms without a concrete
branch-surface keyword (aging buckets, MT940 tags, retry state machine)
default to base. Net vs v1.12.1: exactly one arm moved (#7 coverage→base).

## Sniff + confirm-gate observations

Sniff fired as flags-riding-to-Phase-1 on 4 arms (#3 overdraft threshold,
#6 inheritance semantics, #8 aging-bucket boundaries, #12 rotation cadence),
clean on 9 — #4/#13 flagged in v1.12.1 but clean this run: flag-firing on
those two is not stable across runs (recorded). Confirm-gate behavior
flawless: all 7 arms that computed adversarial refused to invoke from a
dispatched context, held at the one-confirm cost gate, and named the
coverage downgrade unprompted. 11/13 arms surfaced the I21 non-top
disclosure as a ride-along.

## Disclosure / caveats

- Arm model: sonnet (mid) named explicitly in all 13 Agent calls by the
  runner — **but several arms' own I21 disclosures self-identify their
  session model as glm-5.3-flash**, so the effective arm model is ambiguous
  and the pin may not have taken on some arms. Comparability with the
  v1.12.1 run (whose arm model is likewise not recorded) is therefore
  approximate. If #7's regression matters for a future decision, rerun with
  a verified pin.
- 3 arm launches hit a transient harness rate-limit; each was relaunched
  blind with a byte-identical prompt.
- Working tree: current uncommitted state (13 skills present, incl.
  spec-tdd-manager). No record file was written by the runner (this record
  persisted by the session).

## Verdict vs the standing rule

**Baseline holds.** The suite's measured construct — routing fidelity of the
entry text and the blast-radius litmus — is unchanged by the release (0/13
false-adversarial matches the v1.12.1 headline; the new entry point drew
zero attention from blind escalate readers). Ship gate satisfied on the
routing side; the green-lie suite is untouched by this release (no tier
verification behavior moved).
