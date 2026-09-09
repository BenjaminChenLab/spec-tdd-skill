---
name: spec-tdd-task-loop
description: Use when driving a whole MULTI-TASK feature phase — a task plan split into many self-contained task docs, run one task at a time with per-task commits, a plan-doc status board, and sessions that must survive the phase. The main session stays a LIGHTWEIGHT gate (compile + `git diff --stat` + JUnit-XML number recheck — never deep review, never running the tests itself); each task dispatches a level-1 sub-agent that runs the spec-tdd-escalate/tier machinery and itself dispatches the nested implementer (no self-testing — requires CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3). Covers mock-first contract phases (the time dimension of tier choice), mid-run tier downgrades delivered by SendMessage, and resuming a half-finished task after a session break. Triggers on task loop, task-by-task spec-tdd, multi-task orchestration, per-task commit cadence, plan status board, 多 task 迴圈.
---

# spec-tdd-task-loop

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — the front-ends (`grill-spec-tdd`, `spec-tdd-escalate`), the tiers (`spec-tdd-lite` / `spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`), and [PROTOCOL.md](../PROTOCOL.md) (I1–I21 / A1–A16). 本 skill 不新增也不放寬任何 invariant:每個 task 的執行仍由 tier 機械完整落實;這裡定義的是疊在整個家族**外層**的迴圈規則——三層分工、輕量 gate、數字複核、mock-first、續作與揭露。

## Overview

一個多 task phase:任務總表、每 task 一份自足 doc、逐 task 開發與 commit、可能跨越多個 session。**頂層 context 是整個 phase 最稀缺的資源**——唯一必須從頭活到尾的是它。所以深度工作(acceptance test 撰寫、encoding audit、實作、攻擊輪)全部下沉到可拋棄的 sub-agent context;頂層只做兩類事:

1. **跨 task 狀態管理** — 挑 task、維護權威計畫文件的狀態區與決定區、決策回寫、每 task 一個 commit。
2. **輕量 gate** — 只驗「客觀可核事實」:編譯、檔案範圍、測試數字。每項都是機器可比對的,不需要品味也不需要 level-1 的 full context。

| 層 | 是誰 | 做 | 禁止 |
|---|---|---|---|
| 頂層 orchestrator | 主 session(program conductor)| 跨 task 流程、輕量 gate、狀態區維護、決策回寫、commit | 深度 code review、親自跑測試、寫 acceptance test、實作 |
| level-1 sub-agent(**TOP**,I19)| 單 task 的 spec-tdd orchestrator(跑 escalate 機械)| 寫 acceptance test(RED)、encoding audit、派 level-2、親自驗證(re-run / coverage / hash)、tier 要求的攻擊輪 | 自己實作 production code(self-testing 硬禁)、git 寫入 |
| level-2 implementer(**MID**,I19)| 實作者 | 實作到綠 + 自身 unit tests | 改 acceptance test(hash 鎖定)、git 寫入 |

tier 為 `spec-tdd-adversarial` 時,level-1 內部再派 attacker / dry-loop auditor(fresh context、byte-exact 還原紀律、mutant batch verification——那些紀律由該 tier 的 SKILL.md 定義,本層不重複)。

**為何禁 self-testing(同一 agent 寫碼 + 寫測 + 自評):circular reasoning。** 實作者的盲點會同時進入 code 與 test,green 是自我實現的。分離 implementer 與 orchestrator,讓 acceptance test 在實作存在前由不同 context 鎖定——hash 鎖定驗收測試、dispatch 前後 bit-identical 驗證(I4,在 level-1 執行)。這是整個家族存在的原因;在 task loop 裡同樣不可讓步:**level-1 若無法派 level-2,唯一合法的行為是停下回報,不得退化成 self-testing。**

## When to Use

- 一個 feature phase 拆成多個 task(通常 5+),每 task 一份自足 doc,逐 task 開發、逐 task commit。
- 預期跨越多個 session、context 會被壓縮或中斷 → 需要狀態區 + 半成品續作模式。
- 有權威計畫文件(single source of truth:需求 + 決定區 + 任務總表狀態區)。
- 上游依賴(外部 API、別團隊 service)未定案 → mock-first 契約開發(見專節)。

**When NOT to use:**
- 單一 task / 單一 feature → 直接 `/spec-tdd-escalate`(或手動選 tier),主 session 自己當 orchestrator;外層迴圈是 overhead。
- 一次清一 batch 獨立小 bug → `spec-tdd` 的 **multi-unit run**(一個 session 內迴圈單元;邊界在單元,不涉及 per-task commit 與跨 session 狀態)。
- 探索性 / 拋棄式程式碼 → 不需要任何 skill。

## Pre-flight

1. **Orchestrator tier check(I21)。** Before any work, check the model THIS session runs as. A run's judgment executes entirely in the orchestrator's own context; I19 pins every dispatch tier, but nothing can upgrade the session itself. **Top tier in use, or no higher tier exists → silent, move on.** Otherwise surface this ONE ask and stop for the answer:

   > ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

   本 skill 的 gate 雖輕,但 level-1 dispatch 必須 TOP(它承接全部 planning / 驗證判斷)——頂層 session 本身若跑中階,整個 phase 的 routing 與覆核判斷都跟著壓在中階上。
2. **Session commit 授權(開跑前問一次)。** Task 邊界 = commit 邊界是本 skill 的回滾設計,但 commit 權限始終是 user 的——loop 開跑前明確問一次:「本 session 授權頂層在每個 task 邊界 commit 嗎?」**授權** → gate 通過後頂層直接 commit(仍明確列檔名;push 不在此授權內)。**未授權** → 不省略邊界:每個 task 邊界暫停,列出該 commit 的檔案清單交 user 手動執行,狀態區補 user 回報的 hash——回滾單位不變,執行者換人而已。
3. **Adversarial ceiling(開跑前問一次)。** 每 task 的 tier 由 level-1 的 escalate 機械按 stakes 自動判定——但一次 full `spec-tdd-adversarial` 是小時級(攻擊輪 + dry-loop rotation),長 task list 整個 phase 會被吃掉。所以 phase 開跑前先設**全 phase 的 tier 上限**,一問:「本 phase 允許 escalate 到 adversarial 嗎?**預設:不允許**」——**不允許(預設)** → 上限 `spec-tdd-coverage`:level-1 的路由把它當硬上限,stakes 再高也只在 coverage 執行,並在報告揭露「本 task 被 ceiling 擋下」(被擋的 critical task 進 phase 報告的殘餘風險清單)。**允許** → 追問一次:「adversarial task 跑 `timebox` 嗎?**建議:要**」(timebox = I8 的限時 invocation:dry-loop 併成單輪、Part A 限縮到 change surface——正是為 task loop 這種每 task 成本相乘的情境設計的)。Ceiling 是 phase 政策,中途要改走「中途變向」機制(下一個 task 邊界生效,同樣揭露)。
4. **Nested spawn depth check。** 預設 spawn 深度限制會讓 level-1 sub-agent 沒有 Agent tool → 無法派 level-2。修法:環境變數 **`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3`**,設在頂層 session 的啟動環境(harness 讀得到的位置——settings 的 env 區塊或啟動時的 shell 環境;在某次 Bash call 裡 export 影響不了 spawn sub-agent 的上層)。驗證法:dispatch template 內建「若你沒有 Agent tool,立刻 STOP 回報」——第一個 task 它回報有 tool,設定即生效。
5. **權威文件就位。** Phase 開始前確認三件套存在:(a) 需求本文;(b) **決定區**——編號決定(如 D1、D2…),新決定**續接編號**,不改號不重編;(c) **任務總表狀態區**——每 task 一列:id + 白話名稱 + 狀態(pending / in-flight / done + commit hash)+ 一行證據指向。
6. **Task-doc 自足性檢查。** 每個 task 一份自足 doc——sub-agent 不翻其他文件就能做。必要欄位:
   - 目標與範圍(含明確的**非目標**);
   - 現況錨點:file:line(行號會 drift,同時給 method/symbol 名當錨);
   - 設計要點;
   - **完整外部契約一次給全**——DDL 全文、API 形狀、介面簽名;禁寫「同前案」「見需求文件」;
   - 驗收標準(可轉成 acceptance test 的行為描述);
   - 風險與回滾。

## The loop(每 task 一輪)

1. **選 task + 驗錨點。** 依總表依賴順序取下一個;前一個 task 落地後 file:line 會漂移——快速驗 doc 錨點仍準,不準先修 doc(以 method 名重錨)。狀態區標 in-flight。
2. **Dispatch level-1(TOP)。** 用下面的 template。doc 內的路徑縮寫必須在 prompt 裡**還原為絕對路徑**(sub-agent 的 cwd 不可依賴);template 的 `{family root}` 亦同——填 skill family 安裝位置的絕對路徑。
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

NEVER implement production code yourself — no self-testing. Same-context
test+implementation is circular reasoning: the implementer's blind spots
enter both the code and the test, and green becomes self-fulfilling. If you
have no Agent tool, STOP and report that fact — do NOT fall back to
implementing yourself.

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

TIER CEILING: {coverage | adversarial+timebox | adversarial-full} — the
phase-level cap set at pre-flight. Your escalate routing treats it as a
HARD maximum: if this task's stakes would route above the ceiling, run AT
the ceiling and disclose the cap in your report — the capped-critical
residual is the phase's accepted trade, decided by the human upfront.

MOCK PHASE: {yes/no}. If yes: the contract target is the mock established
by task {id}; reduced verification depth is user-approved for mock-phase
tasks; disclose the tier actually used.

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
 4) disclosures: tier actually used (+ any mid-run downgrade or ceiling
cap), deviations from the task doc (DDL deltas, mock placement,
naming/structure), locally decided rule details  5) prior-test adaptations
with per-file rationale.
```

## 輕量 gate(頂層唯一的驗證動作)

Level-1 回報後、commit 前,頂層親自:

1. **編譯** — 主 module 的 `compileJava` + `compileTestJava` 親跑一次(例:`./gradlew :Core:compileJava :Core:compileTestJava`),綠才算數。
2. **檔案範圍** — `git diff --stat` + `git status --porcelain`,對照 level-1 回報的 created/modified 清單;出現清單外的改動 = 先盤點(level-1 說明或回退)再 commit。Untracked scratch 目錄除外。
3. **數字複核** — 讀 JUnit XML(`build/test-results/test/*.xml`)對 level-1 回報的逐類數字(見下節)。
4. **hash 抽查** — level-1 應回報 acceptance test 的 dispatch 前 / 後 hash(bit-identical,I4);頂層比對字串相等即可。

**不做的**:深度 code review(下沉給 level-1 的 audit / 攻擊輪)、親自跑測試(level-1 已跑,XML 在)、重跑全套(gate 失敗需要診斷時例外)。頂層做主觀審查不是勤快,是浪費:它沒有 level-1 的 full context,結論不會比 sub-agent 的 audit 輪好,卻燒掉最稀缺的 context。頂層的價值在**客觀性與連續性**,不在深度。

## 數字複核紀律

- **規則:sub-agent 回報的測試數字一律讀 JUnit XML 複核,不採信口頭。** 實測兩次踩到口頭數字錯:一次回報 165、XML 實為 163;一次回報「+6 個新測試(21+6=27)」、XML 實為 30。
- **計數單位陷阱** — `@ParameterizedTest` 一個方法 = N 個 invocation,JUnit XML 的 tests 計的是 invocation。上述 30 的案例:實際 +7 個方法(6 個 `@Test` + 1 個 `@ParameterizedTest` 跑 3 組)= +9 個執行單位——回報者以方法數口算,行為無矛盾,純計數筆誤。複核對不上時先問:**回報的單位是 method 還是 invocation?**
- **XML 覆蓋陷阱 — 每個 test run 會清掉前一輪的 XML。** level-1 跑多批測試時,事後只有最後一批可複核。對策已寫進 dispatch template:**最終驗證 = 一次涵蓋全部相關 test class 的單一 gradle run + 逐類列數字**——這一輪的 XML 就是頂層複核的對象。

## Mock-first 契約開發(tier 選擇的時間維度)

上游依賴未釋出 / 未定案時:

1. **第一個 task 先做 mock**(mock controller / server),把契約定下來;後續所有 task 對 mock 開發,不空轉等待。
2. **Mock-first 階段的 tier 可以降(user 拍板)。** 對 mock 的程式碼,在契約定案前過度投資 verification 是浪費——契約一變,深測跟著重寫。Tier 不只按 blast radius(空間維度)選,也按**這份 code 的壽命階段**(時間維度)選。
3. **真實依賴確定後,排一個契約對齊 task** — 回頭比對真實 API vs mock 契約、修正偏差、補上 mock 期省下的深測。降級必須是「暫緩 + 回補」,不是「省略」;全程揭露。

## 中途變向(tier 降級送達在跑的 sub-agent)

User 任何時刻可因時間壓力降 tier——包括 task 進行中:

- **送達** — level-1 在背景跑時,用 SendMessage 把變更送進去(例:「停用 adversarial 輪,收斂到綠即收工,報告揭露 tier 變更」)。
- **資產保留** — 已完成的測試與實作不丟棄;收斂到綠就收工。
- **揭露** — 該 task 的報告必須載明 tier 變更(何時、降了什麼、留下什麼未驗風險)。
- 送不進去(非背景 dispatch)→ 於下一個 task 邊界生效,同樣揭露。
- **Ceiling 調整** — 開跑前定的 adversarial ceiling 中途要升/降,同路處理:送達在跑的 level-1,否則下一個 task 邊界生效,揭露同前。

## 半成品續作(session 中斷後)

Session 中斷 / context 損毀,task 停在半途:

1. **先盤點,不重寫** — `git status` + 既有 diff 對照 task doc,判讀哪些是合理半成品。
2. **spec-defect 檢查** — 中斷前留下的測試若與 task doc 矛盾 → **修測試,不扭曲 production**(I15 的精神:production 為遷就缺陷測試而彎 = 失敗的 run)。
3. **續作 brief** — 重派 level-1(若前手有留 ledger / scratch log,一併交出)時明確指示:**保留既有合理改動、只補缺口、不重寫**,並附上盤點結果(diff 檔案清單 + 判讀)。
4. 狀態區就是恢復點 — in-flight 的 task 直接可見(呼應 A16 的 resume 語意:在飛中的 row = re-verify,不盲目重做)。

## 揭露慣例(disclosure)

以下事項 sub-agent 報告**必須明列**、由頂層 / user 複審——不得默默做:

- tier 被上限(如 spawn depth 不足、phase 的 adversarial ceiling)或中途降級;
- doc 字面偏離 — DDL additive 偏差、mock 落點與 doc 不同、命名 / 結構調整;
- 本地拍板的規則細節(doc 沒寫死、level-1 自行決定的小規則);
- 前批測試的調整(下節)。

原則:**task doc 是契約。偏離契約而未揭露 = 契約失效**——下個 task 的 sub-agent 仍按舊契約理解系統。

## 迴圈牆(測試資產)

- 每個 task 的驗收測試是下一個 task 的既有資產——phase 越後面,牆越厚。這是 task loop 的複利。
- 後續 task 因 constructor / 契約演化調整前批測試屬合理演化,但:(1) **逐檔記錄**於報告並附理由;(2) **斷言語意不得改動**——改的只能是接線(新 constructor 參數、新契約欄位),不是預期行為。改了語意 = 那面牆倒了一段,必須當成新測試重走 RED→GREEN。

## LSP / IDE 診斷不是證據

子代理寫檔後,LSP / jdtls 常報過期假錯——「method undefined」「cannot be resolved」,甚至指向已刪除的 scratch 檔。**一律以 gradle compile / test 結果為準**(I19(f):the BUILD is the only oracle — IDE diagnostics are noise)。任何層級都不要把時間花在追 LSP 錯誤上。

## Common Mistakes

| Mistake | Fix |
|---|---|
| 頂層親自深度 code review、親自跑測試 | 輕量 gate only:compile、`diff --stat`、XML 數字複核。深度審查下沉給 level-1 的 audit / 攻擊輪;頂層 context 是整個 phase 最稀缺的資源。 |
| level-1 沒有 Agent tool,於是自己實作(self-testing) | 硬禁——停下回報 user;修法是 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3`(設在頂層啟動環境,不是某次 Bash call 的 export)。 |
| 採信 sub-agent 的口頭測試數字 | 讀 JUnit XML 逐類複核(實測:回報 165 實為 163;回報 21+6、XML 30)。 |
| 數字對不上就當行為異常 | 先問計數單位:`@ParameterizedTest` 1 方法 = N invocations,XML 計 invocations;單位換算後仍不符才是異常。 |
| level-1 跑多批測試,前批 XML 被清掉無法複核 | Dispatch template 明定:最終驗證 = 單一 run 涵蓋全部相關 test class + 逐類數字。 |
| `git add -A` / `git add .` 收 commit | 明確列檔名——工作目錄必有 `.spec-tdd/` 等 untracked scratch,會被吃進 commit。 |
| 頂層沒問就在 task 邊界自己 commit | Pre-flight 問一次 session commit 授權;未授權 → 邊界暫停、列檔案清單交 user 手動 commit,狀態區補回報的 hash。 |
| sub-agent 自己 commit / stash / checkout | 全層禁止 git 寫入;commit 是頂層獨佔職責(task 邊界 = commit 邊界 = 回滾單位)。 |
| user 拍板的決策只留在對話裡 | 即時回寫權威文件決定區(編號續接)+ 相關 task doc(舊方案劃刪除線備查)。對話會被清除 / 壓縮——沒回寫 = 沒發生。 |
| Session 中斷後把半成品整個重寫 | 續作模式:盤點既有 diff vs task doc → spec-defect 檢查(測試與 doc 矛盾 → 修測試)→ 保留合理改動、只補缺口。 |
| Mock-first 階段硬上最重 tier「求穩」 | 時間維度:契約未定案前的深測是浪費(契約一變全部重寫)。User 拍板可降;真實 API 定案後用契約對齊 task 回補。降級是暫緩+回補,不是省略。 |
| 長 task list 放任 escalate 逐 task 自判,多個 task 全上 full adversarial,phase 被攻擊輪吃掉 | Pre-flight 問一次 adversarial ceiling(預設 coverage);template 的 TIER CEILING 是硬上限;stakes 超過 → 在 ceiling 執行並揭露,殘餘風險進 phase 報告。 |
| 中途要降 tier,直接殺掉在跑的 sub-agent 重來 | SendMessage 送達變更;已完成資產保留,收斂到綠即收工,報告揭露。 |
| 後續 task 順手大改前批測試 | 迴圈牆規則:僅允許接線調整(契約演化必須)、逐檔記錄;斷言語意改動 = 新測試,重走 RED→GREEN。 |
| 追 LSP / jdtls 的「method undefined」假錯 | BUILD 是唯一 oracle(I19(f));以 gradle compile / test 為準。 |
| Tier 降級 / doc 偏離 / 本地拍板沒有揭露 | Disclosure 慣例:全部明列由頂層 / user 複審——doc 是契約,未揭露的偏離讓契約失效。 |
| Task doc 寫「DDL 同前案」「見需求文件」 | 自足性:完整契約一次給全;dispatch prompt 把路徑縮寫還原為絕對路徑。 |

## Red Flags — STOP

- level-1 回報「我自己實作了」(self-testing)→ run 作廢,重派。
- level-1 回報沒有 Agent tool → 停,回報 user 設 spawn depth;不得讓它就地 self-testing。
- XML 數字與回報不符(計數單位換算後)→ 要求解釋或重跑;不吻合不 commit。
- `git diff --stat` 出現回報清單外的改動 → 盤點並獲得說明前不 commit。
- 任何層級 sub-agent 動了 git 寫入 → 先確認樹未受損,重申紀律。
- Acceptance test 在 dispatch 前後非 bit-identical → I4 FAIL,走 tier 的 TEST bucket,即使 re-run 是 GREEN。
- 續作盤點發現中斷前的 production 改動是為了遷就與 doc 矛盾的測試 → 修測試,還原被彎曲的 production。
- Tier 被降級、doc 被偏離而報告未載明 → 視為未驗證,要求補揭露後再複審。
