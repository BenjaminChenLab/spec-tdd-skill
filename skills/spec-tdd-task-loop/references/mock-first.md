# Mock-first contract development — spec-tdd-task-loop (progressive reference)

Part of `spec-tdd-task-loop` (v1.36.0 progressive split — the SKILL.md's flow pointers load this file on demand). **Read it when upstream dependencies (external API, another team's service) are unreleased / unsettled and the phase must develop against a mock.** A settled-upstream phase never reads it.

---

## Mock-first contract development (the time dimension of tier choice)

When upstream dependencies are unreleased / unsettled:

1. **The first task builds the mock** (mock controller / server), fixing the contract; all subsequent tasks develop against the mock instead of idling in wait.
2. **The tier may drop during the mock-first phase (user's call).** Over-investing in verification for code against a mock before the contract settles is waste — when the contract changes, the deep tests get rewritten with it. Tiers are chosen not only by blast radius (the space dimension) but also by **this code's life stage** (the time dimension).
3. **Once the real dependency settles, schedule a contract-alignment task** — go back and compare real API vs mock contract, fix deviations, and pay back the deep tests deferred during the mock phase. A downgrade must be "defer + pay back", never "skip"; disclosed throughout.
4. **External open questions get a landing spot in the plan doc (kept distinct from the decisions section).** The decisions section records user rulings; questions awaiting third-party answers (upstream API behavior, another team's reply) get their own section **inside the authoritative plan doc** (living in scratch / conversation = did not happen), one line each: **question + the interim landing (which task uses what stopgap, where the single replacement point is) + where the answer converges when it arrives**. **Answer arrives → write back to the decisions section (numbering continued, source noted as external), strike the line as converged**, and the contract-alignment task digests it — the arriving answer has a definite convergence point and is not lost, and the alignment task has a ready-made digestion list (field record: STP2's G list — "real error-code values undecided → W6's classifier single-replacement point already built; when the answer arrives, change one place").
