---
name: spec-tdd-task-dag
description: Use when driving a multi-task feature phase whose WALL-CLOCK matters and the task plan is a dependency DAG — independent tasks run as parallel waves on a task-loop substrate (authoritative plan doc + per-task commits). Parallel multiplies quota pressure ×N (cap 3, user-adjustable); the serial sibling spec-tdd-task-loop is the 429-safe mode; a plain multi-unit bug batch is NOT this skill. Triggers on parallel tasks, dependency graph, task waves, wall-clock pressure, 時段自動切換, DAG 排程.
---

# spec-tdd-task-dag

**REQUIRED BASE:** `spec-tdd-task-loop` — read it first; every rule there applies unchanged(三層分工、輕量 gate、Phase 0 拆解 bootstrap、數字複核、mock-first、續作、揭露、commit 紀律)。本 skill 是它的**平行 overlay**:任務總表從序列佇列升級為相依 DAG,不相依且檔案互斥的 task 成波並行。不新增也不減弱驗證強度——只壓縮牆鐘(波末聯集測試 run 補回平行失去的那份,見下)。

**`mideco` 繼承(task-loop 的 Mideco 模式全段適用)**:每卡機械全 MID + 每卡 TOP 終審(gate 之後、merge 之前)——平行波是 mideco 的最大受益者:**波內 top-context ×N 的 quota 壓力消失**(波的機械全 MID;每卡終審是短的 read-only TOP,隨卡收斂交錯跑,不併發成波)。終審在**該卡的 worktree 內收斂**(diff、XML、`REPORT.md` 全用該 worktree 路徑;`FINAL-AUDIT.md` 落該卡 worktree 的 scratch——SCRATCH ROOT 填 worktree 根的既有規則),收斂後才進波末 merge;波末聯集 run 與收盤批次審查不變(加法不是替代)。

## When to Use(vs task-loop)

- 時間敏感 + DAG 有真實可平行結構(非鏈)→ 本 skill。平行同時乘上**限額壓力(×N,上限 3)與頂層 context 開銷**(狀態列流量、波管理、逐兄弟處置)——context 緊張的 phase,序列更省。
- 鏈狀相依 / task 數少 / 429 易觸發時段想保守 / 要最簡機制 → `spec-tdd-task-loop`。**序列不是舊行為,是 ×1 限額壓力的安全模式**:平行把 token 吞吐乘上併發數,易觸發時段(如白天尖峰)一個一個慢做,離峰(如半夜)再全速跑 DAG——模式本來就是時段的函數。

**When NOT to use:**
- 多單元 bug batch 的平行波(無 task-loop 基座:無權威計畫文件、無 per-task commit)→ `spec-tdd` 的 **multi-unit** 平行波。

## Board 升級:任務總表 = DAG

- 每列加兩欄:**depends-on**(空 = 根)與**預期改動檔案**(Phase 0 拆解一併產出)。
- Phase 0 的 fresh-context review 因此多一個攻擊維度:**相依邊正確性 + 預期檔案欄的互斥性**。
- **波計算 = 拓撲分組 + 預期檔案欄互斥檢查。** 欄位重疊的兩個 task 不進同波,即使邏輯不相依——共檔 = 序列鏈(tier 層 multi-unit 波的實戰規則上抬)。互斥排除的是**文字 merge 衝突**;**語意互毀(零共檔仍互相改變行為)不能由互斥排除**,由波末聯集 run 兜底(下節)。

## Pre-flight:模式 ask(task-loop 的 asks 之後,加一問)

展示波結構(如「3 波:[T01,T03]→[T02,T04,T05]→[T06]」),四選:

- **全平行** — 建議離峰時段;**全序列** — 行為等同 task-loop,429 易觸發時段的安全選擇;
- **逐波選** — 每波邊界問一次平行或序列;
- **自動時段** — 你報一次尖峰/離峰時段(例:「10:00–22:00 尖峰走序列,其餘平行」——**時段是你的限額經驗,skill 不預設**),之後每波邊界按本地時間自動切換,每次切換在 board 揭露。切換於波邊界生效,**在飛的波不中途殺**。

鏈狀 DAG(無可平行者)→ 此問靜默跳過。**併發上限 3(user 可調)**:同一波最多 3 個 task 同跑(每 task 內部還有 2–3 個 nested dispatch,最多 ≈9 條 agent 流),超過的波內分批輪轉。

**授權耦合(task-loop pre-flight 2)**:未授權頂層 commit → **平行模式不可用,自動退化全序列**——DAG 的 task commit 是頂層執行的 `git merge`,無「暫停交 user 手動 commit」的對應形狀;退化要揭露。

## 平行波執行(worktree 隔離)

- **波起點樹必乾淨,且要驗不是宣稱**:切 worktree 前頂層親跑 `git status`——非 scratch 殘留(untracked scratch 除外)→ STOP 先收乾淨。
- 每個平行 task:`git worktree add .spec-tdd/worktrees/<id> -b task-dag/<id>`(從波起點 HEAD)。tier 層的 worktree 禁令(「worktree 從 HEAD 分枝,未提交工作帶不過去」)在此**不成立**——乾淨樹上 HEAD 就是全部;這是兩層前提的差異,不是放寬。
- **文件權威在 real tree**:task doc 與計畫文件以 real tree 為權威(dispatch prompt 指 real-tree 絕對路徑,唯讀);worktree 只承載 production/test code 與 build 產物(**純文件 task 的交付文件除外**——隨 worktree 承載、波末 merge 回真樹,路徑級核對於 merge 後真樹執行)。波中 user 拍板回寫 real tree 後,影響在飛兄弟 → SendMessage 送達(同中途變向);送不進 → 該 task **merge 前對照決定區補驗**。
- Level-1 全程在 worktree 內(程式碼工作):RED→level-2→GREEN→驗證、XML 數字全在自己的樹。Sub-agent 照舊禁 git 寫入;**worktree 的建/併/清是頂層獨佔職責**。
- Dispatch template 沿用 task-loop 全文,加註一行:WAVE(siblings in flight: <ids> — 預期檔案欄互斥,禁觸其檔);**SCRATCH ROOT 填該 task 的 worktree 根目錄**(頂層所切,絕對路徑已知——level-1 全程在 worktree 內、watchdog 也讀該樹;誤填 repo root 會讓每張卡卡在 rev-parse 門前,而「填 repo root + agent 留在 real tree」的雙重故障會靜默重現 W22 的 stale-heartbeat 形狀)。
- **波末序列 merge**:各 branch 依總表順序 `git merge --no-ff task-dag/<id>`——每個 merge commit = 該 task 的 commit 邊界。衝突(互斥規則下不應發生)→ STOP 交 human。**board 更新無法搭 merge commit(merge hash 要 merge 後才存在)→ 波末最後一個 merge 後立一個 board commit**(狀態區 hashes、決定區、模式切換揭露)。**回滾單位 = merge commit + 其後 board commit,兩步一起 revert**——只 revert merge 會留一個宣稱 done 的 board。
- **波末 gate(merge 後,真樹)**:既有輕量 gate(compile 兩項 + diff 範圍)**加第四項「波聯集測試 run」**——該波全部 task 的相關 test classes 聯集,真樹跑一次(每波一次,仍遠省於序列的每 task 一次;**純文件 task 的數字項由路徑級核對取代,同 task-loop gate 第 5 項;無測試者不進聯集**)。頂層親跑此 run 是 gate 的明定例外(性質同 compile:新資訊、無既有 XML 可複核;同「重跑全套於診斷時例外」的形狀),證據 = 該 run 的 XML 數字。聯集 run 本身即該波最終 run,XML 覆蓋陷阱不適用於它。
- **波末一併重驗下一波全部 task docs 的錨點**(以 method 名重錨)——一波多 task 同時落地,漂移大於序列。
- Worktree 回收:確認 branch 已全併、殘留僅 scratch/build → `git worktree remove --force` + 刪 branch(level-1 必留 scratch 與 build 產物,乾淨 remove 必被拒;Windows 上另有 gradle daemon 檔案鎖)。
- **迴圈牆**:wave N 的 worktree 從 merge 完的 wave N−1 HEAD 切出 → 每 task 的「單一 run 涵蓋全部相關 test class」template 規定驗證了**所有前波**測試;**同波兄弟間**的交叉綠由波末聯集 run 兜底(語意互毀不能由檔案互斥排除)。聯集 run 全綠 → 無殘餘。
- **收盤批次審查**(task-loop 收盤程序)在**全部波 merge 完、總表 all-done 後**於 real tree 執行——波邊界不觸發它(它看的正是整個 phase 的累積效應,不是單波)。其 fix rows 進 DAG 照常排:**depends-on 與預期檔案欄要補**(空 = 根);收斂補輪範圍限 fix rows 的 diff。
- **Watchdog 訊號路徑與產出軸都在 worktree 內**:level-1 全程在 worktree,heartbeat / POLICY 檔、工作樹 diff(vs 波起點 HEAD)、build/test 輸出全部讀**該 worktree** 的路徑(worktree 是頂層切的,絕對路徑已知)——讀 real-tree 對應路徑永遠 stale,每張超過門檻的平行卡都會誤報。檢查點**一次喚醒服務全部 in-flight**(不逐卡排——×N 平行下頂層 context 經濟);zombie 發生在 worktree 內 → 復活嘗試與續作重派都在該 worktree 接手,路徑不變。**冷 worktree 的第一次 build 是冷的**(無 daemon 快取)——平行 task 的預算要把 cold build 計入,否則開工即超支。
- **梯次預排與凍結 SOP(繼承 task-loop watchdog 規則 1–2 與 429 段,此處只記波形 delta)**:平行本就乘上限額壓力(×N,上限 3)——遠火與凍結程序在 dag 是常態路徑不是邊角。細階視野 = 在飛卡預算的**最大值**,每次波 dispatch 補滿梯次;**凍結連波邊界一起凍**——凍結期到期的 wave dispatch 順延,第一個成功 turn 先收單(凍結期完工的兄弟卡、到期未派的波、board 對帳)再判讀與排波;凍結扣除**逐卡**適用——不同池兄弟在頂層凍結期間照跑在 dag 是常態,收單先於三態的價值高於序列。

## 續作(波中斷)

- Board 的 in-flight 可能是**一整波**:每個 worktree 獨立續作——429 死一個不影響兄弟(SendMessage 續該 agent,worktree 狀態即盤點結果);merge 前死的,branch 保留待恢復續跑;merge 完死的,等同 task-loop 的單 task 續作。
- 波內單一 agent 429 陣亡、剩餘量小 → 同 task-loop 規則:等重置 SendMessage 續同一 agent,或立即重派續作 agent 接手該 worktree;**頂層親手收尾在這裡同樣硬禁**——worktree 狀態就是現成的盤點指標,連改了什麼都在 branch diff 裡。波的其他 task 不受影響:不需要等,也不需要殺兄弟。
- 模式切換(逐波/自動時段)於波邊界生效,在飛波不中途殺;走 task-loop 的中途變向慣例,board 揭露。

## Common Mistakes(delta)

| Mistake | Fix |
|---|---|
| 把預期檔案欄重疊的兩個 task 放同波 | 波成員 = 拓撲獨立 + 檔案欄互斥,缺一不可;共檔 → 序列鏈。 |
| 429 易觸發時段硬開全平行 | 序列 = ×1 限額壓力;平行 ×N(上限 3)。模式該隨時段選——自動時段模式就是為此。 |
| 信任 worktree 內綠燈,跳過波末 gate(含聯集 run) | 檔案互斥只排除文字衝突;語意互毀靠波末聯集 run 兜底——它是 gate 必經項,不是可選項。 |
| Sub-agent 在 worktree 裡動 git | 禁令不變;worktree 建/merge/清是頂層獨佔。 |
| 波內兄弟陣亡,頂層吸收它的剩餘工作 | 硬禁(繼承 task-loop 規則)——重派續作 agent 接該 worktree;波的其他 task 不受影響,不需要等也不需要殺。 |
| revert merge commit 而留下其後的 board commit | 回滾單位 = merge commit + board commit 兩步一起;board 宣稱 done 而程式已回滾 = 狀態區說謊。 |
| 未授權 commit 下硬開平行 | 平行模式不可用,自動退化全序列並揭露——DAG 的 commit 是頂層的 merge,無手動路。 |
| 把 worktree 內的 task doc 當權威版本 | 文件權威在 real tree(dispatch 指 real-tree 路徑,唯讀);波中決策 SendMessage 送達,送不進 merge 前補驗。 |
| mideco 下終審讀 real-tree 路徑(卡還沒 merge,real tree 沒有它的產出) | 終審在該卡 worktree 內收斂:diff、XML、`REPORT.md`、`FINAL-AUDIT.md` 全用 worktree 路徑;merge 後才存在的東西不是它的審查對象。 |

## Red Flags — STOP(delta)

- 同波兩個 task 的 diff 出現同一檔案 → 互斥宣稱破產,STOP,該 task 移出波序列重排。
- 切 worktree 前 `git status` 有非 scratch 殘留 → STOP 收乾淨再切(波起點必乾淨是前提,不是假設)。
- 波末聯集 run 有任何紅 → STOP 診斷(語意互毀真發生了);全綠前不立 board commit。
- 自動時段切換未揭露於 board → 補揭露;切換紀錄屬 phase 報告。
