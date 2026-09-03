# Green-lie fixtures — wrong-but-GREEN benchmark

Measures the family's **headline claim directly**: how often does an arm deliver a state that is *GREEN on its own test suite* but *wrong against a hidden oracle* (the requirement's intended behavior)? This is the wrong-but-GREEN rate — not routing (that's [`fintech-routing.md`](fintech-routing.md)), not process compliance.

Companion baseline record: [`docs/specs/2026-09-03-green-lie-baseline.md`](../specs/2026-09-03-green-lie-baseline.md).

## Method

Each fixture is a settled small-unit requirement with a **seeded trap**: a wording that tempts a wrong reading, or a stated-but-subtle behavior that shallow tests skip. Each fixture runs in two **blind arms**, same model (no model pin — both arms inherit the session model; fairness over tier fidelity):

- **Arm A — same-context TDD (control).** ONE fresh subagent gets the requirement, is told to practice TDD (write the test first, then implement to green). This is the ecosystem-standard agentic TDD: the best case for one context.
- **Arm B — spec-tdd base tier (treatment).** The real causal structure, executed as staged blind dispatches standing in for the skill's roles: **B1** test-author (orchestrator Phase 1: writes ONLY the black-box acceptance test, proves RED against a `NotImplementedError` stub), **B0** independent encoding audit of that test (read-only; findings relayed to B1 once — one strengthening round max), **B2** implementer (the test is a read-only contract; may not edit it; reports ERR instead). Verification is the harness re-running the acceptance test — never the arm's self-report.

Both arms see the **identical** requirement file and identical constraints. Arms never see the answer key, the oracle, or each other.

**Run tree:** `docs/fixtures/green-lie-runs/` → `reqs/GL-XX.md` (the verbatim public requirement, one file per fixture, referenced by both arms — **committed**, so the exact bytes arms saw are traceable), `A/GL-XX/`, `B/GL-XX/` (arms' code, gitignored). **Oracles are committed and pre-registered**: [`docs/fixtures/oracle/green-lie/`](oracle/green-lie/) — one runner per fixture, materialized before any dispatch, executed as `python GL-XX_oracle.py <arm_dir>`.

**Scoring (after arms land, mechanical):**

1. Re-run the arm's own suite → `GREEN?`
2. Run the hidden oracle → `ORACLE?`
3. Compare the arm's own test against the fixture's clause checklist → clauses asserted / total (`WEAKENED` when clauses are missing despite GREEN + oracle-pass).
4. **Wrong-but-GREEN := GREEN ∧ ¬ORACLE.** A delivered-but-erroring own-suite is broken (counted, not wrong-but-GREEN); a B2 ERR-stop or an empty/crashed dispatch is `N/A` (infra), never counted.

**Disclosed deviations from the live skill:** B1 is a subagent playing the orchestrator (the live skill authors the test in your session — same stand-in method as the routing suite); the grill/gate front-ends are out of scope (requirements arrive settled); tiers above base (coverage/adversarial) are not compared here — a follow-up arm. **Disclosed limits:** single maintainer; single base model in both arms (context separation ≠ model diversity); N=12; traps authored by the skill's maintainer (authorship bias favors the skill's mechanisms — read with that in mind); arms run with repo access (B1 must read `skills/spec-tdd/SKILL.md` from the working tree), so blinding rests on the explicit containment instruction, same residual risk the routing suite accepted.

## Pre-registered predictions (written before any arm ran)

- **H1 (headline):** arm A wrong-but-GREEN lands 3–6 / 12; arm B lands 0–2 / 12.
- **H2 (by trap class):** boundary traps (GL-01, GL-05, GL-10) catch A hardest — one context writes test and impl agreeing on the same misread. Stated-but-subtle traps (GL-02, GL-09, GL-11) show up as A-weakness (happy-path tests) more than misreads.
- **H3 (B's own risk):** where the requirement wording is genuinely ambiguous, B1 can misread it like anyone — if B fails, predicted at GL-01/GL-05 (boundary semantics); B0's audit catches clause *drops*, not mis*readings* (the audit reads the same requirement, so a shared misread survives it).
- **H4 (weakening):** A's suites assert fewer clauses than B's (B0 explicitly hunts clause drops).

## Fixtures

Legend — **Req** is the verbatim public requirement (what arms see, plus the shared constraints block below). **Key** is the answer: the trap, the correct reading, and the clause checklist the oracle and weakening-judgment use. **Trap class**: `boundary` (inclusive/exclusive misread) · `subtle` (stated but easy to under-assert) · `fail-closed` (default-deny / integrity).

Shared constraints block (appended to every `req.md`): *Python 3.7-compatible, standard library only. Deliver `<MODULE>.py` and `test_<MODULE>.py`; the test file must run with `python test_<MODULE>.py` (plain asserts + a `__main__` runner, no pytest).*

---

### GL-01 retention purge boundary · `boundary`

**Req.** Implement `should_purge(record_date, as_of_date) -> bool` in `retention.py` (args are `datetime.date`). Retention policy: completed transaction records must be **kept AT LEAST 7 full calendar years**, then purged. Return `True` only when the record is *strictly older* than 7 calendar years as of `as_of_date`.

**Key.** Trap: `>=` at the boundary — purging a record on its exact 7-year anniversary violates "kept at least". Exactly-7 → `False` (keep); one day past → `True`. Clauses: ① exactly-7 keeps, ② strictly-older purges, ③ younger keeps.

### GL-02 money split conservation · `subtle`

**Req.** Implement `split_amount(total_cents, n) -> list[int]` in `split.py`. Split a monetary total (integer cents) into `n` integer-cent shares: no share off by more than 1 cent from the exact mathematical share; **shares must sum exactly to `total_cents` (conservation is mandatory)**; when fractional remainders tie, the extra cent goes to the earliest share.

**Key.** Trap: rounding each share independently → sum drifts (100 cents / 6 → six 17s = 102). Correct: largest-remainder, tie → lowest index (100/6 → `[17,17,17,17,16,16]`). Clauses: ① conservation (sum exact), ② per-share within 1 cent, ③ tie → earliest, ④ `n=1` identity.

### GL-03 idempotent batch dedupe · `subtle`

**Req.** Implement `process_batch(entries) -> dict` in `batch.py`. `entries` is a list of `(request_id, amount_cents)` tuples; the same `request_id` may appear more than once due to at-least-once delivery and **must be applied exactly once — first occurrence wins**. Return `{'applied': sum of applied amounts, 'count': unique ids applied, 'duplicates_ignored': dropped repeat occurrences}`.

**Key.** Trap: summing all occurrences → double-applied money. Clauses: ① first-occurrence-wins dedupe (incl. differing repeat amounts), ② `applied` = unique-only sum, ③ `duplicates_ignored` correct, ④ empty batch → zeros.

### GL-04 authorization fail-closed · `fail-closed`

**Req.** Implement `check_access(user, resource, grants) -> bool` in `access.py` (`grants` = iterable of `(user, resource)` pairs). Access is allowed **ONLY** when the exact pair is present in `grants`. Any lookup that does not match a grant — unknown users, **unknown/unregistered resources**, missing entries — must **DENY**. The system must fail closed.

**Key.** Trap: treating a resource that appears nowhere in `grants` as "unrestricted" → `True`. Clauses: ① explicit grant allows, ② unknown user denies, ③ known-user wrong-resource denies, ④ unknown resource denies, ⑤ empty grants denies.

### GL-05 interval overlap, half-open · `boundary`

**Req.** Implement `overlaps(a_start, a_end, b_start, b_end) -> bool` in `intervals.py` (ints = epoch seconds). Intervals are half-open `[start, end)`. Two intervals overlap **only when they share a strictly positive duration** — back-to-back intervals (one ending exactly when the next starts) do **not** overlap.

**Key.** Trap: `<=` comparisons → touching counts as overlap. Clauses: ① touching (either direction) → `False`, ② strict overlap → `True`, ③ zero-length interval never overlaps, ④ identical intervals → `True`.

### GL-06 month arithmetic clamp · `subtle`

**Req.** Implement `add_months(date_str, months) -> str` (ISO `YYYY-MM-DD` in/out) in `monthmath.py`. Add calendar months; when the target month has no such day, **clamp to the last day of that month** (Jan 31 + 1 → Feb 28 non-leap, Feb 29 leap). `months >= 0`; `0` → same date; year carry works (Jan 2026 + 13 → Feb 2027).

**Key.** Trap: day overflow (Mar 2/3) or raising on clamp-day. Clauses: ① non-leap clamp, ② leap-year clamp gives Feb 29, ③ year carry, ④ zero identity, ⑤ leap-day anniversary clamps (2024-02-29 + 12m → 2025-02-28).

### GL-07 counterparty name normalization · `subtle`

**Req.** Implement `same_counterparty(name_a, name_b) -> bool` in `match.py`. Reference-data matching is case-insensitive and whitespace-lenient but **PUNCTUATION-SENSITIVE**: trim outer whitespace, collapse internal whitespace runs to one space, compare case-insensitively — **nothing else**. Names differing only in punctuation (`'ACME Corp.'` vs `'ACME Corp'`) are **different** counterparties.

**Key.** Trap: aggressive normalization (stripping punctuation) → false counterparty merge. Clauses: ① case-insensitive, ② whitespace collapse (incl. trim), ③ punctuation significant, ④ exact-equal matches.

### GL-08 netting sign conservation · `subtle`

**Req.** Implement `net_amount(deals) -> int` in `netting.py`. `deals` = list of `(side, amount_cents)`, side `'BUY'` contributes **positive** and `'SELL'` contributes **negative** to the net position. Return the **signed** net (BUY 100 + SELL 30 → +70). The net is the algebraic sum — **never an absolute value**.

**Key.** Trap: magnitude-summing or sign flip. Clauses: ① BUY positive, ② SELL negative, ③ negative net stays negative, ④ empty → 0.

### GL-09 capped allocation with remainder · `subtle`

**Req.** Implement `allocate(amount_cents, caps) -> (list[int], int)` in `allocate.py` (`caps` = list of per-slot caps, filled in order). Never exceed a cap; never exceed the requested amount; return the **unallocated remainder** as the second element. A **negative amount is invalid: raise `ValueError`** and allocate nothing. Empty or all-zero caps with a positive amount → allocate nothing, remainder = full amount.

**Key.** Trap: dropping the remainder (lost funds) or "processing" a negative amount as a refund. Clauses: ① in-order fill respects caps, ② remainder returned, ③ negative → `ValueError` atomically, ④ empty caps → `([], amount)`; zero caps → zero-filled per-slot list, full remainder (one output per slot — the req pins "per-slot caps, filled in order"; oracle amended at self-test, pre-dispatch).

### GL-10 staleness guard boundary · `boundary`

**Req.** Implement `is_rate_usable(rate_ts_s, now_s) -> bool` in `stale.py` (ints, epoch seconds). A rate is usable only while **fresher than a 30-second staleness window**: usable iff `(now_s - rate_ts_s) < 30`. At **exactly 30 seconds** elapsed the rate is stale (`False`). Future timestamps (`now_s < rate_ts_s`) are not usable either.

**Key.** Trap: `<= 30` usable, or `abs()` accepting future. Clauses: ① diff < 30 usable, ② diff == 30 stale, ③ diff > 30 stale, ④ future invalid, ⑤ diff == 0 usable.

### GL-11 retry backoff schedule · `subtle`

**Req.** Implement `retry_delays(base_s, max_s, retries) -> list` in `backoff.py`. The delay **before retry k** (k = 1..retries) is `base_s * 2**(k-1)`, **capped at `max_s`** (base 2, cap 5, 3 retries → `[2.0, 4.0, 5.0]` — the third would be 8 but is capped). `retries = 0` → `[]`.

**Key.** Trap: exponent off-by-one (`2**k` → first delay 2×base) or cap forgotten. Clauses: ① first delay = base, ② doubling, ③ cap applied (incl. repeated capping), ④ `retries=0` empty.

### GL-12 maker-checker, no self-approval · `fail-closed`

**Req.** Implement `can_approve(maker_user, checker_user, change) -> bool` in `makercheck.py`. A change may be approved only by a user **different from its maker** — the maker can **never** approve their own change, **with no exceptions for any role** (an administrator who is also the maker is still blocked). `change` is opaque (ignored). Usernames are case-sensitive (`'Alice'` ≠ `'alice'`).

**Key.** Trap: inventing an admin bypass (e.g. treating the user string `'admin'` specially) or case-folding usernames. Clauses: ① different users allow, ② same user denies, ③ `'admin'`-as-both still denies, ④ case-sensitive comparison.

---

## Runbook (verbatim arm prompts)

`<DIR>` = the arm's run dir; `<REQFILE>` = `docs/fixtures/green-lie-runs/reqs/GL-XX.md`; `<MODULE>` per fixture. All four templates are used verbatim; the only per-fixture variance is dir and module name. Every template carries the same **containment line** (blinding): reports capped at 12 lines (token economy).

**A (control):**

```text
Work in: <DIR>. Containment: the ONLY file outside <DIR> you may read is
<REQFILE>. Do not read or search anything else in this repository.

This is a small, self-contained Python module task. The requirement is in
<REQFILE> — read it first and treat it as the locked plan. Constraints are
stated in the requirement file.

Practice TDD: write test_<MODULE>.py FIRST from the requirement, run it to
see it fail, then implement <MODULE>.py until all tests pass. You may
iterate freely between the requirement and your code.

When done, all tests must pass via `python test_<MODULE>.py`. Report
(max 12 lines): files written, the exact command you ran, final test
output summary.
```

**B1 (test-author, plays the orchestrator's Phase 1):**

```text
Work in: <DIR>. Containment: the ONLY files outside <DIR> you may read are
<REQFILE> and E:/@sourceCode/spec-tdd-skill/skills/spec-tdd/SKILL.md.
Do not read or search anything else in this repository.

First read skills/spec-tdd/SKILL.md (the path above) — you are executing
its orchestrator phase (acceptance-test authoring) for ONE unit; no
implementer exists yet. Then read the requirement in <REQFILE> and treat
it as the locked plan. Constraints are stated in the requirement file.

Your job — write ONLY the acceptance test, black-box and behavioral,
derived from the REQUIREMENT text (no implementation exists):
1. Create <MODULE>.py containing ONLY the pinned API signatures, each body
   `raise NotImplementedError`.
2. Write test_<MODULE>.py covering the requirement's behaviors, boundaries,
   and edge policies as you read them.
3. Run `python test_<MODULE>.py` and confirm it FAILS (RED).

Do NOT implement any behavior. Report (max 12 lines): files written, the
RED evidence (failing summary line).
```

**B0 (independent encoding audit, read-only):**

```text
You are an independent encoding auditor. READ-ONLY: edit nothing.

Containment: the ONLY files you may read are <REQFILE>,
<DIR>/test_<MODULE>.py, and <DIR>/<MODULE>.py. Do not read or search
anything else in this repository.

The requirement (locked plan) is in <REQFILE>. Another agent wrote the
acceptance test from it: <DIR>/test_<MODULE>.py (+ stub <MODULE>.py).

Audit ONLY whether the test encodes the requirement:
- every behavior clause in the requirement is asserted somewhere with
  discriminating power (a wrong implementation would fail it);
- boundaries and edge policies the requirement pins are actually asserted;
- nothing is over-asserted beyond the requirement (no invented requirements).

Report (max 12 lines): verdict PASS, or a numbered list of concrete gaps
(clause → what is missing). No file edits.
```

**Strengthen relay (only if B0 reports gaps; sent to B1, one round max):**

```text
An independent audit found gaps in your acceptance test (same containment
as before). Fix test_<MODULE>.py ONLY (still no implementation; the stub
stays), re-run `python test_<MODULE>.py`, confirm it is still RED. Gaps:
<GAPS>
Report (max 8 lines): what you changed, RED re-confirmed.
```

**B2 (implementer, contract read-only):**

```text
Work in: <DIR>. Containment: the ONLY files outside <DIR> you may read are
<REQFILE>. Do not read or search anything else in this repository.

You are the implementer stage of a two-agent pipeline. Another agent wrote
the acceptance test from the requirement; it is your READ-ONLY contract.

The requirement is in <REQFILE>; the contract is <DIR>/test_<MODULE>.py
(run: `python test_<MODULE>.py`). Implement <DIR>/<MODULE>.py until the
acceptance test passes. You may NOT modify test_<MODULE>.py — if you
believe the test itself is wrong, STOP and report ERR with one line why,
instead of editing it. You may add your own extra unit tests in
test_<MODULE>_impl.py if you want.

Report (max 12 lines): final acceptance-test output summary, plus any ERR.
```

## Oracle (hidden from arms, committed before any dispatch)

One runner per fixture at `docs/fixtures/oracle/green-lie/GL-XX_oracle.py`, executed as `python GL-XX_oracle.py <arm_dir>`; prints one PASS/FAIL line per case plus a summary. The case tables are exactly the clause checklists above with concrete values — the runner loads `<arm_dir>/<MODULE>.py` fresh and compares against the key (GL-09's negative-amount case expects `ValueError`).

## Results — 2026-09-03 run (12 fixtures × 2 arms, 48 dispatches, ~1.2M subagent tokens)

**Headline: wrong-but-GREEN — arm A 0/12, arm B 0/12. No separation. H1 refuted at this difficulty and scale.**

| # | Fixture | Trap class | A own-suite | A oracle | B own-suite | B oracle |
|---|---|---|---|---|---|---|
| 01 | retention boundary | boundary | GREEN 10/10 | PASS 5/5 | GREEN 14+4 | PASS 5/5 |
| 02 | split conservation | subtle | GREEN 12/12 | PASS 5/5 | GREEN 3 (sweep-based) | PASS 5/5 |
| 03 | batch dedupe | subtle | GREEN 11/11 | PASS 5/5 | GREEN 14+2 props | PASS 5/5 |
| 04 | authz fail-closed | fail-closed | GREEN 10/10 | PASS 5/5 | GREEN 21/21 | PASS 5/5 |
| 05 | interval half-open | boundary | GREEN 17/17 | PASS 7/7 | GREEN 26+3 props | PASS 7/7 |
| 06 | month clamp | subtle | GREEN 10/10 | PASS 6/6 | GREEN 25/25 | PASS 6/6 |
| 07 | name normalization | subtle | GREEN 25/25 | PASS 5/5 | GREEN 46+3 props | PASS 5/5 |
| 08 | netting sign | subtle | GREEN 12/12 | PASS 5/5 | GREEN 10+2 props | PASS 5/5 |
| 09 | allocation remainder | subtle | GREEN 14/14 | PASS 5/5 | GREEN 15/15 | PASS 5/5 |
| 10 | staleness boundary | boundary | GREEN 7/7 | PASS 5/5 | GREEN 11/11 | PASS 5/5 |
| 11 | backoff schedule | subtle | GREEN 8/8 | PASS 5/5 | GREEN 10+1 prop | PASS 5/5 |
| 12 | maker-checker | fail-closed | GREEN 8/8 | PASS 5/5 | GREEN 15/15 | PASS 5/5 |

Every arm's own suite GREEN on the harness's own re-run (self-reports never trusted); every oracle PASS. A's suites genuinely assert the trap clauses (spot-checked, not just self-reported: anniversary-keeps, back-to-back non-overlap, unknown-resource deny, admin-as-both blocked, tie-to-earliest all present) — the null result is not under-testing in disguise.

**What did differ (qualitative, from dispatch reports):**

- **Test depth.** B's suites systematically deeper: property/oracle sweeps on 10/12 fixtures (permutation invariance, translation invariance, conservation grids, 10^15 magnitude checks) vs A's 2/12 (GL-02's invariant grid, GL-06's 816-case differential). RED-purity scans reported on 12/12 B1 dispatches (every failure must be `NotImplementedError`, not an import defect). B0 independent audits: 12/12 PASS, **zero strengthen relays needed**; B2 ERR stops: 0; circuit breakers: never engaged anywhere.
- **Disciplined interpretation disclosures (B).** B1s named silent interpretations ("whitespace = any whitespace char, not just space"; Feb-29 anniversary asserted only on the convention-free band) and refused to guess undecided contracts (no assertion for `n ≤ 0` rather than inventing an error contract). A self-caught its own wrong test expectations twice (GL-02, GL-06) — the free-iteration control does self-correct at this scale.
- **Cost.** A ≈ 20–32k tokens (1 dispatch); B ≈ 66–88k (B1+B0+B2) — roughly 3×. Correctness bought: none detectable on these fixtures.

**Run deviations (disclosed):** 3 dispatches died on API 429 and were re-dispatched identically (A/GL-04, A/GL-12, B1/GL-07). A/GL-04's test file survived its first (killed) dispatch; the retry verified it clause-by-clause against the req, kept it, and wrote the impl — two contexts touched that dir (flagged; does not mirror B's structure: no RED-first handoff discipline, no independent audit). B1 agents had no dispatch tool inside their containment, so the skill's encoding audit ran harness-side (B0) rather than from within B1 — pipeline independence preserved at the harness level; B1s disclosed their same-context fallback re-reads. GL-09's oracle was amended at self-test, pre-dispatch (zero-caps → per-slot reading).

**Reading the null result honestly** — why the traps didn't catch arm A: ① *scale* — single-function greenfield with a 5-line settled spec is cheap to close-read; attention doesn't thin. ② *trap salience* — the cue words are bolded in the reqs (AT LEAST, strictly, NEVER, mandatory) and the traps are classic seeded defects that TDD-trained models reflexively test; there is no domain camouflage (unlike the routing suite's purge-as-housekeeping). ③ *a strong control* — arm A got genuine test-first instructions and free iteration, and this model is heavily trained on exactly that loop. ④ *no pressure* — nothing pushed A to ship early; the circuit breaker never engaged.

**What this bounds:** on THIS model, small settled units with classic traps do not reproduce the green lie even single-context. The correlated-failure regime the family targets lives where this benchmark didn't go: longer specs where the trap is buried unbolded mid-paragraph, fuzzy requirements (the grill front-ends' actual beat), attention dilution across multi-unit batches, and repair-loop pressure. **v2 fixture design:** domain-camouflaged traps, unbolded cues, 1–2 page specs, a deliberately flaky-ish environment to engage repair pressure, and a `spec-tdd-adversarial` third arm.
