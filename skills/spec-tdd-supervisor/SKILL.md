---
name: spec-tdd-supervisor
description: Use when the user says "spec-tdd-supervisor", or wants ONE settled unit implemented with the WHOLE spec-tdd machinery delegated to a subagent while the main session keeps only a final comprehensive review — supervisor mode / full delegation of a single unit; every machinery dispatch (level-1 orchestrator, nested implementer, encoding audit, lite fresh review) is pinned to the MID tier as a recorded user opt-in, and the review-gate upgrade prompt fires at review time when the session is not top-tier. NOT for multi-task phases (spec-tdd-task-loop / -task-dag), NOT for machinery run in-session (spec-tdd-escalate), NOT for fuzzy requirements (grill front-ends). Triggers on supervisor mode, 全委派, delegate the whole run, all-MID run, top reviews only, 主 session 只做總複審, mid model 全包.
---

# spec-tdd-supervisor

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — the front-ends (`grill-spec-tdd`, `spec-tdd-escalate`), the tiers (`spec-tdd-lite` / `spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`), and [PROTOCOL.md](../PROTOCOL.md) (I1–I21). 本 skill 不新增也不放寬任何 invariant：tier 機械原樣下沉到 level-1 執行；這裡定義的是疊在家族**外層**的 run 形狀——誰在哪層、判斷 token 花在哪、以及兩個 recorded opt-in（全部 MID 偏離 I19(a)；I21 ask 移位到 review gate）。外層 driver 有三個**平行同輩**：`spec-tdd-task-loop`（多 task 序列）、`spec-tdd-task-dag`（多 task 平行 DAG）、本 skill（單單元全委派）——三者互不引用、互不派工：loop / dag 的 level-1 跑的是 escalate 機械，不會派 sub-agent 執行本 skill；本 skill 也不依賴它們的本文（監視與恢復機械自足於本檔）。

## Overview

單一已定案單元、一次全委派。主 session（supervisor）把整個 escalate 機械——sniff、選 tier、寫 acceptance test（RED）、派 encoding audit、派 nested implementer、親自驗證——**一次性**下沉給一個 MID level-1 subagent；自己在收尾只做一件事：**總複審**。經濟學：機械 token 全落在可拋棄的 MID context，TOP 判斷 token 集中花在唯一看得到全部 artifacts 的那一刻（終審）。

與 task-loop 的對比（為何這裡的 top **可以**深審、那裡被硬禁）：task-loop 跨多 task，頂層 context 是整個 phase 最稀缺資源，深審下沉給收盤批次審查（一個 dispatch）；本 skill 只有一個單元，頂層 context 便宜，**深審就是本 skill 存在的理由**——終審品質是這個 run 形狀唯一的加值點。

兩個 recorded opt-in（本 skill 形狀的既知代價；user 叫用本 skill 即成立，最終報告必須揭露）：

1. **全部 MID（對 I19(a) 的明示偏離）。** level-1、nested implementer、encoding audit、lite fresh review **全部 MID**——整個 run 唯一的 TOP 判斷點是終審。代價如實記載：弱 test 會先驅動完整實作、到終審才被抓，修復走 findings 重派（比 I19(a) 的實作前攔截貴）。補償控制：總複審的第一項深審固定是 **acceptance test 編碼忠實度重讀**——原 TOP encoding audit 的職責由終審承接，不因省 dispatch 而消失。
2. **I21 ask 移位到 review gate。** 進場只**靜默記錄**本 session tier；升級提示在終審前問（見總複審 0）。同意結構是兩筆帳：**機械跑 MID 的 decline 由 user 叫用本 skill 這個動作本身記錄**（與 opt-in 1 同源，invocation-based，不是被問出來的）；**審查的 tier** 才是那個 ask 的對象，在判斷真正發生的那一刻問。複審之前 top 的機械動作只有 template 驅動的 dispatch——進場路由與 requirement 落檔是少數保留的判斷，命名在此、不假裝不存在；I21 關切的是「判斷在什麼 tier 上執行」：機械判斷已被 invocation-decline 覆蓋、審查判斷由移位後的 ask 覆蓋。升級路徑（`/model` 同對話續行）與 decline 揭露照 I21 原樣——**是移位（對象縮到 review、同意機制從 ask 換成 invocation），不是放寬**。

| 層 | 是誰 | 做 | 禁止 |
|---|---|---|---|
| 頂層 supervisor（主 session，TOP 或 recorded decline） | 進場路由、一次性 dispatch、回報轉達、**總複審**、findings 處置、**列 commit 清單交 user（不自動 commit）** | 跑機械（寫 test / 派 implementer / 期中驗證）、終審前深讀交付物、親手修 findings、**git 寫入（含 commit——除非 user 明示要求代勞）** |
| level-1 sub-agent（**MID**） | 單元 spec-tdd orchestrator（跑 escalate 機械）：sniff、選 tier、寫 acceptance test（RED）、派 encoding audit、派 level-2、親自驗證（re-run / hash / tier 要求的證據） | git 寫入、路由出 band（above-coverage → STOP 回報）、停下等 user（夠不到——回報即 ask） |
| level-2 implementer（**MID**） | 實作到綠 + 自身 unit tests | 改 acceptance test（hash 鎖定）、git 寫入 |

**為何禁 self-testing（同一 agent 寫碼 + 寫測 + 自評）：circular reasoning**——實作者的盲點同時進入 code 與 test，green 是自我實現的。lite 路線的 solo 模式是入口 tier 的已知 trade，補償 = 強制 fresh-context review dispatch；**level-1 若無法派 nested dispatch（lite 的 review dispatch 也算），唯一合法行為是停下回報，不得退化成無 review 的 self-testing。**

## When to Use

- 單一 settled 單元（requirement 已落檔、決定已收斂），想讓主 session 的判斷 token 只花在終審。
- 接受「全部 MID」的代價：機械品質靠 tier 機械自身的結構保證（agent boundary、hash、XML 複核）＋終審把關，不靠 TOP 的期中判斷。
- 主 session 還要在這個對話裡做很多別的事——run 完後 context 仍有存量。

**When NOT to use — route elsewhere:**
- 多 task phase → `spec-tdd-task-loop`（序列）/ `spec-tdd-task-dag`（平行）。多 task 之下頂層 context 是稀缺資源，深審下沉與本 skill 形狀相反。
- 多單元 batch（bug list / 切片 feature）→ `spec-tdd` 的 multi-unit run（主 session 自跑）——本 skill 的一次性 dispatch 形狀不承載多單元（template 的 band carve-out 是第二道攔截，進場路由先擋）。
- 單一極小單元、用完即清的 session → `spec-tdd-lite`（in-session、1 個審查 dispatch）。lite vs supervisor 的分歧點：session 之後還有沒有別的事——有 → supervisor（保 context）；沒有 → lite。
- 純文件交付（無 production/test code 可測）→ tier 機械無適用對象，不進本 skill；直接派文件寫作 dispatch 或人工撰寫。
- 上游依賴未定案、要對 mock 開發的單元 → 嚴格說不是 settled（契約未定）；先走 grill 收斂契約。User 明示對 mock 跑：驗證深度可降（user 拍板、揭露、真實依賴定案後回補——mock-first 的單元版），非默認。
- Requirement fuzzy → `grill-spec-tdd`；fuzzy 且 blast-radius-critical → `adversarial-grill-spec-tdd`。Grill 完且 user 想要全委派形狀 → 再進本 skill。
- 機械要在主 session 親跑（判斷全程 top context、實作前就攔弱 test）→ `/spec-tdd-escalate`。兩者的選擇題是**判斷 token 誰出**：escalate = 機械 TOP；supervisor = 機械 MID + 終審 TOP。
- Session 無法派 sub-agent（無 Agent tool / spawn depth 不足且無法修）→ `/spec-tdd-escalate` in-session，揭露降級。
- 探索性 / 拋棄式程式碼 → 不需要任何 skill。

## Pre-flight（主 session）

1. **進場路由。** 上面的 When/When-NOT 逐項過；進了本 skill 才續行。
2. **Session tier 靜默記錄。** 記下本 session 跑的 model tier，**不問**——review gate 才問（opt-in 2）。
3. **Dispatch 能力檢查。** 主 session 需有 Agent tool；level-1 要派 level-2 → **`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3`** 設在頂層啟動環境（settings 的 env 區塊或啟動 shell；某次 Bash call 裡 export 影響不了 spawn）。修不了 → 降級：改跑 `/spec-tdd-escalate` in-session，報告揭露。
4. **Commit 模式（與 loop/dag 的差異——不自動 commit）。** Loop/dag 的 task 邊界 = commit 邊界，授權後由頂層自動落；本 skill 單一單元只有一個 commit，**預設 user 手動執行**：終審通過後頂層列交付檔案清單（含回寫後的 requirement doc），user 自己 commit、回報 hash，頂層補進最終報告與 RUN-STATE。**全鏈零 git 寫入**——頂層與所有 sub-agent 都不碰（read-only git 照常可用）。User 明示要求頂層代 commit → 照做，以披露模式記載（user 的決定權不因此條喪失）。
5. **Requirement 落檔確認（I17）。** settled 結論必須已是 doc（requirement verbatim + 決定）；只在對話裡 = 沒落檔 → 先落檔再開跑（planning 不下沉——I19(a) 精神，頂層執筆）。Handoff 用 doc path（I19(c)），不貼全文。

## The dispatch（一次性，背景模式）

用下面的 template 派 level-1（**背景模式**——blocking 呼叫讓頂層不可達不可監視）。**Agent call 的 model 參數必須明確指名 MID tier**（harness-relative，例如 sonnet）——省略 = 靜默繼承 session model，session 若是 TOP 則整個 MID 經濟當場破功（I19(a) 每 dispatch 指名 model 的本 skill 版：這裡指名的是 MID）。template 內 `{family root}`、doc 路徑縮寫一律還原為絕對路徑（sub-agent 的 cwd 不可依賴）；`{unit}` 由頂層定一個 kebab-case 單元名（如 `payment-retry`），全 run 一致使用。

派出當下，頂層執筆 `.spec-tdd/<unit>/RUN-STATE.md`：unit 名、requirement doc 路徑、dispatch 時刻、預期時長（依單元尺寸估——tier 此時未知，level-1 路由後對齊 tier 預算）、commit 模式（預設 manual；user 明示要求代 commit 時記錄）。**這是本 skill 的 re-arm base**：session 中斷後的重新武裝、續作重派、凍結記帳都以它為準（本 skill 沒有 task 邊界、沒有總表——這一頁就是狀態載體）。

### Level-1 dispatch template

```
ROLE: You are the spec-tdd orchestrator for ONE settled unit — the
supervisor run-shape: the WHOLE machinery is delegated to you; the
top-level session reserves itself for a final review. Run the
spec-tdd-escalate machinery for THIS unit only: sniff the requirement,
pick the tier by stakes, write the acceptance test (RED, RED-purity
checked), dispatch the encoding audit, dispatch a NESTED implementer
via the Agent tool, and verify it yourself (re-run GREEN, hash check,
tier-required verification). Invoke the /spec-tdd-escalate skill BY
NAME if it is available in your runtime. If it is not, do NOT improvise
a lighter version from this prompt — read FAMILY FILES below and run
that machinery exactly.

MODEL PIN (recorded user opt-in — supervisor shape, a disclosed
deviation from I19(a) made by the user's explicit skill choice): you
run the MID tier, and EVERY dispatch you make — encoding audit, fresh
reviewer (lite route), implementer — is ALSO the MID tier. Name the MID
tier explicitly in every Agent call; never let a dispatch silently
inherit the session model.

ORCHESTRATOR TIER CHECK — PRE-RESOLVED: treat the I21 pre-flight of
escalate AND of the chosen tier as already answered-decline. No ask
was surfaced to any user, and none was needed: the user's explicit
invocation of the supervisor skill-shape IS the recorded decline
(the machinery runs MID on purpose; the top session backstops
judgment at its final review). Do NOT stop to ask about upgrading;
carry "I21 decline recorded (supervisor all-MID opt-in, at
invocation)" into your report disclosures.

No self-testing OUTSIDE the lite tier. Same-context test+implementation
is circular reasoning: the implementer's blind spots enter both the
code and the test, and green becomes self-fulfilling — every tier above
lite dispatches a separate implementer, and lite (the entry tier for
small non-critical units) compensates with a MANDATORY fresh-context
review dispatch over its test+implementation. If your escalate routing
selects lite, run the lite machinery exactly, including that review
dispatch. If you have no Agent tool, STOP and report that fact — do
NOT fall back to implementing yourself (the review dispatch needs the
tool too).

REQUIREMENT DOC: {absolute path} — READ IT FIRST; it is settled
(requirement verbatim + decisions). Path shorthand maps to:
{abbreviation → absolute path}.

USER-FLAGGED GAPS: {none | gap list + the user's recorded
"settled, route" call}. If present, the requirement only LOOKS
settled: these decision gaps were surfaced by the sniff and the
user chose to route anyway — let Phase 1 see them (I20's handoff
shape).

FAMILY FILES (if the skill is not invocable in your runtime, READ these
from disk and follow them — the machinery lives there, not in this
prompt):
{family root}/skills/spec-tdd-escalate/SKILL.md (the routing you run),
{family root}/skills/PROTOCOL.md (invariants I1–I21), and the chosen
tier's {family root}/skills/<tier-name>/SKILL.md.

DOC EDITS: report proposed requirement-doc edits; do not edit the doc
yourself — the top-level session owns decision writeback.

SCOPE: this unit only. Existing acceptance tests this unit touches
are the regression wall: adapt one only where this unit's contract
evolution forces it — one file at a time, assertion SEMANTICS
unchanged, each adaptation listed in your report with its rationale.

GIT: NO git write operations (add/commit/stash/checkout/restore/...)
at ANY level of this run — you, your nested children, and the
top-level session alike. The USER commits manually at close, from
the file list the top delivers. Read-only git
(status/diff/hash-object) is fine.

TIER BAND: lite … coverage — structural. Your escalate routing runs
inside it, including lite (small
non-critical units: solo author-implementer plus ONE fresh-context
review dispatch; disclose the tier used), with ONE carve-out:
escalate's MULTI-UNIT route (a bug list, a feature split into
slices) does not fit this skill's single-dispatch shape — a
requirement that is actually several units: STOP and report BEFORE
anything; the top exits to a spec-tdd multi-unit run in-session.
The CEILING is structural: adversarial is not carried in this
run-shape either (hours-level attack depth contradicts the
MID-delegation economics). A unit whose stakes would route above
coverage: STOP and report BEFORE implementing — the top's default
is to EXIT this skill and run spec-tdd-adversarial standalone
(re-routing at coverage here would be an unconsented downgrade; on
exit, the requirement doc plus any already-written test hand over
as REFERENCE INPUTS — the standalone run executes its own Phase 1,
treating a MID-written test as a draft to re-derive or harden, not
an intake).

ASKS YOU CANNOT REACH (escalate's routing-hygiene asks, dispatched):
the fuzziness-sniff ask (gaps in the "settled" doc) and the top-tier
adversarial confirmation have no user to reach. STOP and report — the
report IS the ask; the top relays it to the user. Do NOT guess, do NOT
silently absorb gaps, do NOT invoke adversarial on your own say-so.

PHASE BOUNDARIES (before/after each nested dispatch, when ENTERING a
wait on a nested dispatch, after each completed long tool run, after
each delivered file): 1) touch `.spec-tdd/<unit>/HEARTBEAT` (create the
directory if missing; touch or an equivalent write) — when the touch
coincides with entering a wait, write into the file: "waiting:
<child-id> expected-done <time>"; 2) re-read
`.spec-tdd/POLICY-<unit>.md` — an ABSENT file means no policy (not an
error); a PRESENT file overrides TIER BAND above, DOWNGRADE-ONLY.

NESTED DISPATCHES (any nested child — your implementer on tiers above
lite; your fresh-context reviewer on lite): dispatch each nested child
in BACKGROUND mode — a blocking Agent call makes you unreachable and
unmonitorable, and its never returning is NOT evidence the child lives.
Record the expected duration with each dispatch (floor it at the known
build cost of the affected files); on overtime with no fresh output from
the child (build outputs, task scratch), treat the child as dead:
TaskStop it first (a presumed death is not a confirmed one — two agents
must never write the same tree; clear build-process locks, e.g. stale
daemons, before re-dispatching), then re-dispatch: a CONTINUATION
implementer on its partial work; for a dead lite reviewer, a FRESH
reviewer — its judgment depends on fresh context, nothing is inherited.
Harness without background nested dispatch: disclose the degradation.

VERIFICATION REPORTING (your numbers will be independently rechecked):
  - FINAL verification = ONE gradle run covering ALL related test
    classes — each run CLOBBERS the previous JUnit XML, so only the
    last run survives for recheck.
  - Report per-class numbers read from build/test-results/test/*.xml
    (or your build system's equivalents), and state whether counts
    are @Test METHODS or EXECUTED INVOCATIONS
    (@ParameterizedTest: 1 method = N invocations).

RETURN (also WRITE the full report to .spec-tdd/<unit>/REPORT.md —
the resume substrate; a broken session recovers the numbers and
hashes from it): 1) one status line per command (command + pass/fail
counts), full logs to scratch files under .spec-tdd/ (never
committed; hand paths)  2) per-class numbers  3) created/modified
file list (absolute paths)  4) the acceptance test's dispatch-time
and post-run hashes (the bit-identical pair; on the lite route,
state "solo re-RED discipline applies — no hash pair")  5)
prior-test adaptations with per-file rationale (per SCOPE)  6)
disclosures: tier actually used (+ any mid-run downgrade or band
cap; the all-MID opt-in and the I21 recorded decline), deviations
from the requirement doc (DDL deltas, naming/structure), locally
decided rule details, and your proposed requirement-doc edits for
the top's writeback.
```

## In-flight 監視（單 dispatch 範圍——本文自足，不引用其他 skill）

三種失敗模式疊加可以燒掉整個下午：hard-fail（429 直接終止、有通知）、soft-wedge（推理退避迴圈：恆 running、零通知、transcript 停更）、zombie-wait（nested child 已靜默死亡，parent 健康地等一個永不返回的 Agent 呼叫——**Agent 呼叫不返回 ≠ child 活著**）。**零產出時長是第一級指標**；這是製程監視不是驗證動作——訊號全是客觀事實，無內容判讀。

1. **定期檢查（checkpoint ladder，dispatch 當下預排整梯）。** 每 ~15 分（示例預設，user 可調）一個一次性喚醒，**梯次預排**而非單發鏈：細階排到預算視野 + 2–3 個粗階遠火（例 +90 分 / +3 時 / +5 時，例示）。**主 session 與池同命**——429 視窗內連頂層 turn 一起死，單發檢查點的 re-arm 前提（fire 了就能補排）當場破產，遠火是唯一不依賴任何成功 turn 的覆蓋。每個 rung 的 prompt 自足自廢：自載 RUN-STATE 路徑 + in-flight 判讀 + 「無 in-flight → 清殘餘檢查點收工」（防收案後 stray 遠火，也抗 context 壓縮）。喚醒落在凍結窗口內 = 0 秒陣亡、免費（被拒請求不燒 token）；落在額度恢復後 = 頂層自動拿回控制權。

2. **每個 rung 檢查什麼（客觀訊號，全程只讀）。** (a) `.spec-tdd/<unit>/HEARTBEAT` 的 mtime 與內容（含 "waiting: <child> expected-done <time>" 宣告）；(b) `.spec-tdd/<unit>/` 背景 scratch 的成長（REPORT.md、log）；(c) build 輸出目錄 mtime（test-results 在滾 = 在推進；進程存在僅輔證——閒置 daemon 可活數小時）；(d) `git status` / `diff --stat`（實質產出）。**agent 自陳狀態永遠不解除實質產出時鐘**（「實作者在跑」不是健康證據）。

3. **三態判定（綁時鐘，各別容忍度）。** (a) **合法工作**——實質產出在流動或 build 在推進 → 重新武裝（成功落地的檢查 turn 順手補滿梯次）；(b) **zombie-wait**——四條件合取才確診：有活動跡象（heartbeat 新鮮或背景檔在冒）、零實質產出、build 未在推進、heartbeat 宣告的等待已逾期。**瞬時訊號區分不了 zombie 與健康的 in-phase 等待——逾期時鐘是唯一鑑別器。** 高置信死亡 → 15 分快刀，但**先走復活嘗試**（便宜路）：帶證據 SendMessage（child 已死的客觀證據 + 停止等待指示）+ 一個有界 grace——活著的 parent 可就地自救保住 context；只有動作（新 child 派出 / heartbeat 邊界 touch）算復活，口頭回報不算。復活失敗 → **共同手術**：kill 前先 SendMessage 拿最後遺言（積壓訊息在死亡瞬間送達，免費的自我狀態認知）→ TaskStop → 孤兒清掃（在飛的 nested children 一併停掉或確認已結束——獨立進程仍可能寫同一棵樹；清掃延伸到 build 進程鎖，Windows 殘留 daemon 鎖會撞新 build）→ 重派 fresh 續作 level-1（keep-don't-rewrite、先讀 POLICY 檔、優先不同池且滿足 **MID** 釘選）；(c) **全面凍結**——heartbeat / 背景檔 / build 全凍：歧義狀態（單一長推理 vs soft-wedge 外部不可區分）→ **長容忍 ~90 分**（示例預設，user 可調），預算兜底。

4. **Soft-wedge 的恢復。** 已知重置時刻（session 內任一 429 訊息載明）→ 排 reset+15 分的 nudge（SendMessage 喚醒＋收斂指示），甦醒寬限 ≈10–15 分（子先母後，n=1 緩衝值）；重置時刻未知 → 立即 nudge（送不進也不花成本）+ 一個 grace 週期；仍凍結 → 走 3(c) 的共同手術，**不無界等待**。**甦醒 ≠ 結束**：醒來的第一輪會按序補送全部積壓訊息（包括數小時前的舊政策——頂層隨即補一則確認/撤回），且距最終回報還有距離。

5. **預算 = 硬上限（三規則）。** tier 推導示例預設：lite 30 / spec-tdd 60 / coverage 120 分（user 可調；tier 路由前未知——初值用尺寸估計，level-1 路由後對齊）。超過 → 終止重派，**沒有「再等等」**；但：(i) 流動中的一次性重設——超支當口實質產出在流動 → 一次性重設並揭露（尺寸估錯是計畫缺陷；只准一次）；(ii) 續作重派按剩餘範圍重給（繼承已燒穿的預算 = 秒殺）；(iii) 預算必須大於該單元驗證計畫的總 build 時間。**重派上限 2**（I9 形狀），超過升交 user。

6. **凍結自動恢復（freeze SOP）。** 主 session 與 level-1 可能同池——429 凍結期間頂層也無法行動，窗口內僅有的槓桿是遠火與 user 手動訊息。**首個成功 turn（不論來源：遠火落地 / user 手動訊息 / 額度 trickle）必做三件事**：(i) 429 事件、池、重置時刻、凍結起點記進 `RUN-STATE.md`（transcript 錯誤行會被壓縮吃掉——檔案才是重新武裝的基礎）；(ii) 補排 reset+15 保險點；(iii) 揭露凍結。**該 turn 先收單再判讀**：先消化凍結期間的積壓（task 通知、agent 狀態、RUN-STATE 對帳）——凍結期完工的 level-1 以「全面凍結」的形狀呈現，先查收案再跑三態，否則誤殺自己的健康卡；已知凍結窗口自產出年齡與預算判讀中**扣除**（凍結是頂層的帳，不是 agent 的——機械式超支 kill 在此是誤殺）。**首見 429 後的派工紀律**：後續 dispatch 不得靜默落在該池——已知不同池且滿足 MID 釘選的模型可指名，否則停派至載明的重置時刻。

7. **本 skill 的降級收尾（最後一階）：退出，不是親跑。** 重派也不可得（池死盡 / harness 壞）→ 向 user 回報，改走 `/spec-tdd-escalate` in-session 跑。頂層親自接手机械（寫 test / 派 implementer）會毀掉本 skill 的兩個 opt-in 前提，不存在這個選項。

## 回報處理（頂層只轉達，不代判）

Escalate 的 routing-hygiene ask 在 dispatched context 裡夠不到 user——I21 已由 handoff pre-resolve（不轉達）；sniff 與 adversarial confirm 走 **v1.20.3 的通則：報告即 ask，由頂層轉達**。Level-1 的 STOP 回報：

- **Sniff 缺口**（doc 只看起來 settled）→ 原樣轉達缺口清單，問 user「grill 先，還是 settled 續跑」：**settled** → 帶旗標重派（fresh level-1，handoff 註記 user 已核可 + 缺口清單，缺口在 Phase 1 可見）；**要 grill** → 退出本 skill 進 grill 前端。
- **多單元真身**（doc 其實是 bug list / 切片 feature——template 的 band carve-out 攔下）→ 轉達，退出本 skill，改主 session 跑 `spec-tdd` multi-unit run。
- **Above-band stakes**（adversarial 級）→ 轉達 stakes 依據（一行），問 user：**Confirm adversarial** → **退出本 skill**，standalone 跑 `spec-tdd-adversarial`（正常 top-session run——攻擊輪是小時級深度，不在 MID 經濟內承載；requirement doc 與任何已寫的 test 作為**參考輸入**交接——standalone run 走自己的 Phase 1（direct-arrival 形狀），MID 寫的 test 是待重推/強化的草稿，不是 intake）；**Downgrade → coverage**，帶 recorded call 重派，最終報告揭露。User 別的裁決照 I12 成立。
- **No Agent tool** → 修 spawn depth / 環境後重派；不得讓 level-1 就地 self-testing。
- **其他終態報告（catch-all）**——I9 breaker 打完的失敗報告（3 次修復未果，是設計內的正常結局）、SPEC-bucket 的決策需要（I10：re-open requirement 是 user 的 call）等一切非 GREEN、非上述各型的終態：**原樣轉達（帶客觀證據），user 拍板**。User 裁定的重派是 fresh mandate，不燒 watchdog 的重派上限。**計數分工，三本帳分開**：死亡重派（watchdog / 恢復程序）計上限 2；findings 迴圈的重派由總複審的一輪 bound 綁；user-mandated 重派由 user 的明示 call 成立（揭露）——不互相挪用。

GREEN 報告 → 進總複審。

## 半成品續作（session 中斷後）

Session 中斷 / context 損毀，run 停在半途。本 skill 沒有 board——**trace base = `RUN-STATE.md` + `REPORT.md` + git**：

1. **先盤點，不重寫** — 讀 `RUN-STATE.md`（in-flight 事實：unit、dispatch 時刻、預算、commit 模式）＋ `git status` / `diff --stat` 對 requirement doc 做路徑級對照，判斷哪些是合理半成品；level-1 若已寫 `REPORT.md`，數字與 hash 從它回收——不從已死的對話挖。
2. **Level-1 還活著 → 優先 SendMessage 續同一個 agent**（背景 dispatch 保留完整 context；429 中斷的既有規則：agent 死、session 活 → SendMessage 續）。掛掉的是 nested implementer → 恢復的 level-1 自己重派續作 implementer，下沉一層。
3. **重派續作 level-1（keep-don't-rewrite）** — 附盤點結果（diff 檔案清單 + 範圍對照）＋「保留既有合理改動、只補缺口、不重寫」＋先讀 `.spec-tdd/POLICY-<unit>.md`（冷啟動的政策來源）＋ USER-FLAGGED GAPS 帶上。預算按剩餘範圍重給（繼承已燒穿的預算 = 秒殺）。
4. **重新武裝** — checkpoint ladder 依新 dispatch 時刻重排整梯；RUN-STATE 補斷點紀錄（中斷時刻、已重派代次）。

## 總複審（review gate——本 skill 的核心）

**0. Review-gate tier check（I21 移位後的落點）。** 非 top session → ONE ask：

> ⚠ **Review-gate tier check** — the machinery ran MID by your opt-in; this review is the run's only TOP judgment point, and this session is not top-tier. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues — the upgrade covers exactly the review + report). **Continue** → review at this tier; the decline is disclosed in the final report.

Top → 靜默。**兩筆同意帳在此分明**：機械跑 MID 的 decline 已由 user 叫用本 skill 時記錄（level-1 的 handoff 依此 pre-resolve，不問）；這裡問的是**審查本身的 tier**——對象與時點都不同，是本 run 唯一一次這個 ask，問完不得重複。

**1. 客觀項（機械便宜，先跑）。**
   (a) **編譯**——主 module 的 compile + compileTestJava 親跑一次，綠才算數；
   (b) **檔案範圍**——`git diff --stat` + `git status --porcelain` 對 level-1 回報的 created/modified 清單；清單外改動先盤點（說明或回退）；untracked scratch（`.spec-tdd/`）除外；
   (c) **數字複核**——讀 JUnit XML（`build/test-results/test/*.xml`）逐類對回報數字；計數單位陷阱（method vs invocation）先換算再判；對不上不收案；
   (d) **hash 比對**——level-1 回報的 acceptance test dispatch 前 / 後 hash 字串相等（bit-identical，I4）；lite 路線除外——無 implementer dispatch 可夾 hash，I14 的 solo re-RED 紀律取代此項（回報「無 hash pair」即合規）。

**2. 深審（TOP 判斷全花在這——本 skill 的加值點）。**
   a. **Acceptance test 編碼忠實度重讀**（全部 MID 的補償控制，固定第一項）：每條 requirement 行都有辨別力的 assertion？舉一個「錯但合理」的實作能通過嗎？over-assertion / silent interpretation？——原由 I19(a) 釘 TOP 的 encoding audit（審查職責定義在 I13）在此形狀下的落點。
   b. **Impl diff 正確性 + SPEC-DEFECT 掃視（I15）**：production 有沒有為遷就測試而彎的改動（test-defect 的痕跡）；diff 是否只在交付範圍內。
   c. **揭露一致性**：tier 實用、doc 偏離、本地拍板——逐筆合理、**合起來**與 requirement / 決定矛盾嗎。
   d. **殘餘風險盤點**：band cap、中途降級、未驗維度——全數進報告。

**3. Findings 迴圈（頂層不親修）。** Finding → **SendMessage 給 level-1 續跑**（完成過的 agent 可續——它有 full context，最便宜的一路）或重派續作（它的 context 已不可用時，keep-don't-rewrite）；頂層只遞事實與 finding，I10 三 bucket 判讀是 level-1 的事。**Bound：一輪 fix → 複審 delta**（I16 慣例）；未收斂 → 升交 user 拍板，不無限循環。

**4. 決策回寫 + commit 清單 + 最終報告。** Level-1 回報的 requirement-doc 編輯提案（DDL 偏差、本地拍板的規則）由頂層**套用回寫**——舊文劃刪除線備查、不直接刪除（家族慣例）；只留在對話裡 = 沒發生（I17 精神），下個 run 會按舊契約理解系統。**Commit 交 user 手動執行（預設）**：頂層列**交付檔案清單**（明列路徑，含回寫後的 requirement doc；`.spec-tdd/` 標記為 scratch 永不入清單——user 手動 commit 也不該 `git add -A`），user commit 後回報 hash，頂層補進最終報告與 RUN-STATE。User 明示要求頂層代 commit → 照做（明列檔名、禁 `git add -A`），以披露模式記載。最終報告必載：證據（XML 數字、hash）、揭露清單（tier 實用、**全部 MID opt-in**、review-gate decline if any、doc 偏離、本地拍板、re-test 建議、代 commit 披露 if any）、findings 處置、殘餘風險。

## 中途變向（降 tier）

User 時間壓力中途降 tier → **雙通道**：SendMessage 送進背景 level-1 + 同時寫 `.spec-tdd/POLICY-<unit>.md`（level-1 於邊界重讀，覆寫 TIER BAND，只降不升）；已完成資產保留，收斂到綠即收工。低於應得 tier 通過 → 最終報告列 **re-test 建議**（單元版記帳——沒有 board，報告就是帳本；不記，輕量首過靜默變永久）。

## Common Mistakes

| Mistake | Fix |
|---|---|
| 頂層 dispatch 後開始讀 level-1 的 scratch / 期中深讀交付物 | 客觀訊號（heartbeat / XML / mtime / 回報轉達）以外止步——判斷留給終審，context 是終審的燃料 |
| Agent call 省略 model 參數（靠預設值） | 靜默繼承 session model——TOP session 下整個 MID 經濟破功；每個 dispatch 明確指名 MID（I19(a) 的本 skill 版） |
| 頂層親自寫 acceptance test / 派 implementer / 跑驗證 | 機械全在 level-1；頂層跑機械 = 毀掉 run 形狀（判斷 token 燒在錯的地方） |
| Level-1 停下問 tier 升級 / 自行換 tier | Template 已 pre-resolve（ORCHESTRATOR TIER CHECK + MODEL PIN）；重派時重申 handoff |
| 採信 level-1 的口頭測試數字 | 讀 JUnit XML 逐類複核；單位換算（method vs invocation）後仍不符才是異常 |
| Findings 頂層親手修 | SendMessage 續跑或重派——頂層只遞事實；親修 = agent boundary 崩塌 |
| Computed adversarial 在本 skill 內將就跑 coverage | 退出 standalone 跑 `spec-tdd-adversarial`——攻擊輪不在 MID 經濟內承載；doc 與已寫 test 作為參考輸入交接（standalone run 走自己的 Phase 1） |
| 非 top session 跳過 review-gate tier check | 必問一次（opt-in 2 的落點）；decline 揭露進報告 |
| 頂層自己動了 git 寫入（「就一個 commit 順手掉了」） | 全鏈零 git 寫入：預設列清單交 user 手動 commit、回報 hash；代 commit 唯 user 明示要求，且以披露模式記載 |
| 交付清單漏列或混入 scratch | 清單逐檔列絕對路徑（含回寫後的 requirement doc）；`.spec-tdd/` 標記 scratch 不入清單——清單是 user 手動 commit 的唯一輸入 |
| Session 完全不能派 sub-agent 還硬跑本 skill | 降級 = `/spec-tdd-escalate` in-session，揭露；「頂層親跑機械」這個選項不存在 |
| In-flight 只排單發檢查點 | Checkpoint ladder 遠火（v1.20.2 形狀）——主 session 與池同命，遠火才不依賴成功 turn |
| Requirement 只在對話裡就開跑 | I17：先落檔（requirement verbatim + 決定），handoff 走 doc path |
| Bug list / 多單元 doc 直接進本 skill | 進場路由先擋（When-NOT）；漏進去 → template 的 band carve-out STOP 回報，退出改 `spec-tdd` multi-unit run——一次性 dispatch 形狀不乘單元數 |
| Session 中斷後從死掉的對話裡挖狀態 | `RUN-STATE.md` + `REPORT.md` + git 是 trace base——對話死了帳還在；見「半成品續作」 |

## Red Flags — STOP

- 頂層在終審前開始逐字深讀交付物 → STOP——context 留給終審；客觀訊號與回報轉達除外。
- Level-1 回報 self-testing，或沒有 Agent tool 還繼續 → run 作廢 / 修環境重派。
- Acceptance test dispatch 前後非 bit-identical → I4 FAIL，走 TEST bucket——即使 re-run GREEN。
- XML 數字對不上（單位換算後）→ 不收案，要求解釋或重跑。
- Level-1 路由發現 above-band stakes 卻默默開工 → STOP 重派——先回報、頂層轉達 user。
- 終審發現弱 test 但實作已 GREEN，頂層想手改 test → STOP——TEST bucket 重派 level-1（re-RED），頂層不親修。
- 重派已達 2 次上限還想再派 → 升交 user。
- 發現自己（頂層）正在跑機械的任何一步 → STOP——回到 run 形狀，或降級退出本 skill。
- 頂層在 user 明示要求之外執行了任何 git 寫入（含 commit）→ STOP——本 skill 的 git 寫入權全鏈歸零，commit 是 user 的手動收尾。
