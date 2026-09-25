---
name: spec-tdd-task-dag
description: Use when driving a multi-task feature phase whose WALL-CLOCK matters and the task plan is a dependency DAG — independent tasks run as parallel waves on a task-loop substrate (authoritative plan doc + per-task commits). Parallel multiplies quota pressure ×N (cap 3, user-adjustable); the serial sibling spec-tdd-task-loop is the 429-safe mode; a plain multi-unit bug batch is NOT this skill. Triggers on parallel tasks, dependency graph, task waves, wall-clock pressure, auto time-band switching, DAG scheduling.
---

# spec-tdd-task-dag

**REQUIRED BASE:** `spec-tdd-task-loop` — read it first; every rule there applies unchanged (the three-layer division of labor, the lightweight gate, the Phase 0 breakdown bootstrap, number recheck, mock-first, resume, disclosure, commit discipline). This skill is its **parallel overlay**: the task table upgrades from a serial queue to a dependency DAG, and tasks that are independent and file-disjoint run as parallel waves. No verification strength added or reduced — only wall-clock compressed (the wave-end union test run pays back what parallelism dropped, see below).

**`eco` inheritance (task-loop's Eco mode section applies in full)**: per-card machinery all MID + a per-card TOP final audit (after the gate, before the merge) — parallel waves are eco's biggest beneficiary: **the wave's top-context ×N quota pressure disappears** (the wave's machinery is all MID; the per-card final audit is a short read-only TOP, running staggered as cards converge, never concurrent as a wave). The final audit converges **inside that card's worktree** (diff, XML, `REPORT.md` all use that worktree's paths; `FINAL-AUDIT.md` lands in that card's worktree scratch — the existing rule that SCRATCH ROOT takes the worktree root), and only after convergence does the card enter the wave-end merge; the wave-end union run and the closing batch review are unchanged (additive, not substitutes).

## When to Use (vs task-loop)

- Time-sensitive + the DAG has a genuinely parallel structure (not a chain) → this skill. Parallel multiplies **quota pressure (×N, cap 3) and top-level context overhead** at once (status-row traffic, wave management, per-sibling handling) — for a context-tight phase, serial is cheaper.
- Chain-shaped dependencies / few tasks / conservative in 429-prone hours / wanting the simplest machinery → `spec-tdd-task-loop`. **Serial is not the old behavior — it is the ×1-quota-pressure safe mode**: parallel multiplies token throughput by the concurrency; in trigger-prone hours (e.g. daytime peak) go one at a time, and run the DAG full-speed in off-peak (e.g. overnight) — the mode is a function of the time band in the first place.

**When NOT to use:**
- Parallel waves of a multi-unit bug batch (no task-loop substrate: no authoritative plan doc, no per-task commits) → `spec-tdd`'s **multi-unit** parallel waves.

## Board upgrade: the task table = a DAG

- Each row gains two columns: **depends-on** (empty = root) and **expected files** (produced by the Phase 0 breakdown together with the rest).
- Phase 0's fresh-context review thereby gains one more attack dimension: **dependency-edge correctness + the expected-files column's disjointness**.
- **Wave computation = topological grouping + the expected-files disjointness check.** Two tasks whose columns overlap never share a wave, even if logically independent — shared files = a serial chain (the tier layer's multi-unit wave rule, lifted). What disjointness excludes is **textual merge conflicts**; **semantic interference (zero shared files yet each changes the other's behavior) cannot be excluded by disjointness** — it is backstopped by the wave-end union run (next section).

## Pre-flight: the mode ask (after task-loop's asks, one more question)

Present the wave structure (e.g. "3 waves: [T01,T03] → [T02,T04,T05] → [T06]"), four options:

- **All-parallel** — recommended for off-peak hours; **all-serial** — behavior identical to task-loop, the safe choice in 429-prone hours;
- **Per-wave choice** — ask at every wave boundary, parallel or serial;
- **Auto time band** — you report the peak/off-peak bands once (e.g. "10:00–22:00 peak, run serial; otherwise parallel" — **the bands are your quota experience; the skill presets nothing**), then every wave boundary switches automatically by local time, each switch disclosed on the board. Switching takes effect at wave boundaries; **an in-flight wave is never killed mid-flight**.

A chain-shaped DAG (nothing parallelizable) → this ask is silently skipped. **Concurrency cap 3 (user-adjustable)**: at most 3 tasks running per wave (each task internally still has 2–3 nested dispatches, at most ≈9 agent streams); an overflowing wave rotates in batches.

**Authorization coupling (task-loop pre-flight 2)**: without top-commit authorization → **parallel mode is unavailable, automatically degrading to all-serial** — the DAG's task commits are top-executed `git merge`s; there is no "pause and hand to the user for a manual commit" counterpart shape; the degradation is disclosed.

## Parallel wave execution (worktree isolation)

- **The wave-start tree must be clean, and verified, not assumed**: before cutting worktrees the top personally runs `git status` — non-scratch residue (untracked scratch excepted) → STOP; clean it first.
- Each parallel task: `git worktree add .spec-tdd/worktrees/<id> -b task-dag/<id>` (from the wave-start HEAD). The tier layer's worktree ban ("a worktree branches from HEAD; uncommitted work doesn't transfer") **does not hold here** — on a clean tree, HEAD is everything; this is a difference of premises between the two layers, not a relaxation.
- **Document authority lives in the real tree**: task docs and the plan doc are authoritative in the real tree (the dispatch prompt points at real-tree absolute paths, read-only); the worktree carries only production/test code and build outputs (**pure-docs tasks' deliverable documents excepted** — they ride the worktree and merge back into the real tree at wave end; the path-level check runs on the real tree after the merge). When a user decision made mid-wave is written back to the real tree and affects in-flight siblings → deliver by SendMessage (same as mid-run redirection); undeliverable → that task **re-verifies against the decisions section before its merge**.
- Level-1 works entirely inside the worktree (code work): RED → level-2 → GREEN → verification, XML numbers all in its own tree. Sub-agents stay git-write-banned; **creating/merging/cleaning worktrees is the top's exclusive duty**.
- The dispatch template is task-loop's verbatim, plus one line: WAVE (siblings in flight: <ids> — expected-files columns are disjoint; touching their files is banned); **SCRATCH ROOT takes that task's worktree root** (cut by the top, absolute path known — level-1 lives in the worktree the whole way and the watchdog reads that tree too; wrongly filling the repo root wedges every card at the rev-parse gate, and the double fault of "repo root filled + agent staying in the real tree" silently reproduces the W22 stale-heartbeat shape).
- **Wave-end serial merges**: each branch in task-table order, `git merge --no-ff task-dag/<id>` — each merge commit = that task's commit boundary. A conflict (which should not happen under the disjointness rule) → STOP, hand to a human. **Board updates cannot ride the merge commit (the merge hash only exists after the merge) → right after the wave's last merge, one board commit** (status-section hashes, decisions section, mode-switch disclosures). **The rollback unit = the merge commit + the board commit after it, both reverted together** — reverting only the merge leaves a board claiming done.
- **The wave-end gate (after the merges, in the real tree)**: the existing lightweight gate (the two compile items + diff scope) **plus a fourth item, "the wave-union test run"** — the union of the wave's every task's related test classes, run once in the real tree (once per wave, still far cheaper than serial's once per task; **a pure-docs task's numbers item is replaced by the path-level check, as in task-loop gate item 5; testless tasks don't enter the union**). The top personally running this run is a named gate exception (the same nature as compile: new information, no existing XML to recheck; the same shape as the "re-running the full suite is a diagnostic exception" rule), evidence = that run's XML numbers. The union run itself is the wave's final run; the XML-coverage trap does not apply to it.
- **At wave end, re-verify the anchors of ALL next-wave task docs at once** (re-anchored by method name) — a wave lands many tasks simultaneously; drift is larger than serial's.
- Worktree reclamation: branches all merged, residue only scratch/build → `git worktree remove --force` + delete the branch (level-1 always leaves scratch and build outputs, so a clean remove is always refused; on Windows there are also gradle daemon file locks).
- **The regression wall**: wave N's worktree is cut from the merged wave N−1 HEAD → the template's "one run covering all related test classes" per task verifies **all previous waves'** tests; cross-green **among same-wave siblings** is backstopped by the wave-end union run (semantic interference cannot be excluded by file disjointness). Union run all green → no residue.
- **The closing batch review** (task-loop's closing procedure) runs in the real tree **after all waves are merged and the table is all-done** — wave boundaries don't trigger it (what it looks at is exactly the whole phase's accumulated effect, not one wave). Its fix rows enter the DAG as usual: **depends-on and expected-files columns must be filled** (empty = root); the convergence re-round is scoped to the fix rows' diffs.
- **Watchdog signal paths and output axes live inside the worktree**: level-1 stays in the worktree the whole way — heartbeat / POLICY files, tree diff (vs the wave-start HEAD), build/test outputs all read **that worktree's** paths (the worktree was cut by the top; the absolute path is known) — reading the real tree's counterpart paths is forever stale, and every parallel card past its threshold would false-alarm. Checkpoints: **one wakeup serves all in-flight** (not scheduled per card — the top's context economics under ×N parallelism); a zombie inside a worktree → the revival attempt and the continuation re-dispatch take over in that same worktree, paths unchanged. **A cold worktree's first build is cold** (no daemon cache) — a parallel task's budget must count the cold build, or it overruns the moment it starts.
- **The pre-scheduled ladder and the freeze SOP (inheriting task-loop watchdog rules 1–2 and the 429 section; only the wave-shape delta recorded here)**: parallel already multiplies quota pressure (×N, cap 3) — far-fires and the freeze procedure are the normal path in dag, not a corner. The fine-rung horizon = the **maximum** of the in-flight cards' budgets; top the ladder up at every wave dispatch; **a freeze freezes wave boundaries too** — wave dispatches falling due during the freeze are deferred; the first successful turn collects first (sibling cards completed during the freeze, waves due but not dispatched, board reconciliation) before judging and scheduling waves; the freeze deduction applies **per card** — sibling cards on different pools running while the top is frozen is the norm in dag; collect-before-judge is worth more here than in serial.

## Resume (a wave interrupted)

- The board's in-flight may be **a whole wave**: each worktree resumes independently — a 429 killing one doesn't touch the siblings (SendMessage resumes that agent; the worktree's state is the inventory result); one dying before its merge → the branch is kept, waiting for recovery to continue; one dying after its merge → identical to task-loop's single-task resume.
- One agent in a wave dying of 429 with little remaining work → task-loop's rule: wait for reset and SendMessage-resume the same agent, or immediately re-dispatch a continuation agent taking over that worktree; **the top finishing the work by hand is equally hard-banned here** — the worktree's state is a ready-made inventory metric; even what changed is in the branch diff. The wave's other tasks are unaffected: no waiting, and no killing siblings.
- Mode switches (per-wave / auto time band) take effect at wave boundaries; an in-flight wave is never killed mid-flight; task-loop's mid-run redirection conventions apply, disclosed on the board.

## Common Mistakes (delta)

| Mistake | Fix |
|---|---|
| Putting two tasks with overlapping expected-files columns in one wave | Wave membership = topologically independent + file-column disjoint, both required; shared files → a serial chain. |
| Forcing all-parallel in 429-prone hours | Serial = ×1 quota pressure; parallel ×N (cap 3). The mode should follow the time band — the auto-band mode exists for exactly this. |
| Trusting the in-worktree green, skipping the wave-end gate (incl. the union run) | File disjointness excludes only textual conflicts; semantic interference is backstopped by the wave-end union run — it is a mandatory gate item, not optional. |
| A sub-agent touching git inside the worktree | The ban is unchanged; worktree create/merge/clean is the top's exclusive duty. |
| A sibling in the wave dying and the top absorbing its remaining work | Hard ban (task-loop's rule inherited) — re-dispatch a continuation agent to take that worktree; the wave's other tasks are unaffected: no waiting, no killing. |
| Reverting the merge commit but leaving the board commit after it | The rollback unit = merge commit + board commit, both together; a board claiming done while the code is rolled back = the status section lying. |
| Forcing parallel on without commit authorization | Parallel mode is unavailable; automatically degrades to all-serial, disclosed — the DAG's commits are the top's merges; there is no manual path. |
| Treating the worktree's copy of a task doc as the authoritative version | Document authority lives in the real tree (dispatch points at real-tree paths, read-only); mid-wave decisions delivered by SendMessage, undeliverable → re-verified before the merge. |
| Under eco, the final audit reading real-tree paths (the card hasn't merged; the real tree doesn't hold its output) | The final audit converges inside that card's worktree: diff, XML, `REPORT.md`, `FINAL-AUDIT.md` all use worktree paths; what only exists after the merge is not its review object. |

## Red Flags — STOP (delta)

- The same file appearing in two same-wave tasks' diffs → the disjointness claim is bankrupt; STOP; move that task out of the wave and reschedule serially.
- Non-scratch residue in `git status` before cutting worktrees → STOP; clean it before cutting (a clean wave-start tree is a premise, not an assumption).
- Any red in the wave-end union run → STOP and diagnose (semantic interference actually happened); no board commit before all green.
- An auto-band switch not disclosed on the board → add the disclosure; switch records belong to the phase report.
