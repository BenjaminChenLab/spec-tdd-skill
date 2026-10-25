# Fintech routing suite — v1.33.0 rerun

Standing-rule rerun for v1.33.0 (routing text touched: the spec-tdd-manager description's S5 list drops `spec-tdd-task-loop eco`; every tier skill's and task-dag's description byte-identical; no When-Use/When-NOT predicate moved anywhere). 13 fresh blind general-purpose arms, each playing spec-tdd-escalate against the working tree (escalate + PROTOCOL + the four tier SKILL.mds), scored against the answer key in [fintech-routing.md](../fixtures/fintech-routing.md).

## Results

| # | Fixture | Expected | Routed | Verdict |
|---|---|---|---|---|
| 1 | netting | adversarial | adversarial | ✅ — "posts ONE wrong net entry replacing N real deals"; invoked the adversarial cost-gate convention unprompted |
| 2 | fund allocation | adversarial | adversarial | ✅ — all three blast-radius arms quoted |
| 3 | cash transfer | adversarial | adversarial | ✅ — money-movement itself, no safety-net downgrade |
| 4 | retention purge | adversarial | adversarial | ✅ — named data-destruction, not fooled by the housekeeping framing |
| 5 | maker-checker | adversarial | adversarial | ✅ — "the dual-control here IS the feature, not a pre-existing safety net" |
| 6 | eligibility limits | adversarial | adversarial | ✅ — changes-authorization reading |
| 7 | cash position | coverage | base | ❌ ±1 cheap — "clean single-unit… no coverage-evidence signal"; the same wobble the v1.27.0 rerun observed on this fixture |
| 8 | recon dashboard | coverage | coverage | ✅ — aging-bucket + day-boundary branches named (the v1.12.1 baseline wobbled this one to base; this arm held it) |
| 9 | MT940 export | coverage | coverage | ✅ — "the over-routing trap" named |
| 10 | FX watchlist | base (lite ok) | coverage | ❌ ±1 up — leaned coverage on the fresh→stale transition state surface; cheap-tier family, no adversarial over-trigger |
| 11 | cut-off config | base/coverage | coverage | ✅ in range — validation boundary branches named |
| 12 | encryption | coverage (litmus-strict) | adversarial | ⚠ defensible split — rotation retiring the old key early = irreversible archive loss; identical to the v1.12.1 baseline result; a finding about the litmus's edge, not a routing failure |
| 13 | notifications | base (lite ok) | coverage | ❌ ±1 up — leaned coverage on the retry state machine + dual-channel branches; identical to the v1.12.1 baseline result |

**Headline: 0/13 false-adversarial. 6/6 true-critical hold adversarial.** Every money-adjacent fixture stayed out of the top tier with the litmus quoted (#12 — the key's own acknowledged edge — is the sole top-tier money-adjacent route and is baseline-equal). The wobble set (#7 down, #10/#13 up — all ±1, boundary probes) matches the recorded base↔coverage boundary behavior of prior runs.

## Verdict

Baseline holds — the v1.33.0 routing-text change (the manager's driver list) contaminated no tier routing. The standing rule's precondition for shipping is satisfied.

## Operational disclosure (the run's noise, recorded honestly)

- **The shared token pool drained live mid-suite**: 4 arms died on 429 (rate_limit, glm-5.3) and were re-dispatched — the maintainer's shared-quota stance observed from inside the suite.
- **Spawn variance**: 3 dispatches landed in runtimes without any local-file-read tool (no Read, no Bash); those arms STOPPED per the prompt's fallback rule instead of routing from memory. One earlier fixture-5 arm that routed from prior knowledge was discarded on exactly that ground and replaced by a file-reading arm.
- **Corrected mid-run at the maintainer's instruction**: some arms initially reached for Playwright/browser tools to read local files; the TOOL RULE (Read tool first, Bash `cat` fallback, no browser) was added to all subsequent prompts and pushed to in-flight arms. Codified post-run as a standing global rule in the maintainer's CLAUDE.md.
- **Handback flakiness**: several arms completed without delivering (one delivered literally "X"); recovered via SendMessage wakes (successful on fixtures 2/4/8) and fresh re-dispatches where wakes failed. Arm attempt counts: fixture 1 ×3, 5 ×2 (one discarded), 8 ×3, 13 ×3 — disclosed against the family's 2-redispatch norm, justified by the suite's need for a complete 13.
- Arm class: general-purpose subagents (glm-5.3-class), ~18–75k tokens each.
