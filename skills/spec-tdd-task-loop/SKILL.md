---
name: spec-tdd-task-loop
description: Use when driving a whole MULTI-TASK feature phase — a task plan split into many self-contained task docs, run one task at a time with per-task commits, a plan-doc status board, and sessions that must survive the phase. The main session stays a LIGHTWEIGHT gate (compile + `git diff --stat` + JUnit-XML number recheck — never deep review, never running the tests itself); each task dispatches a level-1 sub-agent that runs the spec-tdd-escalate/tier machinery and itself dispatches the nested implementer (no self-testing — requires CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3). Covers mock-first contract phases (the time dimension of tier choice), mid-run tier downgrades delivered by SendMessage, and resuming a half-finished task after a session break. Triggers on task loop, task-by-task spec-tdd, multi-task orchestration, per-task commit cadence, plan status board, not-yet-split requirement/blueprint needing task breakdown, 多 task 迴圈.
---

# spec-tdd-task-loop

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — the front-ends (`grill-spec-tdd`, `spec-tdd-escalate`), the tiers (`spec-tdd-lite` / `spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`), and [PROTOCOL.md](../PROTOCOL.md) (I1–I21 / A1–A16). 本 skill 不新增也不放寬任何 invariant:每個 task 的執行仍由 tier 機械完整落實(**band 但書**:下緣 lite 是帶補償的加強——強制 fresh review;上緣 coverage 對 critical 單元是經濟規則的結構性不承載,不是 invariant 修改,逃生口見下);這裡定義的是疊在整個家族**外層**的迴圈規則——三層分工、輕量 gate、數字複核、mock-first、續作與揭露。

## Overview

一個多 task phase:任務總表、每 task 一份自足 doc、逐 task 開發與 commit、可能跨越多個 session。**頂層 context 是整個 phase 最稀缺的資源**——唯一必須從頭活到尾的是它。所以深度工作(acceptance test 撰寫、encoding audit、實作、攻擊輪)全部下沉到可拋棄的 sub-agent context;頂層只做兩類事:

1. **跨 task 狀態管理** — 挑 task、維護權威計畫文件的狀態區與決定區、決策回寫、每 task 一個 commit。
2. **輕量 gate** — 只驗「客觀可核事實」:編譯、檔案範圍、測試數字。每項都是機器可比對的,不需要品味也不需要 level-1 的 full context。

| 層 | 是誰 | 做 | 禁止 |
|---|---|---|---|
| 頂層 orchestrator | 主 session(program conductor)| 跨 task 流程、輕量 gate、狀態區維護、決策回寫、commit | 深度 code review、親自跑測試、寫 acceptance test、實作 |
| level-1 sub-agent(**TOP**,I19)| 單 task 的 spec-tdd orchestrator(跑 escalate 機械)| 寫 acceptance test(RED)、encoding audit、派 level-2、親自驗證(re-run / coverage / hash)、tier 要求的攻擊輪;lite 路線:solo 實作 + fresh-context review dispatch(該 tier 自身的機械形狀) | 自己實作 production code(非 lite tier——例外見 template 的 TIER BAND)、git 寫入 |
| level-2 implementer(**MID**,I19)| 實作者 | 實作到綠 + 自身 unit tests | 改 acceptance test(hash 鎖定)、git 寫入 |

tier 為 `spec-tdd-adversarial` 時,level-1 內部再派 attacker / dry-loop auditor——**adversarial 不在迴圈內承載**(見 Pre-flight 3 的 tier band):critical 單元的預設路徑是**拉出迴圈 standalone 跑**(Phase 0 sniff 預拉、路由點發現即 STOP 回報),留在 loop 內跑 coverage 需 user 明示並進殘餘風險清單。

**為何禁 self-testing(同一 agent 寫碼 + 寫測 + 自評):circular reasoning。** 實作者的盲點會同時進入 code 與 test,green 是自我實現的。分離 implementer 與 orchestrator,讓 acceptance test 在實作存在前由不同 context 鎖定——hash 鎖定驗收測試、dispatch 前後 bit-identical 驗證(I4,在 level-1 執行)。這是整個家族存在的原因。在 task loop 裡,高於 lite 的 tier 同樣不可讓步;**lite 的 solo 模式是入口 tier 的已知 trade,自 v1.20.0 起在 loop 內重新可用**(補償 = 強制 fresh-context review dispatch——迴圈經濟學定調:小卡不付雙 context 稅);**level-1 若無法派 nested dispatch(lite 的 review dispatch 也算),唯一合法的行為是停下回報,不得退化成無 review 的 self-testing。**

## When to Use

- 一個 feature phase 拆成多個 task(通常 5+),每 task 一份自足 doc,逐 task 開發、逐 task commit。
- 預期跨越多個 session、context 會被壓縮或中斷 → 需要狀態區 + 半成品續作模式。
- 有權威計畫文件(single source of truth:需求 + 決定區 + 任務總表狀態區)。
- 進場時只有需求結論或 plan/blueprint,還沒拆成任務總表 + task docs → 先走 Phase 0(總表是續作 / 回滾 / 回寫的 trace base)。
- 上游依賴(外部 API、別團隊 service)未定案 → mock-first 契約開發(見專節)。

**When NOT to use:**
- 單一 task / 單一 feature → 直接 `/spec-tdd-escalate`(或手動選 tier),主 session 自己當 orchestrator;外層迴圈是 overhead。
- 一次清一 batch 獨立小 bug → `spec-tdd` 的 **multi-unit run**(一個 session 內迴圈單元;邊界在單元,不涉及 per-task commit 與跨 session 狀態)。
- 時間敏感且 DAG 有真實可平行結構(非鏈)→ `spec-tdd-task-dag`(平行 overlay;本 skill 仍是序列/429 保守模式)。
- 探索性 / 拋棄式程式碼 → 不需要任何 skill。

## Phase 0 — 任務拆解(進場時總表未拆)

進場時若只有需求結論或 plan/blueprint,**還沒拆成任務總表 + 自足 task docs** → 先做本節,產出控制文件後才進 Pre-flight。三件套已在 → 跳過。理由:狀態區是斷點續作的 trace base、task 邊界是回滾單位、決定區是決策回寫的家——**拆解只在對話裡 = 沒拆**(I17 精神),沒落檔,續作 / 回滾 / 回寫全部無所依附。

1. **結算檢查(I20 sniff)。** 掃需求決策缺口(未綁數量、二選一未選、TODO/TBD):有缺口 → 轉 grill 前端補談,不在本節補洞;乾淨 → 續行。
2. **拆解(頂層執筆 — I19(a):planning 不下沉)。** 頂層讀需求結論 / blueprint + 盤 codebase 錨點(可派 read-only Explore 代跑偵察),產出:(a) 權威計畫文件三件套(Pre-flight 5 格式)——需求本文、決定區(討論既有決定沉澱為 D1… 續接編號)、任務總表狀態區(全部 pending);(b) 每 task 一份自足 doc(Pre-flight 6 欄位)。粒度原則:**一個 task 一件事**——task 邊界 = commit 邊界 = 回滾單位,拆錯顆粒 = 回滾單位變形。**Critical-surface sniff(預設開)**:拆解時以 stakes 謂詞掃全部 task 概念,adversarial 級的 task 在開跑前**拉出 loop**(總表標 pulled/external,standalone 跑;commit 照常落 task 邊界、gate 照常驗回報證據)——靜默降級沒有同意來源,雙重付費(coverage 跑一遍+standalone 再跑一遍)正是要消除的浪費。**預算尺寸可行性**:每 task 的 wall-clock 預算必須大於其驗證計畫的總 build 時間(計畫 run 數 × 全套時長),做不到 → 拆 task 或上調預算(見 watchdog 段)。
3. **Fresh-context plan review(獨立 sub-agent,TOP)。** 派一個未參與撰寫的 sub-agent 攻擊這份計畫:需求覆蓋率(每條需求都有 task 接)、漏 task、依賴順序、task-doc 自足性(契約欄位缺漏)、粒度變形(一個 task 塞多件事 / 切得無謂地細)。Findings → 頂層修 → **同一 reviewer 複審**(bounded:audit + 一次 re-audit,I16 慣例)。
4. **雙同意 gate。** Reviewer 收斂(無 finding)+ 頂層核定 → 進 Pre-flight;任務總表隨 Pre-flight 既有 asks 一併露出(非另設 gate)。Re-audit 後仍有 unresolved finding → 升交 user 拍板,不得帶著未收斂的拆解開跑。

## Pre-flight

1. **Orchestrator tier check(I21)。** Before any work, check the model THIS session runs as. A run's judgment executes entirely in the orchestrator's own context; I19 pins every dispatch tier, but nothing can upgrade the session itself. **Top tier in use, or no higher tier exists → silent, move on.** Otherwise surface this ONE ask and stop for the answer:

   > ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

   本 skill 的 gate 雖輕,但 level-1 dispatch 必須 TOP(它承接全部 planning / 驗證判斷)——頂層 session 本身若跑中階,整個 phase 的 routing 與覆核判斷都跟著壓在中階上。
2. **Session commit 授權(開跑前問一次)。** Task 邊界 = commit 邊界是本 skill 的回滾設計,但 commit 權限始終是 user 的——loop 開跑前明確問一次:「本 session 授權頂層在每個 task 邊界 commit 嗎?」**授權** → gate 通過後頂層直接 commit(仍明確列檔名;push 不在此授權內)。**未授權** → 不省略邊界:每個 task 邊界暫停,列出該 commit 的檔案清單交 user 手動執行,狀態區補 user 回報的 hash——回滾單位不變,執行者換人而已。
3. **Tier band(結構性,非政策、非 ask)。** 迴圈內 tier 帶 = **lite … coverage**:escalate 路由在帶內照常跑(含 lite——小卡的 solo+fresh-review 形狀,v1.18.1 的 loop 內 lite 禁令自 v1.20.0 反轉:小卡不付雙 context 稅)。**Adversarial 結構性不承載**:小時級深度 × 逐卡相乘與迴圈牆鐘經濟學矛盾(「要避免空轉。這功能比人做還慢」)。Critical 單元的收斂點是**逃生口**——Phase 0 sniff 預拉;level-1 路由點發現(實作前)→ STOP 回報、頂層拉出,**不默默 coverage**;經 user 明示留在 loop 內跑 coverage 的 → 揭露 + 殘餘風險清單(**回補 = 拉出 standalone,不是 board re-test row**)。User 中途要對某 critical task 上 adversarial → 一樣拉出,不存在 in-loop 解禁。
4. **Nested spawn depth check。** 預設 spawn 深度限制會讓 level-1 sub-agent 沒有 Agent tool → 無法派 level-2。修法:環境變數 **`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3`**,設在頂層 session 的啟動環境(harness 讀得到的位置——settings 的 env 區塊或啟動時的 shell 環境;在某次 Bash call 裡 export 影響不了 spawn sub-agent 的上層)。驗證法:dispatch template 內建「若你沒有 Agent tool,立刻 STOP 回報」——第一個 task 它回報有 tool,設定即生效。
5. **權威文件就位。** Phase 開始前確認三件套存在:(a) 需求本文;(b) **決定區**——編號決定(如 D1、D2…),新決定**續接編號**,不改號不重編;(c) **任務總表狀態區**——每 task 一列:id + 白話名稱 + 狀態(pending / in-flight / done + commit hash)+ 一行證據指向。不存在 → 回 Phase 0 產出,不得即興開跑(拿 blueprint 直接當計畫、口頭拆一拆就跑,都是即興)。
6. **Task-doc 自足性檢查。** 每個 task 一份自足 doc——sub-agent 不翻其他文件就能做。必要欄位:
   - 目標與範圍(含明確的**非目標**);
   - 現況錨點:file:line(行號會 drift,同時給 method/symbol 名當錨);
   - 設計要點;
   - **完整外部契約一次給全**——DDL 全文、API 形狀、介面簽名;禁寫「同前案」「見需求文件」;
   - **交付檔案清單**——本 task 將產出 / 修改的檔案;純文件 task 必填且 exhaustive(輕量 gate 第 5 項的核對輸入);
   - 驗收標準(可轉成 acceptance test 的行為描述);
   - 風險與回滾。

## The loop(每 task 一輪)

1. **選 task + 驗錨點。** 依總表依賴順序取下一個;前一個 task 落地後 file:line 會漂移——快速驗 doc 錨點仍準,不準先修 doc(以 method 名重錨)。狀態區標 in-flight。
2. **Dispatch level-1(TOP)。** 用下面的 template。doc 內的路徑縮寫必須在 prompt 裡**還原為絕對路徑**(sub-agent 的 cwd 不可依賴);template 的 `{family root}` 亦同——填 skill family 安裝位置的絕對路徑。Dispatch 時刻與交付類別記入狀態區 in-flight 列(watchdog 的武裝基準,見專節)。
3. **回報後跑輕量 gate**(下節)。gate 不過 → 帶**客觀證據**重派(編譯錯誤全文、清單外檔案、XML 數字落差);三 bucket routing(I10)是 level-1 內部的事,頂層只遞事實不代判。
4. **決策回寫 + 狀態區更新。** User 在 task 進行中拍板的業務決策,**即時**寫進權威文件決定區(編號續接),並更新相關 task doc 內文——舊方案劃刪除線備查,不直接刪除。決策只存在對話裡 = 沒發生(session 會被清除/壓縮)。
5. **Commit(頂層獨佔,依 pre-flight 授權)。** **明確列檔名**,嚴禁 `git add -A` / `git add .`——工作目錄必有 sub-agent 的 untracked scratch(`.spec-tdd/` 等),會被吃進 commit。**權威計畫文件本輪的更新(狀態區、決定區新決策)與 task doc 修改同一個 commit**——回滾某個 task 時,它的狀態列與決策紀錄跟著回滾,狀態區才不會宣稱一個已被還原的 task 是 done。Subject 一行。Task 邊界 = commit 邊界 = 回滾單位。狀態區補 commit hash。

### Level-1 dispatch template

```
ROLE: You are the spec-tdd orchestrator for ONE task of a multi-task phase.
Run the spec-tdd-escalate machinery for THIS task only: pick the tier by
stakes, write the acceptance test (RED, RED-purity checked), dispatch a
NESTED implementer via the Agent tool, and verify it yourself (re-run GREEN,
hash check, tier-required verification). Invoke the /spec-tdd-escalate skill
BY NAME if it is available in your runtime. If it is not, do NOT improvise
a lighter version from this prompt — read FAMILY FILES below and run that
machinery exactly. You are level-1; your implementer is level-2 (MID-tier
dispatch, I19).

No self-testing OUTSIDE the lite tier. Same-context test+implementation is
circular reasoning: the implementer's blind spots enter both the code and
the test, and green becomes self-fulfilling — which is why every tier above
lite dispatches a separate implementer, and why lite (the entry tier for
small non-critical units) compensates with a MANDATORY fresh-context review
dispatch over its test+implementation. If your escalate routing selects
lite, run the lite machinery exactly, including that review dispatch. If
you have no Agent tool, STOP and report that fact — do NOT fall back to
implementing yourself (the review dispatch needs the tool too).

TASK DOC: {absolute path} — READ IT FIRST; it is self-contained (goal,
scope, current-state anchors, design notes, full contract incl. DDL,
acceptance criteria, risks, rollback). Doc path shorthand maps to:
{abbreviation → absolute path}.

FAMILY FILES (if the skill is not invocable in your runtime, READ these
from disk and follow them — the machinery lives there, not in this prompt):
{family root}/skills/spec-tdd-escalate/SKILL.md (the routing you run),
{family root}/skills/PROTOCOL.md (invariants I1–I21), and the chosen
tier's {family root}/skills/<tier-name>/SKILL.md.

DOC EDITS: report proposed task-doc / plan-doc changes; do not edit the
authoritative plan doc yourself — the top-level session owns decision
writeback.

SCOPE: this task only. Prior tasks' acceptance tests are the regression
wall: adapt one only where this task's contract evolution forces it — one
file at a time, assertion SEMANTICS unchanged, each adaptation listed in
your report with its rationale.

GIT: NO git write operations (add/commit/stash/checkout/restore/...). The
top-level session owns all commits. Read-only git (status/diff/hash-object)
is fine.

TIER BAND: lite … coverage — the loop's structural band. Your escalate
routing runs UNCHANGED inside it, including lite (small non-critical
tasks: solo author-implementer plus ONE fresh-context review dispatch —
the lite machinery's own shape; disclose the tier used). The CEILING is
structural: adversarial is not carried inside the loop (hours-level depth
× per-task multiplication contradicts its wall-clock economics). A task
whose stakes would route above coverage: STOP and report BEFORE
implementing — the top's default is to pull it OUT of the loop and run it
standalone (double-pay — coverage here PLUS a standalone run later — is
exactly the waste this band exists to kill); running it AT coverage
in-loop requires the user's explicit call at that task boundary and rides
the phase report's residual list. (Pure-docs tasks excepted — no
acceptance test to write, the tier machinery does not apply; see the
loop's gate item 5.)

MOCK PHASE: {yes/no}. If yes: the contract target is the mock established
by task {id}; reduced verification depth is user-approved for mock-phase
tasks; disclose the tier actually used.

PHASE BOUNDARIES (before/after each nested dispatch, when ENTERING a wait
on a nested dispatch, after each completed long tool run, after each
delivered file): 1) touch `.spec-tdd/<task>/HEARTBEAT` (create the
directory if missing; touch or an equivalent write) — when the touch
coincides with entering a wait, write into the file: "waiting: <child-id>
expected-done <time>"; 2) re-read `.spec-tdd/POLICY-<task>.md` — an ABSENT
file means no policy (not an error); a PRESENT file overrides TIER BAND
above, DOWNGRADE-ONLY (raising waits for the next task boundary).

NESTED DISPATCHES (every tier above lite): dispatch your implementer in
BACKGROUND mode — a blocking Agent call makes you unreachable and
unmonitorable, and its never returning is NOT evidence the child lives (a
child's death is silent to you). Record the expected duration with each
dispatch (floor it at the known build cost of the affected files); on
overtime with no fresh output from the child (worktree / build outputs),
treat the child as dead: TaskStop it first (a presumed death is not a
confirmed one — two implementers must never write the same tree; clear
build-process locks, e.g. stale daemons, before re-dispatching), then
dispatch a continuation implementer on its partial work. Harness without
background nested dispatch: disclose the degradation (the top's budget
backstops).

VERIFICATION REPORTING (your numbers will be independently rechecked):
  - FINAL verification = ONE gradle run covering ALL related test classes —
    each run CLOBBERS the previous JUnit XML, so only the last run survives
    for recheck.
  - Report per-class numbers read from build/test-results/test/*.xml, and
    state whether counts are @Test METHODS or EXECUTED INVOCATIONS
    (@ParameterizedTest: 1 method = N invocations).

RETURN: 1) one status line per command (command + pass/fail counts), full
logs to scratch files under .spec-tdd/ (never committed; hand paths)
 2) per-class numbers  3) created/modified file list (absolute paths)
 4) disclosures: tier actually used (+ any mid-run downgrade or band
cap), deviations from the task doc (DDL deltas, mock placement,
naming/structure), locally decided rule details  5) prior-test adaptations
with per-file rationale.
```

## In-flight 監視(anti-idle watchdog)

429 額度耗盡與死亡靜默疊加,一張卡可以燒掉整個下午。**三種失敗模式**:hard-fail(429 直接終止、有通知——既有續作規則覆蓋)、soft-wedge(推理退避迴圈:恆 `running`、零通知、transcript 停更,外部零訊號)、zombie-wait(nested child 已靜默死亡,parent 健康地等一個永不返回的 Agent 呼叫——**Agent 呼叫不返回 ≠ child 活著**)。實戰:三模式疊加,一張卡 ~6 小時、~5 小時零產出——比人做還慢。**定調:零產出時長是第一級指標,「避免空轉」是根本要求,不是 nice-to-have**;同樹 code task 序列,一張卡空轉 = 整條佇列停擺(task-dag 下卡的是波末 merge,兄弟照跑——仍然正當,理由不同)。**這是製程監視不是驗證動作**:訊號全是客觀事實,無內容判讀。

1. **武裝(dispatch 當下,登記交付類別)。** 頂層擁有的每個背景 dispatch——每張卡的 level-1、Phase 0 plan-review、收盤批次審查——派出時:dispatch 時刻與**交付類別**記進狀態區 in-flight 列(board 是檔案,session 中斷後可重新武裝),並以 harness 的一次性喚醒機制排第一個檢查點(task-dag:一次喚醒服務全部 in-flight,不逐卡排)。**兩層都是背景 dispatch**(頂層→level-1、level-1→nested):blocking 呼叫讓 parent 不可達不可監視——中途變向、POLICY 重讀、watchdog 全部依賴 parent 保有 tool round。**交付類別**:(i) **產出型**(code task)——實質產出 = 工作樹 diff、test-results 變化、agent 刻意寫入的 task scratch(報告 / ledger;harness 的背景 task 檔與 transcript 不算);(ii) **唯讀型**(plan-review、收盤審查)——零樹產出、零 build 是 by design,實質產出 = heartbeat / scratch 報告的成長;套產出型公式對它們必然誤判。
2. **兩軸與節奏。** **實質產出年齡**(自上次實質產出以來的時長)與 **wall-clock 預算**(tier 推導的示例預設:lite 30 / spec-tdd 60 / coverage 120 分——環境校準值,user 可調;唯讀型的預算 = 派出時明訂的預期時長)。檢查點每 15 分(示例預設)一個一次性喚醒,事件驅動 re-arm(檢查後排下一個,收案即解除——不是無腦輪詢;×N 平行下這個經濟更重要)。**agent 自陳狀態永遠不解除實質產出時鐘**(實戰:zombie parent 回報「實作者在跑」被證明是錯的——回應內容不是健康證據)。
3. **三態判定(綁時鐘,各別容忍度)。** (a) **zombie-wait**——四條件合取才確診:有活動跡象(heartbeat 新鮮或背景檔在冒;背景檔的所有權對照 heartbeat 內容判斷——可能是 children 的輸出也可能是 parent 的 probe 殘跡)、零實質產出、build **輸出未在推進**(輸出目錄 mtime 滾動為主訊號,進程存在僅輔證——閒置常駐 daemon 如 gradle daemon 預設空閒存活數小時,存在 ≠ 活躍)、且 heartbeat 宣告的等待已逾期(waiting 的 expected-done 已過)。高置信死亡,**15 分快刀**;(b) **全面凍結**——heartbeat / 背景檔 / build 輸出全凍:歧義狀態(單一長推理與 soft-wedge 外部不可區分),**長容忍 ~90 分**(示例預設,user 可調),預算兜底;(c) **合法工作**——實質產出在流動或 build 輸出在推進 → 重新武裝。**瞬時訊號形狀區分不了 zombie 與健康的 in-phase 等待**(等 encoding audit 的健康 parent 四條件前三項全中)——逾期時鐘是唯一鑑別器,這是三態與 nested 時限一體設計的原因。
4. **預算 = 硬上限(三規則)。** 超過 → 終止重派,**沒有「再等等」**。但:(i) **流動中的一次性重設**——超支當口實質產出在流動 → 一次性重設預算並揭露(尺寸估錯是計畫缺陷不是 agent 缺陷;只准一次,防無限展延);停滯 → 立即終止;(ii) **續作重派重置預算**——按盤點後的剩餘範圍重給(繼承已燒穿的預算 = 秒殺);(iii) **Phase 0 尺寸可行性**——預算必須大於該 task 驗證計畫的總 build 時間,做不到 → 拆 task 或上調預算(Phase 0 已載)。**重派上限 2 次**(I9 形狀的 circuit breaker),超過升交 user。
5. **確診 → 對應恢復(429 段)。** zombie → 復活嘗試起手;全面凍結 → soft-wedge 程序;已知重置時刻(session 內任一 429 訊息載明)→ 加排 reset+15 分保險點。**降級階梯(誠實版)**:無排程機制 → watchdog 退化為 board 預算紀錄 + 自然控制點 best-effort 檢查 + 揭露;**唯當重派也不可得**(池全面死盡 / harness 壞)→ 「頂層親跑最終驗證」的降級收尾(見 429 段)——最後一階,不是便利捷徑。

## 輕量 gate(頂層唯一的驗證動作)

Level-1 回報後、commit 前,頂層親自:

1. **編譯** — 主 module 的 `compileJava` + `compileTestJava` 親跑一次(例:`./gradlew :Core:compileJava :Core:compileTestJava`),綠才算數。
2. **檔案範圍** — `git diff --stat` + `git status --porcelain`,對照 level-1 回報的 created/modified 清單;出現清單外的改動 = 先盤點(level-1 說明或回退)再 commit。Untracked scratch 目錄除外。
3. **數字複核** — 讀 JUnit XML(`build/test-results/test/*.xml`)對 level-1 回報的逐類數字(見下節)。
4. **hash 抽查** — level-1 應回報 acceptance test 的 dispatch 前 / 後 hash(bit-identical,I4);頂層比對字串相等即可。
5. **純文件 task 的 gate 與 dispatch 同步縮形。** **純文件 = task doc 明載、且 diff 僅含文件類交付檔案**(契約文件、usecase map、說明)——含任何 production / test code 或 config 變更即非純文件,整 task 回一般 gate(1–4 項全跑);分類在 Phase 0 / task doc 宣告,gate 以 `diff --stat` 對照**交付檔案清單**驗證,不由事後認定。Gate:無測試數字可複核——數字項以路徑級核對取代(清單所列檔案逐項存在、範圍吻合);**交付物內容品質不入頂層 gate**(內容判讀下沉原則,見 429 段)。Dispatch 同步縮形:template 的 acceptance test / hash / gradle 數字回報項整組以「交付檔案清單 + 逐檔交付」取代——無測試可寫即無循環推理顧慮,tier 機械(含 spec-tdd 下限)不適用;文件由 level-1 執筆(或派 level-2),編譯項照跑防夾帶 code 變更,hash / 數字項自然空集。PHASE BOUNDARIES 指令照帶——純文件 task 可能零 nested dispatch,heartbeat 靠「每交付一份檔案」的觸發點覆蓋。內容**正確性**由產出的 level-1 對照上游出處自證並於報告揭露;消費 task 的契約測試與 plan review 把關的是**接線與覆蓋**,不是文件本身的真偽。

**不做的**:深度 code review(下沉給 level-1 的 audit / 攻擊輪;跨 task 深審另由收盤批次審查承接,見專節)、親自跑測試(level-1 已跑,XML 在)、重跑全套(gate 失敗需要診斷時例外)。頂層做主觀審查不是勤快,是浪費:它沒有 level-1 的 full context,結論不會比 sub-agent 的 audit 輪好,卻燒掉最稀缺的 context。頂層的價值在**客觀性與連續性**,不在深度。

## 數字複核紀律

- **規則:sub-agent 回報的測試數字一律讀 JUnit XML 複核,不採信口頭。** 實測兩次踩到口頭數字錯:一次回報 165、XML 實為 163;一次回報「+6 個新測試(21+6=27)」、XML 實為 30。
- **計數單位陷阱** — `@ParameterizedTest` 一個方法 = N 個 invocation,JUnit XML 的 tests 計的是 invocation。上述 30 的案例:實際 +7 個方法(6 個 `@Test` + 1 個 `@ParameterizedTest` 跑 3 組)= +9 個執行單位——回報者以方法數口算,行為無矛盾,純計數筆誤。複核對不上時先問:**回報的單位是 method 還是 invocation?**
- **XML 覆蓋陷阱 — 每個 test run 會清掉前一輪的 XML。** level-1 跑多批測試時,事後只有最後一批可複核。對策已寫進 dispatch template:**最終驗證 = 一次涵蓋全部相關 test class 的單一 gradle run + 逐類列數字**——這一輪的 XML 就是頂層複核的對象。

## Mock-first 契約開發(tier 選擇的時間維度)

上游依賴未釋出 / 未定案時:

1. **第一個 task 先做 mock**(mock controller / server),把契約定下來;後續所有 task 對 mock 開發,不空轉等待。
2. **Mock-first 階段的 tier 可以降(user 拍板)。** 對 mock 的程式碼,在契約定案前過度投資 verification 是浪費——契約一變,深測跟著重寫。Tier 不只按 blast radius(空間維度)選,也按**這份 code 的壽命階段**(時間維度)選。
3. **真實依賴確定後,排一個契約對齊 task** — 回頭比對真實 API vs mock 契約、修正偏差、補上 mock 期省下的深測。降級必須是「暫緩 + 回補」,不是「省略」;全程揭露。
4. **外部未決題在計畫文件記落地點(與決定區分流)。** 決定區記 user 拍板;等第三方答案的題(上游 API 行為、別團隊回覆)在**權威計畫文件內**另立一節(落在 scratch / 對話 = 沒發生),每題一行:**問題 + 權宜落地點(哪個 task 用什麼權宜、單一替換點在哪)+ 答案到手收斂哪裡**。**答案到手 → 回寫決定區(編號續接,註記來源為外部),該行劃記已收斂**,由契約對齊 task 消化——答案到達有明確收斂點不散失,對齊 task 有現成消化清單(實戰:STP2 G 清單——「錯誤碼真實值未決→W6 分類器單一替換點已建,答案到手改一處」)。

## 中途變向(tier 降級送達在跑的 sub-agent)

User 任何時刻可因時間壓力降 tier——包括 task 進行中:

- **送達(雙通道)** — level-1 在背景跑時,用 SendMessage 把變更送進去(例:「降級到 spec-tdd,收斂到綠即收工,報告揭露 tier 變更」)——對醒著的 agent 最即時;**同時寫進 `.spec-tdd/POLICY-<task>.md`**(level-1 於每個 phase 邊界重讀,template 邊界指令)。檔案通道的三個理由:積壓訊息**延遲送達非丟失**(實測:wedge 甦醒的第一輪才按序補送——時效性強的指令晚數小時 = 沒送);重派的 fresh 續作 agent **冷啟動**沒有訊息積壓可收,只有檔案可讀;政策留在訊息佇列裡 = 還沒落地。POLICY 檔覆寫 template 的 TIER BAND,**只降不升**(升回應得 tier 走下一個 task 邊界);落點在 scratch,不進 task doc——task doc 修改與 commit 同捆,作戰政策寫進契約會汙染回滾單位或觸發 gate 檔案範圍核對。
- **資產保留** — 已完成的測試與實作不丟棄;收斂到綠就收工。
- **揭露** — 該 task 的報告必須載明 tier 變更(何時、降了什麼、留下什麼未驗風險)。
- 送不進去(非背景 dispatch)→ 於下一個 task 邊界生效,同樣揭露。
- **Band 內降級** — 中途要降 tier(如 coverage→spec-tdd)同路處理:SendMessage+POLICY 檔送達,否則下一個 task 邊界生效,揭露同前。升回應得 tier 只於下一個 task 邊界(升級不走 mid-run 通道);band 上限是結構性的,不存在「升出 coverage」。
- **時間壓力的降級產生 re-test 債。** **任何因時間壓力的 runtime 降級——中途調降 tier(如 coverage→spec-tdd),或逐 task SendMessage 降級——一視同仁記債:低於應得 tier 通過的 task 進 re-test debt 清單**(board 記錄;stakes 本就低於新 ceiling、未受降級影響的 task 不記——稀釋清單 = 清單失效),並進 phase 報告揭露。回補(re-test)是正式入口,不是可選:**時間允許時直接排回本 phase 總表**(新增 task 列續接);phase 收盤仍未回補 → 清單全量列入 phase 報告移交 user。沒記帳,輕量首過會靜默變永久;沒移交,記帳也會。Pre-flight 的 tier band 上限是結構性的(pre-flight 3),capped-critical(經 user 明示留在 loop 內跑 coverage 者)進殘餘風險清單,回補 = 拉出 standalone,不重複記債。這是 mock-first「暫緩+回補,不是省略」的 phase 級版(實戰:STP2「W11–W14 全以輕量通過=re-test 對象」)。

## 半成品續作(session 中斷後)

Session 中斷 / context 損毀,task 停在半途:

1. **先盤點,不重寫** — `git status` + 既有 diff 對照 task doc,以路徑對照判讀哪些是合理半成品(內容級判讀下沉——見 429 段原則)。
2. **spec-defect 檢查** — 中斷前留下的測試若與 task doc 矛盾 → **修測試,不扭曲 production**(I15 的精神:production 為遷就缺陷測試而彎 = 失敗的 run)。
3. **續作 brief** — 重派 level-1(若前手有留 ledger / scratch log,一併交出)時明確指示:**保留既有合理改動、只補缺口、不重寫**,並附上盤點結果(diff 檔案清單 + 範圍對照——哪些 diff 屬本 task 範圍,路徑級)。
4. 狀態區就是恢復點 — in-flight 的 task 直接可見(呼應 A16 的 resume 語意:在飛中的 row = re-verify,不盲目重做)。

**API 限額中斷(429)——agent 死了、session 還活著,與上述 session 遺失不同:** 額度重置 / 換 key 後**用 SendMessage 續同一個 agent**(保留完整 context),不重派新 agent 重來。斷點性質照步驟 1 盤點:acceptance test 已寫、production 零改動 = 乾淨 RED 斷點,恢復零風險;production 已有部分改動 → 先驗 acceptance test 的 I4 hash 未被動過。掛掉的若是 nested implementer 而非 level-1:orchestrator 恢復後**重派一個續作 implementer,在前身的半成品上修正完成**(同「保留、只補缺口、不重寫」,下沉一層)。resume 訊息講明現況(working tree 已有哪些檔、斷在哪一步),不讓 agent 重建認知。

**Soft-wedge 與 zombie-wait——第二、三種斷點,watchdog 確診後走此程序:**

1. **Zombie-wait 先走復活嘗試(便宜路,跳過 nudge)。** 帶證據 SendMessage:「你的 child 已死(test-results 凍結於 X、build 輸出未推進、零活躍進程),停止等待,重派續作 implementer」+ 一個有界 grace(一個檢查週期,不是等回覆)——活著的 parent 可就地自救,保住完整 context 省 冷啟動 + 重盤點。Parent 有**動作**(新 child 派出 / heartbeat 恢復邊界 touch)→ 重新武裝;它的**口頭回報不算**(自陳不解除實質產出時鐘);grace 過了沒動作 → 共同手術。
2. **Soft-wedge:已知重置時刻** → 排 reset+15 分的 nudge(SendMessage 喚醒+收斂指示);甦醒寬限 ≈10–15 分(實測子先母後——n=1 緩衝值,非精律)。**重置時刻未知**(純 soft-wedge、session 內無任何 429 訊息)→ 立即 nudge(送不進也不花成本)+ 一個 grace 週期;仍凍結 → 共同手術,或按派工紀律換池重派——不無界等待。
3. **共同手術(soft-wedge 確診 / zombie 復活失敗)。** (a) **kill 前先 SendMessage**——被殺瞬間積壓訊息送達(最後遺言):免費拿到它的自我狀態認知(可能是錯的,但診斷價值在——實戰:最後遺言坐實了錯誤認知);(b) TaskStop 殺 parent;(c) **孤兒清掃**:以 agent 清單找出在飛的 nested children,一併停掉或確認已結束(獨立進程,可能仍在寫同一棵樹——孤兒與新 level-2 相撞),清掃延伸到 **build 進程鎖**(殘留 daemon 鎖檔會撞新 agent 的 build,Windows 尤甚);(d) 重派 fresh 續作 level-1——**優先不同池且滿足 tier 釘選的模型**(I19(a):換池不得降 tier;無 → 同池,預算按剩餘範圍重給),brief 照續作模式(盤點 git status + task doc + acceptance tests,保留、只補缺口、不重寫)+ **先讀 POLICY 檔**(冷啟動的政策來源);(e) 機械收尾仍是 dispatched agent 的事。
4. **降級收尾(最後一階)。** 唯當重派也不可得(池全面死盡 / harness 壞)→ 收尾模式降級為「**頂層親跑單一合併驗證 run**」——性質是 gate 例外(同 task-dag 波末聯集 run 的形狀:新資訊、無既有 XML 可複核、證據 = run 的 XML 數字),**不是**授權頂層收卡(機械修完仍是 agent 的事——本路通常已無 agent 可派,頂層只驗證既有產出的可收性);report 揭露。(Description 的 "never running the tests itself" 自此帶著已知例外在跑——比照 task-dag 先例,body-level 處理,routing 未動。)
5. **甦醒 ≠ 結束。** 甦醒的第一輪會按序補送**全部**積壓訊息——包括數小時前拍的舊政策;頂層隨即補一則確認 / 撤回,不讓過時指令繼續生效。且醒來也只是開始消化積壓(nested 結果、訊息、收斂),距最終回報還有距離。
6. **凍結的是 nested child(parent 活著)** → 既有規則:停掉該 child,重派續作 implementer,下沉一層(TaskStop 先於重派——推定死亡 ≠ 死亡)。

**首見 429 後的派工紀律:** session 內任一 agent 出現 429(訊息載明池與重置時刻)→ 後續 dispatch **不得靜默落在該池**:已知**不同池且滿足 tier 釘選**的模型可指名 override(opt-in),否則停派至載明的重置時刻。明文化,不靠臨場判斷——耗盡期間他池照常開工是實證有效的。

**不等重置的合法路:重派「續作」agent(不重來)。** 剩餘工作小、等限額重置不划算時(實戰:3.5 小時),重派一個 fresh agent 在前身的半成品上收尾——keep-don't-rewrite brief + **指標不帶內容**:前任 scratch log、diff 檔案清單、死點描述;**交付物的內容級判讀(讀全文判完整性/品質)一律下沉,由續作 agent 自己做**——此原則通用,不分 429 / session 遺失。**硬禁第三條路:頂層自作主張親手收尾**——「剩很少」「純文件」「我 session 未受 429 影響」都不構成例外(實戰 incident:429 死在交付物 2 開頭,頂層開始讀 560 行契約文件驗屍,被 user 叫停——頂層每讀一份交付物都是不可回滾的 context 消耗)。User 明示要求頂層親收 → 照做,以 degraded mode 揭露於 phase 報告——**禁的是頂層自作主張,不是 user 的決定權**。盤點原則:頂層只看客觀廉價事實(git status / `diff --stat` / 檔案路徑對照 task 範圍)。

## 揭露慣例(disclosure)

以下事項 sub-agent 報告**必須明列**、由頂層 / user 複審——不得默默做:

- tier 被上限(如 spawn depth 不足、tier band 上限下的 capped-critical)或中途降級;
- doc 字面偏離 — DDL additive 偏差、mock 落點與 doc 不同、命名 / 結構調整;
- 本地拍板的規則細節(doc 沒寫死、level-1 自行決定的小規則);
- 前批測試的調整(下節)。

原則:**task doc 是契約。偏離契約而未揭露 = 契約失效**——下個 task 的 sub-agent 仍按舊契約理解系統。

## 迴圈牆(測試資產)

- 每個 task 的驗收測試是下一個 task 的既有資產——phase 越後面,牆越厚。這是 task loop 的複利。
- 後續 task 因 constructor / 契約演化調整前批測試屬合理演化,但:(1) **逐檔記錄**於報告並附理由;(2) **斷言語意不得改動**——改的只能是接線(新 constructor 參數、新契約欄位),不是預期行為。改了語意 = 那面牆倒了一段,必須當成新測試重走 RED→GREEN。

## 收盤批次審查(batch review)

總表全部列 done ≠ 直接出報告——收盤有固定程序:**先派一次收盤批次審查,再出 phase 報告。** 理由:task doc 自足設計讓每個 level-1 互相看不見對方,跨 task 維度在整條鏈上無人可見(頂層被硬禁深審是對的——它沒 full context 又燒稀缺資源);這個盲區用一個一次性 fresh context 補,不靠任何人「順便看」。

1. **觸發。** 任務總表全部列 done(含 re-test debt 排回的補測列)→ 派收盤審查;審查收斂、findings 處置完 → 才產 phase 報告。User 明示跳過 → 照做,但列入 phase 報告殘餘風險清單——不靜默省略。
2. **誰審、審什麼(bounded,唯讀)。** Fresh-context **TOP** sub-agent(同 Phase 0 plan-review 的形狀),一次看整個 phase 的累積成果:全部 task 的 commit 範圍(首..末 hash)、task docs、權威計畫文件(狀態區/決定區/外部未決題)、揭露清單(由頂層彙總交付——reviewer 不重讀交付物)。唯讀:git read + 讀檔;不改 code、不跑 build、不動 git。
3. **四個攻擊維度(跨 task 才看得到的)。** (a) 跨 task 不一致——同一概念多種實作形狀(金額處理、錯誤處理風格、命名);(b) 重複邏輯沒抽出——跨 task 邊界的多份相似 copy,日後改一處漏一處;(c) 迴圈牆調整的累積效應——逐次合法的接線調整,合起來牆薄了一段;(d) 揭露的合併模式——多筆本地拍板合起來與決定區矛盾(單筆都合理)。
4. **Findings 處置(自動進板)。** 每筆 finding 編號(F1、F2…)→ **自動開總表新 task row**(續接編號、來源註明「收盤審查 F#」),走正常迴圈——tier 機械照判、輕量 gate、per-task commit。頂層判為非缺陷的 finding **不得靜默丟棄**:總表劃刪除線 + 一行理由(同決策備查慣例)。Findings 是缺陷帳,與 re-test debt(tier 降級帳)分開記,不合併。
5. **收斂 bound(I16 慣例)。** Fix rows 全部 done → **同一 reviewer 補一輪收斂審查**,範圍限 fix rows 的 diff;仍有 unresolved finding → 升交 user 拍板,不無限循環。無 findings → 免補輪,直接出報告。
6. **它是加法,不是替代。** Per-task 輕量 gate 與 tier 機械照舊——收盤審查不接手任何單 task 驗證(consolidated 視角抓不到單 task 內的洞);也不改頂層深審禁令——審查是派的 dispatch,頂層只做 findings triage 與劃記。審查 dispatch 撞 429 → 適用既有續作規則(SendMessage 續同一 agent);soft-wedge 確診後 TaskStop 重派的是 **fresh reviewer**——「同一 reviewer 補一輪」不可得,此重派成本在報告揭露。收盤審查也在 watchdog 的監視範圍(唯讀型:預算 = 派出時明訂的預期時長,訊號 = heartbeat)。
7. **成本與揭露。** +1 TOP dispatch/phase(有 findings 才有補輪,上限 +1)。審查輪數、findings 數、開了幾個 fix row、劃掉幾筆(附理由)全部進 phase 報告。

## LSP / IDE 診斷不是證據

子代理寫檔後,LSP / jdtls 常報過期假錯——「method undefined」「cannot be resolved」,甚至指向已刪除的 scratch 檔。**一律以 gradle compile / test 結果為準**(I19(f):the BUILD is the only oracle — IDE diagnostics are noise)。任何層級都不要把時間花在追 LSP 錯誤上。

## Common Mistakes

| Mistake | Fix |
|---|---|
| 拿 blueprint 直接當權威計畫文件開跑(沒狀態區、task docs 不自足) | Phase 0 先行:進場判三件套在不在,不在 → 拆解 bootstrap 產出,才進 Pre-flight。 |
| 口頭在對話裡拆 task 就開跑 | 拆解只在對話裡 = 沒拆(I17 精神):session 壓縮後 trace base 消失,續作 / 回滾 / 回寫無所依附。落檔三件套 + 自足 task docs。 |
| 拆解未經 fresh-context review 就開跑 | Reviewer 攻擊覆蓋率 / 漏項 / 順序 / 自足性 / 粒度 + 頂層核定(雙同意)是 bootstrap 的一半;錯拆的成本是整個 phase;unresolved → 升交 user。 |
| 頂層親自深度 code review、親自跑測試 | 輕量 gate only:compile、`diff --stat`、XML 數字複核。深度審查下沉給 level-1 的 audit / 攻擊輪,跨 task 深審下沉給收盤批次審查;頂層 context 是整個 phase 最稀缺的資源。 |
| level-1 沒有 Agent tool,於是自己實作(self-testing) | 硬禁——停下回報 user;修法是 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3`(設在頂層啟動環境,不是某次 Bash call 的 export)。 |
| 採信 sub-agent 的口頭測試數字 | 讀 JUnit XML 逐類複核(實測:回報 165 實為 163;回報 21+6、XML 30)。 |
| 數字對不上就當行為異常 | 先問計數單位:`@ParameterizedTest` 1 方法 = N invocations,XML 計 invocations;單位換算後仍不符才是異常。 |
| level-1 跑多批測試,前批 XML 被清掉無法複核 | Dispatch template 明定:最終驗證 = 單一 run 涵蓋全部相關 test class + 逐類數字。 |
| `git add -A` / `git add .` 收 commit | 明確列檔名——工作目錄必有 `.spec-tdd/` 等 untracked scratch,會被吃進 commit。 |
| 頂層沒問就在 task 邊界自己 commit | Pre-flight 問一次 session commit 授權;未授權 → 邊界暫停、列檔案清單交 user 手動 commit,狀態區補回報的 hash。 |
| sub-agent 自己 commit / stash / checkout | 全層禁止 git 寫入;commit 是頂層獨佔職責(task 邊界 = commit 邊界 = 回滾單位)。 |
| user 拍板的決策只留在對話裡 | 即時回寫權威文件決定區(編號續接)+ 相關 task doc(舊方案劃刪除線備查)。對話會被清除 / 壓縮——沒回寫 = 沒發生。 |
| Session 中斷後把半成品整個重寫 | 續作模式:盤點既有 diff vs task doc → spec-defect 檢查(測試與 doc 矛盾 → 修測試)→ 保留合理改動、只補缺口。429 中斷(agent 死、session 活):SendMessage 續同一 agent,或立即重派續作 agent(不重來);死的是 implementer → 重派續作 implementer,不清空重做。 |
| 429 陣亡的 agent 剩餘工作小,頂層「順手」親手收尾 | 不是選項。兩條合法路:等重置 SendMessage 續同一 agent,或立即重派續作 agent(不重來)。頂層盤點只到客觀事實(status / `diff --stat` / 路徑對照);交付物內容判讀是續作 agent 的事。User 明示要求親收 → 照做,degraded mode 揭露。 |
| Mock-first 階段硬上最重 tier「求穩」 | 時間維度:契約未定案前的深測是浪費(契約一變全部重寫)。User 拍板可降;真實 API 定案後用契約對齊 task 回補。降級是暫緩+回補,不是省略。 |
| 長 task list 放任 escalate 逐 task 自判,多個 task 全上 full adversarial,phase 被攻擊輪吃掉 | Tier band 上限結構性 = coverage(pre-flight 3,非 ask);critical 單元走逃生口(Phase 0 sniff 預拉 / 路由點 STOP 回報),不默默 coverage;經 user 明示留在 loop 的 → 揭露+殘餘風險清單。 |
| 誤以為 loop 內 lite 不可用,小卡硬上 spec-tdd(雙 context 稅) | Tier band 含 lite:小卡走 lite 機械(solo 實作+**強制** fresh-context review dispatch),報告揭露 tier——v1.18.1 的 lite 禁令已由 v1.20.0 反轉(迴圈經濟學:小卡不付雙 context 稅)。 |
| 中途要降 tier,直接殺掉在跑的 sub-agent 重來 | SendMessage 送達變更;已完成資產保留,收斂到綠即收工,報告揭露。 |
| 後續 task 順手大改前批測試 | 迴圈牆規則:僅允許接線調整(契約演化必須)、逐檔記錄;斷言語意改動 = 新測試,重走 RED→GREEN。 |
| 總表 all-done 直接出 phase 報告,沒跑收盤批次審查 | 收盤程序:all-done(含補測列)→ 收盤審查 → findings 進板/劃記 → 報告。跨 task 盲區(自足設計的代價)整條鏈只有這一關看得到。 |
| 把收盤審查當 per-task 深審的替代(「有它兜底,tier 降了也行」) | 加法不是替代:consolidated 視角抓不到單 task 內的洞;tier 機械與輕量 gate 照舊,審查不接手任何單 task 驗證。 |
| 收盤審查的 findings 靜默丟棄,或只列在 phase 報告 | 進總表 row(收斂點:板上 = 會被執行)或劃刪除線附理由;只列報告 = 沒收斂點(I17 精神)。 |
| 在 loop 內放行 adversarial「求穩」 | 結構性不承載:小時級深度×逐卡相乘與 anti-idle 經濟學矛盾;critical 單元拉出迴圈 standalone 跑(逃生口,pre-flight 3)——中途要求也一樣拉出,in-loop 解禁不存在。 |
| in-flight 期間零監視,空轉靠人肉發現 | Anti-idle watchdog:dispatch 時武裝(登記交付類別)、產出年齡+預算兩軸、三態判定綁時鐘。實戰:三模式疊加一張卡 6 小時、5 小時零產出。 |
| 三態判定只看瞬時訊號(zombie 誤判健康的 in-phase 等待) | zombie 四條件含「heartbeat 宣告的等待已逾期」——瞬時形狀區分不了 zombie 與等待,時鐘是唯一鑑別器;全面凍結保留 ~90 分長容忍(長推理 vs soft-wedge 不可區分)。 |
| 把產出型公式套在唯讀 reviewer 上(必然誤判) | 交付類別武裝時登記:唯讀型的實質產出 = heartbeat/scratch 成長、預算 = 派出時明訂的預期時長,不是工作樹 diff。 |
| agent 回報「還在跑/一切正常」就解除警報 | 自陳永不解除實質產出時鐘(實戰:zombie parent 的「實作者在跑」是錯的);只有動作(新 child 派出/邊界 touch/產出流動)算數。 |
| 超過 wall-clock 預算還在「再等等」;或產出流動中硬殺 | 停滯超額 → 立即終止重派;流動中超額 → 一次性重設預算並揭露(只准一次);續作重派按剩餘範圍重給預算;重派上限 2 次,超過升交 user。 |
| nested dispatch 用 blocking 呼叫(parent 自己被堵死) | 明文背景模式:中途變向、POLICY 重讀、watchdog、 responsiveness 全依賴 parent 保有 tool round;不支援背景 nested → 揭露降級(頂層預算兜底)。 |
| 視 child 超時為已死直接重派 implementer | 先 TaskStop 舊 child(推定 ≠ 確認,兩個 implementer 禁寫同樹)+ 清 build 進程鎖,才重派續作。 |
| 中途變更只走 SendMessage | 雙通道:積壓訊息延遲補送(時效性指令晚到=沒到)、fresh 續作 agent 冷啟動無訊息可收——POLICY 檔同時寫,覆寫 band 且只降不升。 |
| 把 POLICY 寫進 task doc 開頭 | task doc 修改與 commit 同捆——作戰政策進契約汙染回滾單位,或留下觸發 gate 檔案範圍核對的髒改動;落 scratch 的 POLICY 檔。 |
| Zombie 確診直接殺 parent | 先帶證據復活嘗試(child 已死證據+停止等待指示)+有界 grace——活著的 parent 可就地自救保住 context;失敗才共同手術(kill 前先 SendMessage 拿最後遺言)。 |
| TaskStop 殺 wedged/zombie parent 後直接重派 | 先孤兒清掃(在飛 nested children 一併停掉或確認已結束)+清 build 進程鎖(殘留 daemon 撞新 build);恢復重派優先不同池**且滿足 tier 釘選**。 |
| 首見 429 後續 dispatch 仍靜默落在同池 | 派工紀律:指名不同池且滿足 tier 釘選的 model(opt-in)或停派至載明重置時刻;明文化,不靠臨場判斷。 |
| 追 LSP / jdtls 的「method undefined」假錯 | BUILD 是唯一 oracle(I19(f));以 gradle compile / test 為準。 |
| Tier 降級 / doc 偏離 / 本地拍板沒有揭露 | Disclosure 慣例:全部明列由頂層 / user 複審——doc 是契約,未揭露的偏離讓契約失效。 |
| Task doc 寫「DDL 同前案」「見需求文件」 | 自足性:完整契約一次給全;dispatch prompt 把路徑縮寫還原為絕對路徑。 |

## Red Flags — STOP

- Loop 已開跑但狀態區 / task docs 不存在 → STOP,回 Phase 0 補齊(既有成果按 diff 盤點回補狀態列)再續。
- 頂層開始逐字讀 sub-agent 交付物的全文(驗屍式內容判讀;XML 數字複核與路徑級對照除外)→ STOP——內容判讀是 sub-agent(audit 輪 / 續作 dispatch)的工作。
- level-1 回報「我自己實作了」(self-testing)→ run 作廢,重派。
- level-1 回報沒有 Agent tool → 停,回報 user 設 spawn depth;不得讓它就地 self-testing。
- XML 數字與回報不符(計數單位換算後)→ 要求解釋或重跑;不吻合不 commit。
- `git diff --stat` 出現回報清單外的改動 → 盤點並獲得說明前不 commit。
- 任何層級 sub-agent 動了 git 寫入 → 先確認樹未受損,重申紀律。
- Acceptance test 在 dispatch 前後非 bit-identical → I4 FAIL,走 tier 的 TEST bucket,即使 re-run 是 GREEN。
- 續作盤點發現中斷前的 production 改動是為了遷就與 doc 矛盾的測試 → 修測試,還原被彎曲的 production。
- Tier 被降級、doc 被偏離而報告未載明 → 視為未驗證,要求補揭露後再複審。
- 收盤審查的 finding 沒進總表、也沒劃刪除線附理由 → STOP 補程序——板上 = 收斂點;記在帳上然後不看 = 沒記。
- 頂層把 liveness 檢查延伸成內容判讀(開始讀 wedged agent 的產出判斷「做對了沒」)→ STOP——監視止於客觀事實(mtime / git status / 進程 / 狀態列),確診後走程序,不是驗屍。
- 卡已停滯超過 wall-clock 預算仍在「再等等」→ STOP——預算是硬上限,終止重派;重派已達 2 次上限 → 升交 user。
- Level-1 路由發現 stakes 超過 coverage 卻默默開工 → STOP 重派——先回報、頂層拉出 loop(standalone);in-loop 的 critical 降級需要 user 明示。
