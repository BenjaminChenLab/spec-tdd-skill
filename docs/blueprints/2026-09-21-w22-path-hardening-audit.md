# 2026-09-21 — W22 silent-success absolute-path incident: the PHASE BOUNDARIES path hard rule (the plan under audit)

**Status**: implemented (2026-09-21) — user decisions: 1 = **change them all (class-level retirement, six files)**, 2 = **A (no phantom-tree detection added)**, 3 = **implementation authorized**; after completion, spawn a subagent audit; **both sides agree → commit (short) + tag v1.24.0 + release + push + local install** (the conditional release chain explicitly authorized by the user).

**Orchestrator tier disclosure**: this session runs a non-top model (`glm-5.3-flash`); the I21 ask was surfaced and the user answered **ignore** — recorded decline, listed in the final report's disclosures per the skill's rules.

---

## 1. Background (context and established facts, each with evidence)

### The incident (2026-09-18, dtms-core repo)

> Source of facts: another session's incident report. dtms-core is an external repo; this repo (spec-tdd-skill) cannot re-verify the scene — the auditor takes the facts as given and states "incident facts taken as given" in the report.

- The W22 re-test batch was dispatched by `spec-tdd-task-loop`; the level-1 implementation subagent's very first instruction hand-typed the repo root as `E:/sourceCode/...` (correct: `E:/@sourceCode` — the `@` was dropped).
- The instruction looked like: `mkdir -p "E:/sourceCode/.../.spec-tdd/W22" && date > ".../W22/HEARTBEAT"`.
- `mkdir -p` + output redirection make any path "silently succeed" → an entire parallel directory tree was materialized out of thin air, the HEARTBEAT written to the wrong location (a watchdog checking the correct path would see a stale heartbeat).
- The same instruction read `POLICY-W22.md` with `2>/dev/null`, getting an ABSENT false negative from the same wrong path (which happened to be the correct conclusion that time — the real path had no POLICY file to begin with).
- The rest of that batch's artifacts all landed at the correct paths; zero data loss.

### Root-cause finding (the proposing session's claim)

SKILL.md's heartbeat instruction was written in relative form but never banned the agent from composing absolute paths itself; "create the directory if missing" + `mkdir -p` materializes the typo'd path into reality.

### Current-state facts (established by the orchestrator's 2026-09-21 file reads; re-verified by the auditor)

- `skills/spec-tdd-task-loop/SKILL.md` L144–151: the PHASE BOUNDARIES block (inside the level-1 dispatch template); the heartbeat instruction = L146–147 "1) touch `.spec-tdd/<task>/HEARTBEAT` (create the directory if missing; touch or an equivalent write)…"; item 2 in the same block = the POLICY-<task>.md re-read.
- `skills/spec-tdd-supervisor/SKILL.md` L161–168: the same-shaped block, the `<unit>` version; heartbeat instruction = L163–164.
- Both blocks are currently in relative-path form, with no absolute-path ban wording anywhere.
- Adjacent doctrine (interacting with this fix, not its object): task-loop L73 and supervisor L57 both require that the dispatch prompt restore "doc path shorthands / the template's `{family root}` to **absolute paths** (the sub-agent's cwd cannot be relied on)"; both templates also carry `TASK DOC: {absolute path}` / `REQUIREMENT DOC: {absolute path}` fields.

## 2. The plan under audit (verbatim, no pre-defense)

Two identical PHASE BOUNDARIES blocks, one fix:

1. `skills/spec-tdd-task-loop/SKILL.md` (~L146, immediately after the heartbeat instruction)
2. `skills/spec-tdd-supervisor/SKILL.md` (~L163, immediately after the heartbeat instruction)

The fix: add one hard rule, proposed English wording (consistent with the template's language):

> ~~"Resolve `.spec-tdd/...` against the repo-root cwd and use this RELATIVE form verbatim for the touch, the POLICY re-read, and every scratch write; NEVER hand-compose an absolute path — mkdir -p plus output-redirect makes a typo'd absolute path silently succeed, materializing a parallel tree whose heartbeat the watchdog never sees (2026-09-18 W22 incident)."~~
>
> **[Superseded — audit #1 C5(ii) refuted: "resolve against the repo-root cwd" leans on the very cwd the family doctrine declares unreliable; the wrong-cwd hole stays open and the dag worktree mode gets the wrong anchor; the five follow-up amendments are in section 7, the final text in section 8]**

The proposer's own emphasis: it must cover the POLICY re-read and **all scratch writes** in the same phase-boundary block, not just the heartbeat itself.

## 3. Claims to verify (falsifiable, each with an indicator)

- **C1 (task-loop current state)**: the PHASE BOUNDARIES block of `skills/spec-tdd-task-loop/SKILL.md` sits at L144–151, the heartbeat instruction reads as quoted in section 1, and the block contains no absolute-path ban.
- **C2 (supervisor current state)**: the corresponding block of `skills/spec-tdd-supervisor/SKILL.md` sits at L161–168, the same-shaped `<unit>` version.
- **C3 (root-cause correspondence)**: the two current blocks genuinely leave room for "the agent may compose absolute paths itself and `mkdir -p`/redirection makes the typo silently succeed" — i.e. the proposed root cause holds at the text level.
- **C4 (coverage)**: are those two files the (only) carriers of this hazard in the family repo? At minimum check: `skills/spec-tdd-task-dag/SKILL.md` (the parallel overlay, worktree waves), `skills/PROTOCOL.md`, and heartbeat / `.spec-tdd/` scratch-write instructions of the same type in the other skills (e.g. task-loop's template RETURN "full logs to scratch files under `.spec-tdd/`", supervisor's template "WRITE the full report to `.spec-tdd/<unit>/REPORT.md`"). Does fixing only two files leave a sibling hole?
- **C5 (wording side-effects)**: the proposal's interaction with the existing "restore path shorthands to absolute paths (cwd unreliable)" doctrine — is the jurisdiction of "NEVER hand-compose an absolute path" clearly limited to `.spec-tdd/…` (otherwise it collides with the TASK DOC / FAMILY FILES fields' absolute-path instructions); is "resolve against the repo-root cwd" consistent with the "sub-agent cwd is unreliable" doctrine (when cwd ≠ repo root, relative form + mkdir -p still materializes in the wrong place); the insertion point ("immediately after" = after item 1 vs. the block's end) and its effect on C4 / the coverage emphasis.
- **C6 (drift)**: line numbers and quotations vs. the two files' on-disk state; whether recent `git log` commits touched these blocks (this repo's recent v1.23.0 touched supervisor).

## 4. Checklist (the auditor executes at minimum)

(a) verify each claim; (b) blueprint-vs-code drift (dates/commits cross-checked); (c) cross-item interaction risks (incl. C5's doctrinal tension, worktree mode if relevant); (d) a verdict on the fix as a whole + the strongest counter-argument (e.g. is instruction text the right repair layer — does the relative form still have a wrong-cwd hole; is there a stronger shape, like the template handing over a verbatim instruction directly); (e) one risk nobody listed.

## 5. Pending user decisions (the auditor may only annotate consequences, never decide)

- Whether to adopt this fix, and the final wording / insertion point (incl. choosing among the audit's amendments).
- Version number and commit: always the user's manual act; this session never git-commits.

## 6. Audit record (fill-in section)

- 2026-09-21 **Audit #1 complete** (read-only TOP, background). Verdict: C1/C2/C3/C6 confirmed; C3 moreover rated understated (the family's cwd doctrine actively pushes toward hand-composed absolute paths); C4 partially — the heartbeat/POLICY wording lives in only two files, but same-species surfaces exist elsewhere (supervisor L267 FINAL-AUDIT write, spec-tdd L82, coverage L75, adversarial L94/L100; task-dag L42 reuses the template so the edit flows in automatically, and its L49 worktree mode constitutes a trap); C5(i) partially (NEVER unscoped), C5(ii) refuted (cwd-resolution contradicts the "cwd unreliable" doctrine + the wrong-cwd hole + the wrong dag worktree anchor), C5(iii) partially (placement inside item 1 misleads jurisdiction). Position: agree with the direction and the two anchor points, disagree with the wording as-is — five required amendments. **Orchestrator arbitration: all five adopted** (see the amended text in section 7).
- 2026-09-21 **Re-audit #2 dispatched** (fresh, read-only TOP, scoped to the amended text + the disagreement history). Results pending notification.
- 2026-09-21 **Re-audit #2 complete**. Verdict: R1/R2/R4 confirmed (both holes closed, zero conflict with the absolute-path fields, the bare-relative reading blocked by three signals, ABSENT semantics executable with the fast path preserved); R3/R5/R6 partially — the dag wave-mode text correct but missing the dispatcher-side fill rule (a double-fault silent path), the L261 brief inventory not extended (deadlock risk), the separator and join left unstated. **New risk (e)**: PATH RULE's "in this prompt" structurally stops at the nesting boundary — the level-1 brief for level-2 uses the tier SKILL.md's handoff template, whose `.spec-tdd/` shorthand is still unanchored, and the write-heavy layer is exactly the incident's surface. **Position: endorse the amended plan** — A1 required (dispatcher fill rule: task-loop L73 / supervisor L57 / dag L42), A2 strongly recommended (item 3 gains a carry-down sentence), A3 recommended (L261 inventory gains the FINAL-AUDIT path), A4 cosmetic ("; 3)" separator + "joined with a `/`"). **Orchestrator arbitration: A1–A4 all adopted. The audit bound is reached (audit + one re-audit); no further round.**

## 6.5 Post-implementation audit (audit #3, 2026-09-21)

- Post-implementation read-only TOP audit (working tree vs. blueprint §7/§8 + the user's change-them-all scope): **P1–P5 all confirmed; position = agree-to-release**. Two deviations from the blueprint's letter were independently verified as substance-preserving and more correct (the supervisor field can never carry a dag-wave mode, so the clause was dropped; the dag WAVE line gained its rationale). CHANGELOG under-claim nit (the ABSENT hardening attributed to loop only, supervisor omitted) — **fixed per the audit's correction** (before commit).
- **P6 residual risk (on the record, next release)**: the tier skills' multi-unit wave scratch-copy location is not pinned — if a copy is cut **inside** the repo working tree, `git rev-parse --show-toplevel` from inside the copy succeeds against the parent repo, and the handoff's branch condition ("in a git repo/worktree: rev-parse must equal it; otherwise pwd-inside") turns ambiguous: a literal reader would STOP on a **correctly filled** SCRATCH ROOT (every card of that wave fail-stop deadlocks). The worst case is fail-stop or a run.log in the wrong place — not the silent phantom tree this fix targets — so it doesn't block this release. **Cheap fix (left for a future release)**: one sentence pinning wave copies outside the repo working tree, or changing the branch condition to "SCRATCH ROOT carries no `.git` of its own → pwd branch". Secondary thought (weak): the top-side read-only dispatches' (Phase 0 plan-review, closing batch review) heartbeat signal has no text-level anchored path — not a regression of this change, but the same species of "unanchored dispatched writer".
- **Release chain executed**: both sides agreed (auditor agree-to-release + orchestrator agreement, incl. the two document fixes) → commit (short) + tag v1.24.0 + GitHub release + push + `cp -r skills/* ~/.claude/skills/` (explicitly authorized in the user's decision 3).

## 7. Amended plan text (after audit #1's five amendments integrated; the re-audit #2 target)

### 7.1 The SCRATCH ROOT field (one per template, adjacent to TASK DOC / REQUIREMENT DOC)

```
SCRATCH ROOT: {absolute path} — paste-verbatim anchor for EVERY
`.spec-tdd/` path in this prompt (repo root; under task-dag's wave
reuse, the assigned worktree root).
```

### 7.2 The amended PHASE BOUNDARIES block (final = audit #1's five + re-audit #2's A2/A4 folded in; the task-loop version; supervisor the same shape, `<unit>`, no raising clause at item 2's end, item 3's enumeration adds REPORT.md)

```
PHASE BOUNDARIES (before/after each nested dispatch, when ENTERING a wait
on a nested dispatch, after each completed long tool run, after each
delivered file): 1) touch `.spec-tdd/<task>/HEARTBEAT` (create the
directory if missing; touch or an equivalent write) — when the touch
coincides with entering a wait, write into the file: "waiting: <child-id>
expected-done <time>"; 2) re-read `.spec-tdd/POLICY-<task>.md` — ABSENT
means ONLY a confirmed file-not-found (e.g. `test -f` fails); any OTHER
read error is a STOP, not "no policy"; a PRESENT file overrides TIER
BAND above, DOWNGRADE-ONLY (raising waits for the next task boundary);
3) PATH RULE (every `.spec-tdd/` path in this prompt — the touch, the
POLICY re-read, every scratch write, incl. RETURN's logs): form it by
prefixing SCRATCH ROOT from your brief, joined with a `/`, PASTED
VERBATIM — never retype it, never resolve it against your own cwd, never
hand-compose any other absolute form; mkdir -p plus output-redirect makes
a typo'd absolute path silently succeed, materializing a parallel tree
whose heartbeat the watchdog never sees (2026-09-18 W22 incident).
Before the first such write: `git rev-parse --show-toplevel` must equal
SCRATCH ROOT — a mismatch is a STOP-and-report, never a best-effort
guess. Carry SCRATCH ROOT and this PATH RULE verbatim into every nested
brief you compose (implementer, reviewer, attacker): their templates'
`.spec-tdd/` shorthand is anchored by YOUR pasted root, never their own
cwd.
```

> A4 (per re-audit #2): the separator unified to "; 3)", the join stated as "joined with a `/`" (a naive string concat missing the `/` reproduces the silent materialization; the rev-parse gate checks only the root, not the seam).
> A2 (per re-audit #2): the final carry-down sentence — closes the new hole of "PATH RULE stops at the nesting boundary" (the level-2 implementer / attacker's `.spec-tdd/` shorthand is taken over by level-1's pasted anchor).

### 7.3 Amendments to supervisor's final review 2 "output and evidence rules" bullet (L267) + brief inventory extension (L261, per re-audit #2 A3)

- L267: the findings' full text goes to `.spec-tdd/<unit>/FINAL-AUDIT.md` (resume substrate) — **the file named by absolute path in the brief (SCRATCH ROOT pasted, never retyped); the auditor never composes paths itself**; + a returned summary.
- L261 brief inventory gains one item: **the absolute path of FINAL-AUDIT.md (pasted by the top) — the auditor's only write target** (without it, a top strictly following the checklist would omit the path, deadlocking against L267's ban).

### 7.4 Dispatcher-side fill rules (per re-audit #2 A1 — required)

- task-loop L73 (the dispatch instruction), appended at the sentence end: "the template's **SCRATCH ROOT** field takes this run's absolute scratch root path (the convention = repo root)".
- supervisor L57: the same addition.
- task-dag L42 (the WAVE line) extended: "SCRATCH ROOT takes that task's worktree root (cut by the top; the absolute path is known)." — closes the wave-mode double-fault silent path (when "the top fills repo root" + "the agent stays in the real tree" coexist, rev-parse actually passes and the heartbeat lands in the wrong tree).

## 8. FINAL PLAN (settled; the user has decided — implementation and scope below)

**User decisions (2026-09-21)**: 1 = change them all (class-level retirement: beyond the 3 files / 8 points, extend the mechanism in the same batch to the three tier skills spec-tdd / coverage / adversarial — "it's just requiring an absolute path; change them all"); 2 = A (no phantom-tree detection — the prevention side is already double-gated); 3 = implementation authorized; after completion spawn a subagent audit; the release chain runs only when both sides agree (short commit + tag v1.24.0 + release + push + `cp -r skills/* ~/.claude/skills/`).

**Edit list (3 files, 8 points, listed in implementation order):**

1. `skills/spec-tdd-task-loop/SKILL.md`
   - a. L73: the SCRATCH ROOT fill rule (7.4)
   - b. after the L101 TASK DOC section: the SCRATCH ROOT field (7.1)
   - c. L144–151: the PHASE BOUNDARIES block rewritten (7.2 final, task version)
2. `skills/spec-tdd-supervisor/SKILL.md`
   - a. L57: the SCRATCH ROOT fill rule (7.4)
   - b. after the L105 REQUIREMENT DOC section: the SCRATCH ROOT field (7.1)
   - c. L161–168: the PHASE BOUNDARIES block rewritten (7.2 final, unit version)
   - d. L261 brief inventory gains the FINAL-AUDIT path item (7.3) + the L267 bullet clause (7.3)
3. `skills/spec-tdd-task-dag/SKILL.md`
   - a. L42 WAVE line: SCRATCH ROOT = the worktree root (7.4)

**Rationale**: W22's root cause = the dispatched agent hand-composing an absolute path + `mkdir -p`/redirection succeeding silently. The fix extends the family's existing reliability anchor (the dispatcher fills absolute paths; the cwd-unreliable doctrine) to the scratch namespace: SCRATCH ROOT pasted verbatim, never retyped (closes the typo hole), no cwd resolution + the rev-parse gate (closes the wrong-cwd hole and also intercepts a dispatcher that fills it wrong itself), carry-down (closes the nesting-boundary hole), hardened ABSENT semantics (closes the `2>/dev/null` false negative).

**Attribution**: proposal = the original session (wording superseded, see the strikethrough in §2); the five amendments = audit #1; A1–A4 = re-audit #2; arbitration and integration = the orchestrator.

**Pending user decisions (presented in conversation; not decided here)**
1. Class-level scope: the standalone tier run templates (escalate → spec-tdd L82 / coverage L75 / adversarial L94/L100) still use unanchored relative shorthand — this fix + A2 covers only the nested briefs under the loop/supervisor/dag shapes. Do the class-level retirement in the same batch, or list it as tech debt?
2. The phantom-tree detection add-on: yes / no.
3. Adoption of this plan and implementation authorization (SKILL.md is touched only after explicit consent).
4. Version number and commit (user manual).

**Residual risks (surfaced by the audits, not blocking)**
- Top-side `.spec-tdd/` writes (RUN-STATE supervisor L59, POLICY writes task-loop L227 / supervisor L276) are outside the paste rule's jurisdiction — pre-existing scope, noted for the record.
- The rev-parse gate is one-shot (before the first write); later re-typing drift is guarded only by instruction.
- `test -f` misreads EACCES corners as not-found — negligible in the scratch scenario.
- Once a phantom tree exists, the gate's `git status` never sees it (outside the repo) — detection is pending decision 2.

**Disclosures**
- Orchestrator tier decline: this session is non-top (`glm-5.3-flash`); the I21 ask was answered ignore by the user — the review judgment ran in a TOP-pinned auditor dispatch; the orchestrator only distilled the brief / arbitrated / integrated.
- Audit bound: audit #1 + re-audit #2 (audit-plus-one, I16's shape); the cap is reached.
- The incident's facts (dtms-core, 2026-09-18) were taken as given from an external session's report, not re-verified (both auditors so stated).
