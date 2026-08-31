# Fintech routing fixtures

Regression suite for the v1.12.0 routing litmus (blast radius, not domain adjacency), grounded in a real treasury/dealing codebase (DTMS Core: netting, cashflow, cashposition, cashtransfer, fundallocation, fxdeal, fxwatchlist, reconciliation, statement, liquidity, eligibility, STP, auth).

**Method:** each fixture is routed independently by a fresh subagent playing `spec-tdd-escalate` (reads the skill text from the working tree, blind to the answer key). Fixture = a settled one-line requirement, as a locked plan would state it.

**Answer key per the v1.12.0 litmus:** adversarial ⇔ a silent wrong result MOVES money / CHANGES authorization / IRREVERSIBLY corrupts data. Money-adjacent (reads/displays/reports the money system) → coverage or base. Pre-settlement safety nets drop a tier.

| # | Fixture (abbreviated) | Domain (DTMS) | Expected | Why |
|---|---|---|---|---|
| 1 | Multi-currency net-amount calculation: net per pair per day, post ONE net entry replacing N deals | netamount/booking | **adversarial** | posted entries; wrong netting books wrong amounts |
| 2 | Partial fund allocation against multiple open positions; conservation must hold; atomic rollback | fundallocation | **adversarial** | money movement itself |
| 3 | Inter-account cash transfer, same-day value dating, overdraft guard, atomic reversal | cashtransfer | **adversarial** | money movement itself |
| 4 | Scheduled purge deleting completed transactions older than 7 years (retention compliance) | transaction | **adversarial** | irreversible DATA LOSS if criteria wrong — the litmus's data-destruction clause, disguised as housekeeping |
| 5 | Maker-checker approval for back-office role changes, enforced at service layer | auth | **adversarial** | changes authorization |
| 6 | Sub-affiliates inherit the parent counterparty's dealing limits | eligibility | **adversarial** | wrong inheritance = dealing beyond authorized limits |
| 7 | Intraday cash-position snapshot endpoint: balances per account per currency, read-only | cashposition | **coverage** | branchy aggregation; reads money, cannot corrupt it |
| 8 | Reconciliation stats dashboard: matched/unmatched/break-aging per source per day, read-only | reconciliation/statistics | **coverage** | read-only reporting; branchy |
| 9 | MT940-format statement export generated from existing statement records | statement | **coverage** | format/parsing branch surface; read-only generation |
| 10 | FX watchlist display: live indicative rates with stale-rate highlight after 30s | fxwatchlist | **base** (lite acceptable) | indicative, display-only, small surface |
| 11 | Back-office CRUD for bank currency cut-off times, with validation | bankcurrencyconfig | **base/coverage, NOT adversarial** | boundary probe: wrong config disrupts/blocks flow but does not itself move money; recoverable (fix config) |
| 12 | AES-256 encryption at rest for statement archives; keys in vault; re-encrypt on rotation | statement/storage | **coverage (litmus-strict)** | boundary probe: the litmus is corruption/loss-focused; broken encryption EXPOSES data, does not destroy it. Adversarial defensible under PCI paranoia — a split here is a finding about the litmus, not a routing failure |
| 13 | Payment-status change notifications via email/webhook, 3× backoff retry, content from existing events | notification | **base** (lite acceptable) | no money-state change; wrong content embarrassing, not corrupting |

Score: strict for #1–#9; acceptable-range for #10–#13 (boundary probes — the point is to observe, and to learn where the litmus's edges sit).

## Results — v1.12.1 run (13 fresh-subagent arms, blind, parallel, ~20k tokens each)

| # | Expected | Routed | Verdict |
|---|---|---|---|
| 1 netting | adversarial | adversarial | ✅ |
| 2 fund allocation | adversarial | adversarial | ✅ |
| 3 cash transfer | adversarial | adversarial | ✅ |
| 4 retention purge | adversarial | adversarial | ✅ — named the data-loss clause ("silently destroys financial data"), not fooled by the housekeeping framing |
| 5 maker-checker | adversarial | adversarial | ✅ — "privilege escalation… changes authorization" |
| 6 eligibility limits | adversarial | adversarial | ✅ — flagged the check-then-consume race unprompted |
| 7 cash position | coverage | coverage | ✅ — quoted the litmus verbatim |
| 8 recon dashboard | coverage | **base** | ❌ ±1 — judged "no parsing/state-machine surface"; the aging buckets + per-source×day grouping are moderately branchy. Wrong tier, harmless direction (cheap tier), no adversarial over-trigger |
| 9 MT940 export | coverage | coverage | ✅ — "the over-routing trap" named |
| 10 FX watchlist | base/lite | base | ✅ |
| 11 cut-off config | base/coverage | coverage | ✅ in range — found the DST/equality-boundary branches |
| 12 encryption | coverage (litmus-strict) | **adversarial** | ⚠ defensible split — its corruption reading is real: rotation retiring the old key too early makes archives unrecoverable (irreversible data loss), and "authorized read" is auth logic. A finding about the litmus's edge, not a routing failure |
| 13 notifications | base/lite | **coverage** | ❌ ±1 — correctly REFUSED adversarial ("cannot move money, change auth, or corrupt payment data"); leaned coverage on retry/backoff branches |

**Headline: 0/13 false-adversarial.** Every money-adjacent fixture was held out of the top tier with the litmus quoted; the 6 true-critical fixtures all landed adversarial. The v1.12.0 fix does its job. The residual wobble is base↔coverage boundary judgment (2 arms, ±1 tier, both cheap) — a far weaker error mode than the pre-1.12.0 collapse, and both defensible on branchiness grounds. Sniff worked on every arm: flagged unnumbered cadence (purge), priority criterion (allocation), backoff base/max (notifications), aging-bucket boundaries (dashboard); clean docs routed silently.

**Litmus edge learned from #12:** "irreversibly corrupts data" legitimately reaches key-rotation data-loss, not just row deletion — confidentiality-only surfaces (broken encryption with intact data) stay at coverage, but any irreversible-loss angle in the unit pulls it up.
