# v1.31.0 design — manager discussed-entry fast lane, going-dark Gate 2 pre-approval, tier map

Date: 2026-10-13. Status: **FINAL** — audit round 1 (agree, 7 amendments folded) + targeted round 2 (agree, 7 wording amendments folded; the one-re-audit bound is spent). Awaiting the maintainer's explicit edit go; no skill file touched yet. Scope: `spec-tdd-manager` (items 1–3), the drivers (item 5), the whole family (item 4).

## Maintainer rulings (this session, all recorded)

1. **Fast-lane trigger = "content equals the conversation," not a magic phrase.** Entering manager after the requirement was fully discussed in conversation; the formalized spec doc is a transcription. The maintainer never reads generated docs (global rule), so a bulk re-approval stop on a transcribed spec is ceremony. Machine-checked: grounding + the materiality scan still run; any dimension the conversation left undecided surfaces via the lane's residual ONE ask (never silently defaulted). **Consent source (per audit, round 1): the entry shape is the consent** — the family's first token-less deviation; the qualifier text names this explicitly.
2. **Unclean audit still stops exactly once.** Audit amendments (attributed) ride Gate 2's presentation; one approval covers spec direction + final plan + route.
3. **Going-dark Gate 2 pre-approval is conditional.** Valid only when: the audit closes "agreed, no amendments" AND no user-owned findings are pending AND every IRREVERSIBLE-tagged decision was named-confirmed inside the same batched ask. Any miss → the pipeline waits for the return. Per-absence only, never carries over; default is hold-until-return.
4. **Tier map: TOP = opus-class.** The top workhorse tier (opus-class) IS "top tier" for every I19 pin and every I21 check; the flagship-experimental tier above it (fable-class) is never required for any pin. Ruling folded into skill text in this same release.
5. **Pre-approval delivery extends to task-loop and task-dag** (ruling on round 1's A3, 2026-10-13): the going-dark batched ask pre-rules the drivers' entry asks; the rulings ride the S5 hand-off; each driver gains a one-line entry clause honoring them (item 5).

## Item 1 — discussed-entry fast lane (manager)

**Problem.** A settled-doc entry already skips Gate 1 today (S1 sniff clean → grill skipped, no Gate 1). A conversational entry where everything was discussed still routes through grill Phase 1, whose spec gate IS Gate 1 — a rubber-stamp stop for a maintainer who never reads the doc it presents.

**Change (manager `SKILL.md` only; grill's own file untouched — standalone grill runs unchanged):**

- **S1 gains the lane, formalize-first.** Trigger: conversational entry + the material dimensions **anchored to I11's materiality canon by name (observable behavior, state transitions, failure semantics, data integrity, security/authorization, compatibility, explicit NFRs — per audit round 2; the draft's own list had dropped three)** all settled in the discussion. **Order (per audit round 1 — the compaction mitigation): formalize the spec doc from the discussion FIRST, then the materiality scan reads the doc (durable) plus the conversation (I17's spirit).** Grounding still runs.
- **The lane ADDS the residual-ask shape on the conversational path** (per audit round 1 — no such ask exists there today; the ONE-ask shape lives on the settled-doc sniff only). Open dimensions → ONE ask, recommendations attached. **An IRREVERSIBLE-tagged decision not explicitly settled in-conversation gets its named confirmation in that same ask, and — stated in the lane text itself, not by reference — an unanswered IRREVERSIBLE still parks; a bulk "all defaults" reply does not cover it.** Converged with nothing open → **no standalone Gate 1 stop**.
- **The direction approval rides Gate 2** — one stop total, clean or unclean (amendments shown at Gate 2 as today; substantive changes keep the ONE targeted re-audit bound).
- **The Gate 1 audit-preview line** ("Audit: 2nd / 3rd, reason: IRREVERSIBLE tag") moves to the lane's entry announcement (one line, veto right stands).
- **S0 resume marker.** The spec doc gains a lane stamp line ("fast lane declared (YYYY-MM-DD): direction approval rides Gate 2"). Gate 2's pass stamp notes it covered Gate 1's direction approval. **Known lane cost (per audit round 1): session death between discussion and the stamp → the conversation never existed → full re-grill (I17 as-is); recorded, not fixed.**
- **The stamp-reader line (per audit round 2 — blocking; closes a pre-existing hole):** S0's trio-present branch and Gate 2's letters gain — "a Gate 2 stamp on file (attended approval, or the going-dark pre-approval record) → Gate 2 is not re-presented; S5 has fired or fires now." Covers both stamp kinds; today's text reads no stamp at all.
- **Condition sweep of manager's own two-gate text (per audit round 1).** Every two-gate/Gate-1 site gains the lane's conditional or qualifier: REQUIRED BACKGROUND's "adds no new invariant and relaxes none" (consent source named per ruling 1), the Overview strip, pillar 4's "Zero new deviations … PROTOCOL untouched, the existing twelve untouched" (release-scoped qualifier), the ask ledger (the lane's merged stop; the going-dark pre-answer exception), the S5 row "this skill never pre-answers" (the going-dark exception), the non-delegable list (the lane's conversation + merged direction approval stay session-side), the Common-Mistakes "gate = Gate 1" row. Compensations: in-conversation settlement of every decision + the residual ask + the S4 independent audit + Gate 2's full presentation.

## Item 2 — going-dark promoted to pipeline level (manager)

The going-dark bullet currently lives in the `longrun` section only, triggered by "delegated dispatch in flight." Promoted to a manager-level rule (with or without the flag; the S4 auditor dispatch exists in both modes): trigger = the user announces leaving/sleeping/offline at ANY pipeline point, including a declared overnight run at entry. The longrun-specific dialect (runner's ONE fresh re-dispatch, drafter bounce loop) stays in the longrun section, referencing the pipeline rule. A going-dark before the grill conversation has settled the decisions → grill's own "no human reachable → park at the gate" letter governs; the lane does not apply.

## Item 3 — conditional Gate 2 pre-approval (manager + GOING-DARK.md)

- Manager's going-dark dialect gains the pre-approval item: the three conditions of ruling 3; granted + conditions hold at audit close → S5 fires unattended. **The going-dark batched ask pre-rules the S5 target's own entry asks as open-decision items (per ruling 5 + round 2's completions, item 5): loop's commit authorization; dag's time-band mode — the auto-band choice only, with the peak/off-peak bands themselves riding the hand-off (dag's letter: "the bands are your quota experience; the skill presets nothing"); per-wave mode barred as an unattended pre-rule (it asks at every wave boundary, unanswerable while away); and the session's I21 tier-check answer (a carried decline pre-answers the driver's check — without it, a non-top session + granted pre-approval stalls at driver entry unattended, and the attended known-friction at manager's ask ledger closes too).**
- **Condition-verification actor (per audit round 1): the session** (S5 is non-delegable). Under `longrun`, the runner's RETURN — close stamp + user-owned findings verbatim (I12) — is the input the session verifies the three conditions against, then fires S5 itself.
- The v1.30.1 hard line is amended: "the gates themselves never run unattended — user-owned, they wait for the return" gains "the sole exception: a Gate 2 pre-approval explicitly granted at the going-dark gate under its three conditions."
- **The unattended pass record (per audit round 1's (f) gap, worded per round 2):** at S5 fire the session writes into the plan doc: "Gate 2 pre-approved (going-dark gate YYYY-MM-DD; conditions verified YYYY-MM-DD): route = <choice>" — plus, when the lane stamp is on file, "covers Gate 1's direction approval" (per audit round 2 — the two folds now agree). Read at resume by item 1's stamp-reader line.
- GOING-DARK.md: the `For:` line adds `spec-tdd-manager`; the dialect-mapping paragraph gains one clause (under manager, "the board" = the plan trio / spec doc; the gates' pre-approval shape lives in manager's own text). **Nothing else in the shared file changes (per audit round 2 — the earlier "Return re-arm gains a manager clause" draft sentence is deleted; the existing dialect mapping already redirects "the board" for the re-arm).**

## Item 4 — tier map, family-wide (ruling 4)

- `PROTOCOL.md` I19(a): "harness-relative: top = the strongest model" → "harness-relative: top = the top workhorse tier (opus-class as of this writing; a stronger flagship-experimental tier above it — fable-class — exists but is never required for a pin), mid = the strong-but-cheaper tier". I21 gains the same map and the same branch fix **in its own wording (its tail "silent, zero interaction" keeps its phrasing — no copy of the 10-file sentence, per audit round 2)**.
- **The tier-check sentence — exactly 10 SKILL.md files** (adversarial-grill, grill, escalate, 2nd-opinion, lite, spec-tdd, coverage, adversarial, task-loop, manager — per audit rounds 1+2 census; 3rd-opinion inherits 2nd-opinion's flow incl. the I21 pre-flight — map reaches it by inheritance, no edit; supervisor retires the ask and carries no sentence — its TOP final-audit pin is reached via PROTOCOL's I19(a), no edit; quickfix has no tier check). `spec-tdd-quickfix` untouched.
- **The branch fix, merged (per audit round 2 — replacing the fallback branch would open the mirror hole: a harness where the opus-class top is unavailable would ask the strongest-available session an unanswerable upgrade): "**Top tier — or any tier above it — in use, or no higher tier exists → silent, move on.**"**

## Item 5 — driver delivery clauses (task-loop + task-dag; per ruling 5)

Each driver gains ONE entry clause at its pre-flight ask site:

- task-loop (at Pre-flight 2, the commit-authorization ask): "Entry arrived with pre-ruled unattended rulings aboard (a manager going-dark gate's batched rulings carried on the `<phase>` hand-off) → the asks they cover are treated as answered, never re-asked; the board's status section discloses which asks were pre-ruled and by which gate (its opening rows gain this disclosure — a new slot, per audit round 2's note). Those rulings cover THIS absence only (per-window, GOING-DARK item 1's non-carryover shape). The carried I21 decline pre-answers Pre-flight 1."
- task-dag (at its mode ask): the same shape covering the time-band mode ask **(auto-band only, bands riding the hand-off; per-wave barred) — and stating that task-loop's amended Pre-flight 2 reaches dag via its REQUIRED BASE ("every rule there applies unchanged"), per audit round 2**; dag's existing authorization-coupling degradation (no top-commit authorization → parallel unavailable, auto-serial) needs no precedence text — it already rules the inconsistent-pre-rule case.
- supervisor needs nothing (no entry asks; structurally no-commit close).

## Docs sync

README: version header 1.30.1 → 1.31.0; manager row; tier-map note; **the six two-stop claims reworded** (per audit round 1 — "you show up exactly twice" / the pipeline diagram's two approval marks / "holds the two human gates" / the decision tree's "only at the two gates" / "only two checkpoints") → the new promise: at most twice; once on a discussed entry; zero while away under a granted pre-approval (with the I21-carry fix of item 5, this holds on any session tier). CHANGELOG: entry + standing-rule note carrying **two judgments** (routing-inert for items 1–3 + 5 — frontmatter byte-identical; tier-definition-inert for item 4 — codifies practice already recorded in the field docs, and the merged-branch fix prevents any silent→ask behavior flip in either direction) + an **explicit supersession line** for v1.30.1's "gates never run unattended" record. **CHANGELOG history lines quoting the old tier sentence stay untouched (append-only).** Install-copy sync applies to GOING-DARK.md/PROTOCOL.md as in v1.30.0.

## Out of scope (recorded, not built)

- Standalone spec-2nd/3rd-opinion runs keep their own gate discipline (no fast lane there).
- No change to grill/adversarial-grill standalone behavior; no new skill; no rename.
- IRREVERSIBLE → 3rd-opinion auto-upgrade logic unchanged (only the preview's presentation point moves on the lane).
- The compaction risk is mitigated (formalize-first), not eliminated — the lane's trigger judgment still depends on the surviving conversation; recorded as a standing knob.

## Pending user decisions

None — five rulings settled in session (2026-10-13), the last (ruling 5) mid-audit.

## Audit trail

**Round 1 (2026-10-13, spec-2nd-opinion, opus read-only): agree with the plan as a whole, seven required amendments — all adopted verbatim** (count 10 + inheritance → item 4; fable-branch + two standing-rule judgments → item 4 + Docs sync; A3 delivery gap → ruling 5 + item 5; manager's unnamed two-gate sites → item 1's sweep; README six claims → Docs sync; IRREVERSIBLE-parks restatement + "existing ask" correction → item 1; death-before-stamp + verification actor → items 1, 3) **plus two missed risks folded** ((e) compaction → formalize-first; (f) unattended pass record → item 3).
**Round 2 (targeted, fresh opus, scoped to the round-2 folds): agree — every mechanism holds against the actual files; seven wording amendments, all folded** (stamp-reader landing sentence + both stamps covered → item 1; GOING-DARK edit-scope contradiction resolved (dialect-mapping only) → item 3; dag mode completeness (bands ride, per-wave barred, REQUIRED-BASE inheritance) → items 3, 5; I21 carried-decline pre-answer → items 3, 5; merged fallback branch + I21 tail keeps its wording → item 4; lane dimension list anchored to I11 → item 1; stamp/lane Gate-1 note aligned → item 3). **The one-re-audit bound is spent; round 2's fixes ride the auditors' own drafted directions.**
