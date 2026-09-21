# 2026-09-21 — W22 絕對路徑靜默成功事故:PHASE BOUNDARIES 路徑硬規範(受審計畫)

**Status**: 已施工(2026-09-21)— user 決策:1 = **全改(類級退役,六檔)**、2 = **A(不加幻影樹偵測)**、3 = **授權施工**;完工後 spawn subagent audit,**雙方同意 → commit(簡短)+ tag v1.24.0 + release + push + 本地安裝**(user 明示授權的條件式 release 鏈)。

**Orchestrator tier 披露**:本 session 跑非頂層模型(`glm-5.3-flash`);I21 ask 已問,使用者答 **ignore** — recorded decline,依 skill 規定列入最終報告披露。

---

## 1. Background(背景與既成事實,各附證據)

### 事故(2026-09-18,dtms-core repo)

> 事實來源:另一 session 的事故報告。dtms-core 為外部 repo,本 repo(spec-tdd-skill)無法重驗其現場 — auditor 取信即可,並在報告中聲明「incident facts taken as given」。

- W22 re-test 批次由 `spec-tdd-task-loop` 派工;level-1 實作 subagent 開工第一條指令把 repo 根目錄手打成 `E:/sourceCode/...`(正確為 `E:/@sourceCode` — 掉了 `@`)。
- 指令形如:`mkdir -p "E:/sourceCode/.../.spec-tdd/W22" && date > ".../W22/HEARTBEAT"`。
- `mkdir -p` + 輸出重定向讓任何路徑「靜默成功」→ 整棵平行目錄樹憑空被建,HEARTBEAT 寫進錯誤位置(watchdog 若查正確路徑會看到 stale 心跳)。
- 同一條指令以 `2>/dev/null` 讀 `POLICY-W22.md`,因同樣的錯誤路徑得到 ABSENT 假陰性(該次碰巧結論正確 — 真實路徑本來就沒有 POLICY 檔)。
- 當批其餘產物全落在正確路徑,零資料損失。

### 根因判定(提案 session 的主張)

SKILL.md 的 heartbeat 指示寫的是相對形式,但沒有禁止 agent 自行組絕對路徑;「create the directory if missing」+ `mkdir -p` 把打錯的路徑 materialize 成真。

### 現況事實(orchestrator 2026-09-21 讀檔建立;auditor 重驗)

- `skills/spec-tdd-task-loop/SKILL.md` L144–151:PHASE BOUNDARIES 段(level-1 dispatch template 內),heartbeat 指示 = L146–147「1) touch `.spec-tdd/<task>/HEARTBEAT` (create the directory if missing; touch or an equivalent write)…」;同段 item 2 = POLICY-<task>.md 重讀。
- `skills/spec-tdd-supervisor/SKILL.md` L161–168:同形狀段落,`<unit>` 版;heartbeat 指示 = L163–164。
- 兩段現況均為相對路徑形式,無任何絕對路徑禁令文字。
- 相鄰教義(與本修法互動,非修法對象):task-loop L73、supervisor L57 均要求 dispatch prompt 內「doc 路徑縮寫/template `{family root}` 還原為**絕對路徑**(sub-agent 的 cwd 不可依賴)」;兩 template 並有 `TASK DOC: {absolute path}` / `REQUIREMENT DOC: {absolute path}` 欄位。

## 2. The plan under audit(受審計畫,原樣,不預辯護)

兩處同樣的 PHASE BOUNDARIES 段,同樣修法:

1. `skills/spec-tdd-task-loop/SKILL.md`(~L146,heartbeat 指示緊後)
2. `skills/spec-tdd-supervisor/SKILL.md`(~L163,heartbeat 指示緊後)

修法內容:加一句硬性規範,建議英文措辭(與 template 語言一致):

> ~~"Resolve `.spec-tdd/...` against the repo-root cwd and use this RELATIVE form verbatim for the touch, the POLICY re-read, and every scratch write; NEVER hand-compose an absolute path — mkdir -p plus output-redirect makes a typo'd absolute path silently succeed, materializing a parallel tree whose heartbeat the watchdog never sees (2026-09-18 W22 incident)."~~
>
> **[已取代 — audit #1 C5(ii) refuted:「resolve against the repo-root cwd」倚賴家族教義宣告不可靠的 cwd,wrong-cwd 洞未關且 dag worktree 模式錨點錯誤;後續五項修正見第 7 節,定稿見第 8 節]**

提案者自述的重點:須涵蓋同一個 phase-boundary 區塊裡的 POLICY 重讀與**所有 scratch 寫入**,不只 heartbeat 本身。

## 3. Claims to verify(可證偽主張,各附指標)

- **C1(task-loop 現況)**:`skills/spec-tdd-task-loop/SKILL.md` 的 PHASE BOUNDARIES 段位於 L144–151,heartbeat 指示文字如第 1 節所引,段內無絕對路徑禁令。
- **C2(supervisor 現況)**:`skills/spec-tdd-supervisor/SKILL.md` 的對應段位於 L161–168,同形狀 `<unit>` 版。
- **C3(根因對應)**:現行兩段文字確實存在「agent 可自行組絕對路徑且 `mkdir -p`/重定向使 typo 靜默成功」的空間 — 即提案指出的根因在文本層面成立。
- **C4(涵蓋面)**:上述兩檔是否為此 hazard 在本家族 repo 的(唯一)承載面?至少檢查:`skills/spec-tdd-task-dag/SKILL.md`(平行 overlay,含 worktree 波次)、`skills/PROTOCOL.md`、其餘 skills 中同型 heartbeat / `.spec-tdd/` scratch 寫入指示(如 task-loop template RETURN 的 "full logs to scratch files under `.spec-tdd/`"、supervisor template 的 "WRITE the full report to `.spec-tdd/<unit>/REPORT.md`")。修法只改兩檔是否留下兄弟洞?
- **C5(措辭副作用)**:提案措辭與既有「路徑縮寫還原為絕對路徑(cwd 不可依賴)」教義的互動 — "NEVER hand-compose an absolute path" 的管轄範圍是否清楚限於 `.spec-ttd/…`(否則與 TASK DOC / FAMILY FILES 欄位的絕對路徑指示衝突);「resolve against the repo-root cwd」的前提與「sub-agent cwd 不可依賴」教義是否自洽(cwd 非 repo root 時,相對形式 + mkdir -p 仍會在錯誤位置 materialize);插入位置(「緊後」= item 1 之後 vs 整段尾)對 C4/涵蓋重點的影響。
- **C6(drift)**:行號與引文 vs 兩檔磁碟現況;`git log` 近期 commit 是否動過這兩段(本 repo 最近 v1.23.0 動過 supervisor)。

## 4. Checklist(auditor 至少執行)

(a) 逐主張驗證;(b) blueprint-vs-code drift(日期/commit 對照);(c) cross-item 互動風險(含 C5 的教義張力、worktree 模式若相關);(d) 對修法整體的 verdict + 最強反論(例:指示文本是否為正確的修補層 — 相對形式是否仍有 wrong-cwd 洞;有無更強形狀如 template 直接給出逐字指令);(e) 一個無人列過的風險。

## 5. Pending user decisions(auditor 只可標註後果,不代判)

- 是否採用本修法,以及最終措辭/插入位置(含 audit 修正案的取捨)。
- 版本號與 commit:一律 user 手動;本 session 永不 git commit。

## 6. Audit record(回填區)

- 2026-09-21 **Audit #1 完成**(read-only TOP,背景)。判決:C1/C2/C3/C6 confirmed;C3 且被評為 understated(家族 cwd 教義正向推向手組絕對路徑);C4 partially — heartbeat/POLICY 文字僅在兩檔,但同類表面另存(supervisor L267 FINAL-AUDIT 寫入、spec-tdd L82、coverage L75、adversarial L94/L100;task-dag L42 沿用 template 故編輯自動流入,L49 worktree 模式構成陷阱);C5(i) partially(NEVER 未限域)、C5(ii) refuted(cwd-resolution 與「cwd 不可依賴」教義矛盾 + wrong-cwd 洞 + dag worktree 錨點錯誤)、C5(iii) partially(item 1 內放置誤導管轄)。Position:方向與兩處錨點同意、措辭 as-is 不同意 — 五項必要修正。**Orchestrator 仲裁:五項全採納**(見第 7 節修正後文本)。
- 2026-09-21 **Re-audit #2 已派**(fresh,read-only TOP,scoped to 修正後文本 + 分歧史)。結果待通知。
- 2026-09-21 **Re-audit #2 完成**。判決:R1/R2/R4 confirmed(雙洞關閉、與絕對路徑欄位零衝突、bare-relative 讀法被三重訊號擋下、ABSENT 語意可執行且保留 fast path);R3/R5/R6 partially — dag wave 模式文本正確但缺 dispatcher 側填充規則(雙重故障靜默路徑)、L261 brief inventory 未擴充(死結風險)、分離符與 join 未言明。**新風險(e)**:PATH RULE 的 "in this prompt" 結構性停在 nesting 邊界 — level-1 組 level-2 brief 用的是 tier SKILL.md 的 handoff template,其 `.spec-tdd/` shorthand 仍無錨,write-heavy 層正是事故面。**Position:endorse the amended plan** — A1 必要(dispatcher 填充規則:task-loop L73 / supervisor L57 / dag L42)、A2 強烈建議(item 3 加向下攜帶句)、A3 建議(L261 inventory 加 FINAL-AUDIT 路徑)、A4 cosmetic("; 3)" 分離符 + "joined with a `/`")。**Orchestrator 仲裁:A1–A4 全採納。Audit bound 已達(audit + 一次 re-audit),不再有下一輪。**

## 6.5 施工後 audit(audit #3,2026-09-21)

- 施工後 read-only TOP audit(審工作樹 vs 藍圖 §7/§8 + user 全改範圍):**P1–P5 全部 confirmed;position = agree-to-release**。兩處與藍圖字面的偏差經獨立驗證為 substance-preserving 且更正確(supervisor 欄位不可能有 dag-wave 模式故刪子句;dag WAVE 行補理由)。CHANGELOG under-claim nit(ABSENT 硬化只歸 loop、漏 supervisor)——**已依 audit 指正修正**(commit 前)。
- **P6 殘餘風險(記錄在案,下個版本處理)**:tier skill 的 multi-unit wave scratch-copy 位置未釘死 — 若 copy 切在 repo 工作樹**內**,`git rev-parse --show-toplevel` 自 copy 內會對父 repo 成功,handoff 的分支條件("in a git repo/worktree: rev-parse must equal it; otherwise pwd-inside")產生歧義:字面讀者會對**正確填寫**的 SCRATCH ROOT STOP(該波每張卡 fail-stop 死鎖)。最壞是 fail-stop 或 run.log 落錯,不是本修法針對的靜默幻影樹,故不阻擋本版。**廉價修法(留給 future release)**:一句釘死 wave copies 切在 repo 工作樹外,或把分支條件改為 "SCRATCH ROOT carries no `.git` of its own → pwd branch"。次要想(弱):task-loop 的唯讀 top-side dispatch(Phase 0 plan-review、收盤批次審查)的 heartbeat 訊號無文字層錨定的路徑 — 非本次改動的退化,同屬「未錨定的被派工寫入者」物種。
- **Release 鏈執行**:雙方同意(auditor agree-to-release + orchestrator 同意,含兩文件修正)→ commit(簡短)+ tag v1.24.0 + GitHub release + push + `cp -r skills/* ~/.claude/skills/`(user 於決策 3 明示授權)。

## 7. 修正後計畫文本(audit #1 五項修正整合後;re-audit #2 標的)

### 7.1 SCRATCH ROOT 欄位(兩 template 各一,鄰 TASK DOC / REQUIREMENT DOC)

```
SCRATCH ROOT: {absolute path} — paste-verbatim anchor for EVERY
`.spec-tdd/` path in this prompt (repo root; under task-dag's wave
reuse, the assigned worktree root).
```

### 7.2 PHASE BOUNDARIES 段修訂(定稿 = audit #1 五項 + re-audit #2 A2/A4 融入;task-loop 版;supervisor 同形,`<unit>`,item 2 尾無 raising 子句,item 3 列舉加 REPORT.md)

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

> A4(per re-audit #2):分離符統一 "; 3)"、join 明言 "joined with a `/`"(naive 字串拼接少 `/` 會重現靜默 materialization,rev-parse 門只驗根不驗接縫)。
> A2(per re-audit #2):末段向下攜帶句 — 關掉「PATH RULE 停在 nesting 邊界」的新洞(level-2 implementer / attacker 的 `.spec-tdd/` shorthand 由 level-1 的貼上錨接管)。

### 7.3 supervisor 總複審 2「產出與證據規則」bullet 修訂(L267)+ brief inventory 擴充(L261,per re-audit #2 A3)

- L267:findings 全文寫入 `.spec-tdd/<unit>/FINAL-AUDIT.md`(resume substrate)——**brief 內以絕對路徑指明該檔(SCRATCH ROOT 貼上、不重打),auditor 不自行組路徑**;+ 回傳摘要。
- L261 brief inventory 追加一項:**FINAL-AUDIT.md 的絕對路徑(top 貼上)——auditor 的唯一寫入落點**(不加則嚴格照清單行事的頂層會漏給路徑,與 L267 的禁令死結)。

### 7.4 Dispatcher 側填充規則(per re-audit #2 A1 — 必要)

- task-loop L73(dispatch 指示)句尾追加:「template 的 **SCRATCH ROOT** 欄填本 run 的 scratch 根目錄絕對路徑(常規 = repo root)」。
- supervisor L57 同形追加。
- task-dag L42(WAVE 行)擴充:「SCRATCH ROOT 填該 task 的 worktree 根目錄(頂層所切,絕對路徑已知)。」——關掉 wave 模式雙重故障靜默路徑(頂層填 repo root + agent 留在 real tree 兩錯並存時 rev-parse 反而通過、heartbeat 落錯樹)。

## 8. FINAL PLAN(定稿;user 已決策 — 施工與範圍如下)

**User 決策(2026-09-21)**:1 = 全改(類級退役:3 檔 8 點之外,同批把機制延伸到 spec-tdd / coverage / adversarial 三個 tier skill——「只是要求 absolute path 而已,全改」);2 = A(不加幻影樹偵測——預防面已雙門);3 = 授權施工,完工後 spawn subagent audit,雙方同意才走 release 鏈(commit 簡短 + tag v1.24.0 + release + push + `cp -r skills/* ~/.claude/skills/`)。

**編輯清單(3 檔 8 點,列序即施工序):**

1. `skills/spec-tdd-task-loop/SKILL.md`
   - a. L73:SCRATCH ROOT 填充規則(7.4)
   - b. L101 TASK DOC 段後:SCRATCH ROOT 欄位(7.1)
   - c. L144–151:PHASE BOUNDARIES 段重寫(7.2 定稿,task 版)
2. `skills/spec-tdd-supervisor/SKILL.md`
   - a. L57:SCRATCH ROOT 填充規則(7.4)
   - b. L105 REQUIREMENT DOC 段後:SCRATCH ROOT 欄位(7.1)
   - c. L161–168:PHASE BOUNDARIES 段重寫(7.2 定稿,unit 版)
   - d. L261 brief inventory 追加 FINAL-AUDIT 路徑項(7.3)+ L267 bullet 子句(7.3)
3. `skills/spec-tdd-task-dag/SKILL.md`
   - a. L42 WAVE 行:SCRATCH ROOT = worktree 根目錄(7.4)

**Rationale**:W22 根因 = 被派工 agent 手組絕對路徑 + `mkdir -p`/重向靜默成功。修法把家族既有的可靠性錨(dispatcher 填絕對路徑,cwd 不可依賴教義)延伸到 scratch 命名空間:SCRATCH ROOT 貼上不重打(關 typo 洞)、不靠 cwd 解析 + rev-parse 門(關 wrong-cwd 洞,兼攔 dispatcher 自身填錯)、向下攜帶(關 nesting 邊界洞)、ABSENT 語意硬化(關 `2>/dev/null` 假陰性)。

**Attribution**:提案 = 原 session(措辭已被取代,見 §2 劃線);五項修正 = audit #1;A1–A4 = re-audit #2;仲裁與整合 = orchestrator。

**Pending user decisions(見對話呈現;不代判)**
1. 類級範圍:standalone tier run(escalate → spec-tdd L82 / coverage L75 / adversarial L94/L100)的 template 仍為無錠相對 shorthand — 本次修法 + A2 只覆蓋 loop/supervisor/dag 形狀下的 nested brief。是否同批做類級退役、或列 tech-debt。
2. 幻影樹偵測加項:要/不要。
3. 本計畫採用與施工授權(明示同意後才動 SKILL.md)。
4. 版本號與 commit(user 手動)。

**Residual risks(audits 揭露但不阻擋)**
- 頂層側 `.spec-tdd/` 寫入(RUN-STATE supervisor L59、POLICY 寫入 task-loop L227 / supervisor L276)不受貼上規範管轄 — 既有範圍,註記備查。
- rev-parse 門為一次性(首寫前);後續重打漂移僅靠指示。
- `test -f` 對 EACCES 邊角會誤判 not-found — scratch 情境可忽略。
- 幻影樹一旦生成,gate 的 `git status` 永遠看不到(repo 外)——偵測屬 pending decision 2。

**Disclosures**
- Orchestrator tier decline:本 session 非頂層(`glm-5.3-flash`),I21 ask 使用者答 ignore — 審查判斷由 TOP-pinned auditor dispatch 執行,orchestrator 僅 brief 蒸餾/仲裁/整合。
- Audit bound:audit #1 + re-audit #2(audit-plus-one,I16 形狀),已達上限。
- 事故事實(dtms-core,2026-09-18)取信自外部 session 報告,未重驗(兩 auditor 均已聲明)。
