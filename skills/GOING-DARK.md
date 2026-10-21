# Unattended Window (the Going-Dark Protocol)

For: `spec-tdd-manager` / `spec-tdd-task-loop` / `spec-tdd-task-dag` / `spec-tdd-supervisor` (and any future driver or front door). Loaded at the moment the user announces leaving / sleeping / going offline with work in flight. Dialect mapping: "the top" means the driving top session (under supervisor, the session itself); "the board" means the plan-doc status board (under supervisor, `RUN-STATE.md`; under manager pre-S5, the plan trio / spec doc); tier pins are the driving skill's (supervisor's stay MID). The gates' pre-approval shape lives in manager's own text.

Work in flight + the user unreachable — asleep, out, in a long meeting: any window where an ask cannot be answered is dead on arrival. Overnight is the sharpest case (task-dag's auto time band routes full-speed waves there; field 2026-10-05/06: a 429-killed card with a known 02:56 reset sat dead ~4.5 h because the session-only insurance had no live session to fire it), but a two-hour absence hits the same wall at smaller scale.

## The going-dark gate (one batched ask)

Everything the window may need is asked ONCE, up front. Collect, stating a default per item:

0. **Expected return** — drives how much gets armed (a short absence with the session left alive needs nothing; overnight or unknown needs the full set).
1. **Unattended commit authority** — loop/dag: (a) **auto-commit ON** — per-task/wave merges and board commits land unattended at their normal cadence, exactly as an attended run (the returning review finds the board + commit list; the approval covers THIS absence only and is re-asked at every gate — it never carries over), or (b) **hold-until-return (default)** — recover, converge, run the lightweight gate, stage everything, zero git writes until the user returns. Supervisor: the no-commit close is structural (converge + stage the file list; commits are the user's act on return — an explicit on-behalf instruction is honored and disclosed).
2. **Recovery actions pre-approved** — SendMessage resume, continuation re-dispatch, different-pool tier-pinned overrides (blanket or per action).
3. **Unattended tier ceiling** — convergence downgrades allowed down to which tier (default: the band floor).
4. **Open decisions that could block a card** — pre-ruled now or explicitly deferred (a deferred blocker = that card parks, disclosed on the board).
5. **Run scope** — what state the return should see (through which cards / what counts as closed); without it the returning user cannot tell "on track" from "stalled" (field 2026-10-21: one gate carried it — "through T11" — and its morning read clean; the other lacked it and read as dead while actually working).

One round, no follow-ups.

## Substrate choice (declared at the same gate)

The recovery machinery needs a live host:

- (a) **Keep this session alive** — machine sleep off, Claude open; the session's recurring watchdog ring re-fires on its own through and after any exhaustion window (no successful turn needed — trial-verified 2026-10-21), and the durable reset+15 point (when armed for this window) covers the named reset; zero new machinery at this gate.
- (b) **Arm the OS-level fallback** (below).

A closed session has NO insurance — say so at the gate instead of discovering it at 03:00.

## OS-level unattended recovery (the fallback; armed only with the gate's consent)

Reset moment known and the session will not stay alive: schedule a one-shot OS task at reset+15 (Windows: `schtasks /create /sc once`, self-deleting) that runs headless `claude -p` in the repo with the SAME self-contained self-retiring prompt shape as a watchdog ring (board path + in-flight interpretation + recovery instruction + "board shows no in-flight → stand down" — in this headless cross-session context the **BOARD is the in-flight authority**: a fresh session's agent list is empty by construction and notifications may drop; never judge in-flight from the agent list here), with the machine-wake flag if the machine sleeps rather than shuts down. The headless top obeys the gate's rulings exactly (commit authority per item 1; content judgment never — mechanical completion stays a dispatched agent's job) and must be launched with a permission mode that survives unattended operation; everything it does is disclosed into the board for the return. No gate consent → this fallback does not arm.

## Return re-arm

First turn of any session launched after the window: read the current wall clock, then check the board's (or RUN-STATE.md's) freeze rows and pending durable insurance — a missed durable one-shot whose named reset is ALREADY PAST means collect-and-resume NOW, never execute the stale point (v1.32.1; field 2026-10-21: a revival scheduled a point 5h45m past and advised waiting for it); collect-before-judge and freeze-window deduction per the freeze SOP, then resume per card (the recurring ring is re-created + verified at this first dispatch).
