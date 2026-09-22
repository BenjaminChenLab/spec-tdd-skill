---
name: spec-tdd-manager
description: Use when the user says "spec-tdd-manager", or wants ONE feature walked end-to-end through the family's whole running order as a single invocation — inventory-resume → grill the requirement if fuzzy (the grill's spec gate is Gate 1) → size route (one unit vs multi-task) → top-layer breakdown in the Phase-0 shape (authoritative plan trio + self-contained task docs, dag-ready columns) → independent plan audit via spec-2nd-opinion (auto-escalates to spec-3rd-opinion when any decision carries an IRREVERSIBLE blast-radius tag) → ONE merged go-ahead gate (final plan + audit verdict + implementation route) → delegated implementation (spec-tdd-supervisor / spec-tdd-task-loop eco / spec-tdd-task-dag eco). A sequence-and-route-only pipeline front door: it owns the two gates and the stage handoffs, nothing else — every mechanism lives in the invoked skill. NOT for routing one settled requirement to a tier (spec-tdd-escalate), NOT for plain multi-unit bug batches (spec-tdd's multi-unit run), NOT for standalone plan audits (spec-2nd/3rd-opinion), NOT for resuming an in-flight implementation phase (invoke the driver skill directly), NOT for adversarial-grade features (standalone tier run). Triggers on 全流程一條龍, grill 到實作一把抓, end-to-end feature management, one command from requirement to landing, 流程經理, 給我管到底.
---

# spec-tdd-manager

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — the front-ends (`grill-spec-tdd`, `adversarial-grill-spec-tdd`, `spec-tdd-escalate`, `spec-2nd-opinion`, `spec-3rd-opinion`), the tiers (`spec-tdd-lite` / `spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`), the outer drivers (`spec-tdd-task-loop` / `spec-tdd-task-dag` / `spec-tdd-supervisor`), and [PROTOCOL.md](../PROTOCOL.md) (I1–I21). 本 skill 不新增也不放寬任何 invariant：它是疊在整個家族**最外層**的純 sequencer——階段接力、自動選路、兩個 gate。所有機械活在被叫的 skill 裡；本 skill 親手跑任何機械（寫 acceptance test、深審、實作）= 越權走樣。

## Overview

一件 feature 的全流程經理：從需求進場到實作落地，同一張流程表跑到底——

**S0 盤點**（續跑起點）→ **S1 grill**（需要時；Gate 1 = grill 的 spec gate）→ **S2 尺寸路由**（單元 or 多工）→ **S3 拆解**（僅多工；頂層執筆）→ **S4 獨立審計**（2nd/3rd-opinion）→ **Gate 2：合併開工 gate**（唯一自有 ask）→ **S5 實作交棒**（supervisor / task-loop eco / task-dag eco）。

四根設計柱：

1. **Sequence-and-route-only**（escalate route-only 原則的推廣）。本 skill 擁有的是「下一站是誰」與「兩個 gate」，不是任何機械。
2. **先拆再審。** 多工時計畫本體（三件套 + task docs）先行，審計審的是**實作真正消費的成品**；之後帶著三件套進 task-loop，Phase 0 由它自己的進場條件（三件套已在 → 跳過）省掉第二道計畫審查——**一次 TOP 審查抵兩道**（2nd-opinion + Phase 0 step 3），這是本 skill 對多工 phase 的主要經濟學。審計 brief 追加拆解維度屬 2nd-opinion checklist 的 "at minimum" 合法擴充。
3. **兩個 gate，不多不少。** Gate 1 繼承自 grill（spec gate——方向核准，家族 invariant）；Gate 2 是本 skill 唯一自有的 ask（最終計畫 + 審計結論 + 實作路由 + 開工，一次核准）。拆解不另設 gate——任務總表併入 Gate 2 一起呈現。
4. **零新增偏離（per audit 修訂措辭）。** 拆解頂層執筆（I19(a) 字面）、審計 brief 組裝在 session（2nd-opinion 原文）、一切被叫 skill 原文照跑——PROTOCOL 不動、既有十二支不動。實作段**恒走 eco 經濟**是既有 opt-in（v1.26.0 的 invocation token）的沿用，非新偏離：user 叫本 skill 即成立（supervisor 原生即此形狀，loop/dag 帶 `eco` token），phase 報告照目標 skill 的既有揭露義務。

**階段邊界 = session 邊界。** 每段產出都是落檔文件（spec doc、三件套、審計回寫）：任何階段之間可以 `/clear` 換 session 再叫本 skill——S0 從磁上文件續跑，不重做（I17 精神：只在對話裡 = 不存在）。

**Ask 帳（誠實清單）。** Gate 1（grill 的）、Gate 2（自有）、I21 tier check（本 skill 進場問一次，handoff 沿路抑制重問；**已知摩擦，per audit 記載**：task-loop 的 pre-flight 無 skip 條款——非 top session 已答過仍可能重問一次，照答即可、揭露）、目標 skill 自帶的 ask（loop 的 commit 授權、dag 的時段模式）。除此之外全自動——每個自動決定一行宣告 + 一行理由，不問。

## When to Use

- 一個 feature 想從需求到落地一個指令走完，只在兩個 gate 出現。
- 進場素材不限：對話裡的 fuzzy 需求、已落檔的 settled spec、或介於其間。

**When NOT to use — route elsewhere:**

- 只想路由一個 settled 需求到 tier、不要計畫審計 → `spec-tdd-escalate`。
- 純 bug 清單 / multi-unit batch（多個獨立小修正）→ `spec-tdd` 的 **multi-unit run**（user 裁定 2026-09-22：manager 的價值在 feature 的計畫審計，batch 不需要 per-task commit / board / watchdog / 每卡終審）。
- 只想審計既有計畫、不實作 → `spec-2nd-opinion` / `spec-3rd-opinion` 直接。
- 實作 phase 已在飛（board / RUN-STATE 有 in-flight）→ 直接叫該 driver 續作（S0 也只會指路，不重跑前置）。
- 整個 feature 是 adversarial 級 → grill 照走，但實作**出管道** standalone 跑 tier（grill Phase 3 的路由與確認機制照舊）——小時級攻擊深度不在 eco 經濟與本流程的承載範圍。
- 探索性 / 拋棄式程式碼 → 不需要任何 skill。

## Pre-flight — orchestrator tier check (I21)

Before any work, check the model THIS session runs as. 本 skill 的 S3 拆解、S4 brief 組裝與仲裁、S2/S5 路由判斷都在 orchestrator 自己的 context 執行；I19 釘住每個 dispatch 的 tier，但沒有東西能升級 session 本身。**Top tier in use, or no higher tier exists → silent, move on.** Otherwise surface this ONE ask and stop for the answer:

> ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

已在本次對話問過（本 skill 或被叫的 skill）→ 跳過，永不重問；handoff 紀錄沿路攜帶，decline 進最終報告揭露。

## S0 — 進場盤點（續跑起點）

純文件盤點，一行宣告推斷結果：

- **FINAL SPEC doc 已在** → 走 S1 的 sniff 路線（乾淨 → 宣告跳過 grill，進 S2），並補做不可逆形狀掃描（S1 末段）。
- **三件套已在** → 已審計回寫過（修正歸因、struck-through 在檔）→ Gate 2；未審計 → S4。
- **任一 driver 的 board / RUN-STATE in-flight** → 指路：叫該 driver 續作，本 skill 不重跑前置階段。
- **全無** → S1。

分支優先序（per audit 修訂）：**三件套存在 > spec doc 存在**——兩者並存（S3 後常態）走三件套分支，不重跑 grill、不重拆。文件互相矛盾 / 多份同日 spec 無法判定 → 問一次（罕見）。grill 中斷重進 = 對話即不存在，從 S1 重來（I17）。

## S1 — Grill（需要時；Gate 1 在此）

- 進場是**對話需求**（無 doc）→ 需要 grill：critical 謂詞（a silent wrong result MOVES money / CHANGES authorization / IRREVERSIBLY corrupts data）命中 → `adversarial-grill-spec-tdd`；否則 `grill-spec-tdd`。其 Phase 1 的 spec gate 即 **Gate 1**。**grill 只跑 Phase 1（per audit 修訂）**——其 Phase 2（寫 acceptance test）與 Phase 3（叫 tier）由本流程的 S2–S5 取代：test 由下游機械撰寫、路由是本 skill 的 S5 表；唯一例外是全 adversarial feature 出場時的 Phase 3 路由再利用（見 When-NOT）。
- 進場帶 **doc 宣稱 settled**（user 手上的文件，或 S0 判定已有的 spec doc）→ fuzziness sniff（escalate I20 的形狀）：乾淨 → 宣告跳過 grill；有缺口 → ONE ask（grill 補談，還是 settled 續跑）——settled 成立即續（I12），缺口旗標隨行交給下游。grill gate 落檔的 FINAL SPEC 由建構即已決——sniff 對它靜默通過，不另設旁路。
- **Gate 1 的包加一行（審計預告，per audit 修訂為條件式）。** grill 的 gate 呈現裡附加：「審計：2nd / 3rd（理由：決定 D_k 帶 IRREVERSIBLE tag）」——**僅在管線續行時出現**（全 adversarial feature 已由 grill Phase 3 出場，不預告不會花的審計）；3rd 的兩倍 TOP 成本在**花錢前**可見、可否決。settled 進場（無 Gate 1）時，本 skill 自行掃 spec doc 的**不可逆形狀**（資料遷移 / DDL、對外契約、安全姿態、錢移動語義），掃描結果分兩支：**不可逆但非全 adversarial** → 3rd 觸發，一行宣告；**全 adversarial 形狀** → 出管道宣告（standalone tier run；escalate 的 adversarial confirm 慣例照家族規則）。user 當場可改（他們的 call 恆成立），不另設 ask。

## S2 — 尺寸路由

- **多工**：特徵切片、預期 > 1 個自足單元 → 進 S3。**純 bug 清單（multi-unit batch）不在本 skill**——直接導 `spec-tdd` 的 multi-unit run 出場（user 裁定 2026-09-22：manager 的價值在 feature 的計畫審計，batch 走家族既有較輕形狀）。
- **單元**：單一自足單元 → 跳過 S3（plan under audit = spec doc 本身，S4 照跑）。
- **adversarial 級** → S2 不重判（per audit 修訂）：grilled 進場已在 Gate 1 由 grill Phase 3 出場；settled 進場由 S1 掃描出場。**晚發現**的 adversarial（S3 critical-surface sniff 全數 pulled、或審計揭示）→ 走 S5 表的出場列。

一行宣告 + 一行理由，不問。

## S3 — 拆解（僅多工；頂層執筆 — I19(a)）

依 task-loop **Phase 0 / Pre-flight 5–6** 的格式，由本 session 執筆（planning 不下沉；事實偵察可派 read-only Explore，task-loop 原文允許）：

- **權威計畫三件套**：需求本文、決定區（既有決定沉澱為 D1… 續接編號）、任務總表狀態區（全部 pending）。
- **每 task 一份自足 doc**（欄位照 task-loop Pre-flight 6：目標與非目標、現況錨點 file:line + method 名、設計要點、完整外部契約一次給全、交付檔案清單、驗收標準、風險與回滾）。
- 總表加 dag 的兩欄：**depends-on** 與**預期改動檔案**——Gate 2 改路由（loop ↔ dag）零成本。
- **Critical-surface sniff**（Phase 0 機械）：adversarial 級 task 在總表標 pulled/external，standalone 跑，commit 照常落 task 邊界。
- 檔案路徑依專案慣例（I17：project convention wins）。

## S4 — 獨立審計

- Invoke **`spec-2nd-opinion`**（IRREVERSIBLE 觸發 → **`spec-3rd-opinion`**，預告見 S1）。
- **brief 的 checklist 追加拆解維度**（2nd-opinion 的 "at minimum" 允許）：task 覆蓋率（每條需求有 task 接）、漏 task、依賴順序正確性、task-doc 自足性、粒度變形、預期檔案欄互斥。
- 2nd / 3rd-opinion 的機械**原文照跑**：brief 組裝（Step 1，session 的活）、auditor dispatch、merge、disagreement 仲裁、grill-coverage finding 的 user 路由（I12）、回寫（struck-through 備查）、ONE targeted re-audit bound。
- 單元路線（S3 跳過）：claims-vs-codebase、blueprint-vs-code drift、grill-coverage hunt 照跑——計畫 = spec doc。
- **收案 stamp（續跑依據，per audit 修訂）。** 合意成立時，session 在計畫文件（三件套或 spec doc）記一行：「per audit (spec-2nd-opinion, YYYY-MM-DD): agreed, no amendments」（有修正時既有回寫已是磁上痕跡）。乾淨合意不留痕 = `/clear` 後與「沒審過」位元組相同——I17 形狀的洞。

## Gate 2 — 合併開工 gate（唯一自有 ask）

一次呈現：

1. **最終計畫**——多工：任務總表（id + 白話名稱 + 一行）＋ pulled/external 標記；單元：單元範圍一行。不可逆標記點名。
2. **審計結論**——verdict、已摺入的修正（歸因「per audit: …」，絕不默默吸收）、殘餘風險。
3. **實作路由 + 一行理由**（S5 表）。
4. **開工核准。**

- user 修正計畫 → 摺入 + 揭露；實質變更（動到 audited claims）→ 2nd-opinion 的一次 targeted re-audit bound 照用。
- 路由否決 → 同表重算（例：補「有時間壓力」→ dag eco）。
- **通過 stamp（per audit 修訂）。** 核可後、S5 叫用前，計畫文件補一行：「Gate 2 approved (YYYY-MM-DD): route = <choice>」——核可只活在對話 = `/clear` 後重問。
- **Gate 2 未過，不得叫任何實作 skill。**

## S5 — 實作交棒

| 形狀 | 叫用 |
|---|---|
| 單元、非 adversarial | `spec-tdd-supervisor`（requirement doc = spec doc；I17 已滿足；其 pre-flight 照跑） |
| 多工、預設 | `spec-tdd-task-loop eco <phase>`（序列 = ×1 限額壓力的 429 安全模式；Windows worktree 摩擦是已知 dag knob，預設偏序列） |
| 多工 + 真 DAG + user 明示時間壓力 | `spec-tdd-task-dag eco <phase>`（其時段模式 ask 照跑，本 skill 不預答） |
| adversarial 級（晚發現：S3 sniff 全數 pulled、或審計揭示） | 出管道：standalone tier run，doc 交接 |

- **eco 恒走**（invocation-based consent；supervisor 原生即此形狀）。
- **叫用 = 交棒。** phase 的續作、watchdog、commit 授權、中途變向、收盤批次審查，全部是目標 skill 的事。`<phase>` 帶 doc 路徑 + 一行 phase 描述（handoff 走 doc path，I19(c)）。

## Common Mistakes

| Mistake | Fix |
|---|---|
| 本 skill 親手寫 acceptance test / 深審 / 實作 | Sequence-and-route-only——機械在被叫的 skill 裡；越權即走樣 |
| 先審高階 blueprint，再讓 Phase 0 重拆重審 | 先拆再審：審的是三件套本體；Phase 0 由進場條件跳過，每個多工 phase 省一道 TOP 審查 |
| Gate 2 未過就叫實作 skill | 開工 gate 是唯一實作授權點（never-code-before-approval 的家族落點） |
| 3rd 升級在審計後才揭露 | Gate 1 的包先行預告（settled 進場則一行宣告）——花錢前可見可否決 |
| 審計未合意（disagreement 未決）就進 Gate 2 | 2nd-opinion 的 gate 是合意不是報告；未合意先仲裁或上交 |
| 對已落檔 spec 重新盤問（沒跑 sniff） | I20：乾淨即續行；user 的 settled call 成立 |
| grill 後照著它的 Phase 2/3 跑（寫 test、直叫 tier） | grill 只跑 Phase 1（gate = Gate 1）；Phase 2/3 由 S2–S5 取代——唯一例外是 adversarial 出場的路由再利用（per audit 修訂） |
| 純 bug 清單導入 loop eco | 出場：`spec-tdd` multi-unit run（user 裁定 2026-09-22）；batch 不需要 per-task commit / board / watchdog |
| 磁上已有產物還重跑前置階段 | S0：落檔即存在，續跑不重做 |
| 自行加第三個 gate（拆解後再確認一次） | 兩個 gate 是設計；任務總表併入 Gate 2 呈現 |
| eco 沒帶 loop/dag token | 叫本 skill = 選 eco 經濟；token 恒帶，phase 報告照目標 skill 揭露義務 |
| adversarial 級硬塞 eco 管道 | 出管道 standalone——小時級攻擊深度不在承載範圍 |

## Red Flags — STOP

- 正在寫 acceptance test、派 implementer、深讀交付物 → STOP——不是本 skill 的活。
- Gate 1 未過就進 S3 拆解 → STOP——grill gate 是拆解前提。
- Gate 2 未過就叫任何實作 skill——supervisor / task-loop / task-dag **或任何 tier**（grill Phase 3 直叫 tier 同罪，per audit 修訂）→ STOP。
- 磁上無 spec、sniff 也沒跑就跳過 grill → STOP。
- 不可逆標籤在案卻只排 2nd（無 user 否決紀錄）→ STOP。
- 帶著未收斂的審計 disagreement 開工 → STOP。
- 發現自己正在發明流程表以外的階段或 ask → STOP——流程表是閉集：S0–S5 + 兩個 gate，其餘交給被叫的 skill。
