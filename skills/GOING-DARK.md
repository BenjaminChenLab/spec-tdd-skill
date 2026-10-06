# Unattended Window (the Going-Dark Protocol)

For: `spec-tdd-task-loop` / `spec-tdd-task-dag` / `spec-tdd-supervisor` (and any future driver). Loaded at the moment the user announces leaving / sleeping / going offline with work in flight. Dialect mapping: "the top" means the driving top session (under supervisor, the session itself); "the board" means the plan-doc status board (under supervisor, `RUN-STATE.md`); tier pins are the driving skill's (supervisor's stay MID).

Work in flight + the user unreachable — asleep, out, in a long meeting: any window where an ask cannot be answered is dead on arrival. Overnight is the sharpest case (task-dag's auto time band routes full-speed waves there; field 2026-10-05/06: a 429-killed card with a known 02:56 reset sat dead ~4.5 h because the session-only insurance had no live session to fire it), but a two-hour absence hits the same wall at smaller scale.

## The going-dark gate (one batched ask)

Everything the window may need is asked ONCE, up front. Collect, stating a default per item:

0. **Expected return** — drives how much gets armed (a short absence with the session left alive needs nothing; overnight or unknown needs the full set).
1. **Unattended commit authority** — loop/dag: (a) **auto-commit ON** — per-task/wave merges and board commits land unattended at their normal cadence, exactly as an attended run (the returning review finds the board + commit list; the approval covers THIS absence only and is re-asked at every gate — it never carries over), or (b) **hold-until-return (default)** — recover, converge, run the lightweight gate, stage everything, zero git writes until the user returns. Supervisor: the no-commit close is structural (converge + stage the file list; commits are the user's act on return — an explicit on-behalf instruction is honored and disclosed).
2. **Recovery actions pre-approved** — SendMessage resume, continuation re-dispatch, different-pool tier-pinned overrides (blanket or per action).
3. **Unattended tier ceiling** — convergence downgrades allowed down to which tier (default: the band floor).
4. **Open decisions that could block a card** — pre-ruled now or explicitly deferred (a deferred blocker = that card parks, disclosed on the board).

One round, no follow-ups.

## Substrate choice (declared at the same gate)

The recovery machinery needs a live host:

- (a) **Keep this session alive** — machine sleep off, Claude open; the existing session-scoped reset+15 then fires on its own at reset+15, zero new machinery.
- (b) **Arm the OS-level fallback** (below).

A closed session has NO insurance — say so at the gate instead of discovering it at 03:00.

## OS-level unattended recovery (the fallback; armed only with the gate's consent)

Reset moment known and the session will not stay alive: schedule a one-shot OS task at reset+15 (Windows: `schtasks /create /sc once`, self-deleting) that runs headless `claude -p` in the repo with the SAME self-contained self-retiring prompt shape as a ladder rung (board path + in-flight interpretation + recovery instruction + "no in-flight → stand down"), with the machine-wake flag if the machine sleeps rather than shuts down. The headless top obeys the gate's rulings exactly (commit authority per item 1; content judgment never — mechanical completion stays a dispatched agent's job) and must be launched with a permission mode that survives unattended operation; everything it does is disclosed into the board for the return. No gate consent → this fallback does not arm.

## Return re-arm

First turn of any session launched after the window: check the board's (or RUN-STATE.md's) freeze rows and pending durable insurance (a missed durable one-shot surfaces for catch-up) — collect-before-judge and freeze-window deduction per the freeze SOP, then resume per card.
