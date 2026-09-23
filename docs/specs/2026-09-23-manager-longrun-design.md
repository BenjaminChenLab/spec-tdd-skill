# spec-tdd-manager `longrun` 旗標 — 設計與出貨前審計記錄(v1.28.0)

日期:2026-09-23 設計;2026-09-24 審計折入定稿。狀態:待 maintainer 核可 → 實施。

## 1. 動機(field signal)

v1.27.0 首次實跑後 maintainer 回報:「實際用過,還是覺得 top agent context size 會變得有點多」。這正是設計期按下暫緩的 delegation-first knob 的觸發條件(「先這樣試,若 context 真不夠再來改」)。

結構性原因:manager 把原本四個分開的 session(grill、拆解、審計、driver)串進同一個對話。context 大頭依序:S1 grill 的 grounding 檔案 reads → S3 拆解偵查(與 S1 重複消費)→ S4 審計回流與打回迴圈 → S5(driver 本身已是 lightweight gate,maintainer 裁定不動)。

## 2. 定案決策

| 決策 | 結果 | 理由 |
|---|---|---|
| 旗標名稱 | **`longrun`**(否決 `eco`) | maintainer 指出動機是 **keep top session context small、可以走更久**,不是省 token——此形狀 total TOP token 反而上升(S4 runner 自身即一個 TOP context;邊界複製)。`eco` 在 loop/dag 定義為 token 經濟,語意錯配。旗標命名法「意圖直名」(v1.26.1 先例)。曾考慮 lean(家族詞彙)/slim,選 longrun(直名動機)。 |
| flag vs default | **旗標優先(opt-in)** | crossover:小 run 委派純損(三條 dispatch 鏈+digest 固定開銷)、大 run 純贏(context 壓力主導);委派路徑零實跑數據,先校準。size-auto(≥N 卡自動)記為未來 knob。 |
| 範圍 | S1 grounding + S3 起草 + S4 審計跑委派;**S2 / Gate 2 / S5 / 兩個 gate 不變** | maintainer 裁定:S5 不用動;S1 也要包(investigation 委派「也很好」)。 |
| runner 溢位行為(per audit (f)) | **STOP 回報**(user 裁定 2026-09-24) | 嚴禁 truncate、嚴禁 digest 三件套進 brief(no-digests 規則);session 接手裁量:/clear 分段或不帶旗標重跑該段。分批審被否(v1.14.0 consolidated-attack 教訓:分批丟 cross-item 洞);規模上限被否(把最大受益者排除,自相矛盾,記為未來數據齊後 knob)。 |

## 3. 模式設計(審計後定稿)

`/spec-tdd-manager longrun` — 不帶旗標的 run 與 v1.27.0 逐 byte 相同;frontmatter description 一字不動(旗標不進 routing 文字)。

- **S1 grounding → read-only MID dispatch**。法源(per audit C1 修正):**task-loop Phase 0 的「盤 codebase 錨點可派 read-only Explore 代跑偵查」+ grill 原文 "(or dispatched)"**——grounding 事實的蒐集不是 I19(a) 的 planning 對象,委派由這兩處既有文字支撑(原設計誤引不存在的「I19(a) anchor-recon carve-out」,已改正)。產出**事實摘要落檔**(spec doc 同目錄):已確立事實每條 `file:line`、相關 symbol/table/config、鄰近慣例、blast-radius 相關表面、**coverage statement(自報沒涵蓋什麼)**;禁止結論與建議(下判斷即規劃下漏)。grill 以摘要為底,保留**抽取權**(決策關鍵特定檔可自讀;例外,非 bulk read 後門)與**續問權**(SendMessage 續問同一 agent;I18 照成立)。**帶旗標重進 + digest 已在 → 重用不重派,一行揭露**(per audit 修訂 4:堵 digest 重複生產)。摘要路徑 = S3 brief 輸入、S0 續跑素材。
- **S3 起草 → TOP-pinned 背景起草 dispatch**(recorded opt-in #1;**旗標下 supersede S3 節「由本 session 執筆(planning 不下沉)」**,per audit 修訂 3;補償 = TOP pin + S4 審計本就攻拆解維度 + Gate 2)。brief = FINAL SPEC 路徑 + 摘要路徑 + Phase 0 / Pre-flight 5–6 格式 + 每卡 sniff + dag 兩欄;三件套與 task docs **落磁碟** + **claims 附錄**(可證偽主張 `file:line`)。**完成時在計畫文件蓋「draft complete (YYYY-MM-DD)」戳——無戳視為 partial,S0 不送審、續派起草**(per audit missed-risk:堵半套三件套被審)。adversarial 發現 → STOP 回報(報告即 ask,top 轉達;機器 say-so 不啟動)。session 只做呈現層審閱與修改(attributed delta)。**單元路線(S3 跳過)此項不適用**(per audit 修訂 7)。
- **S4 審計跑 → TOP-pinned 背景 runner dispatch**(recorded opt-in #2;補償 = TOP pin + I12 硬 carve-out + Gate 2 + **brief-distiller 獨立性折損知情聲明**(per audit (d) 最強反論):claims 附錄由起草者自撰、受審者對審題的框架力上升——界:checklist 維度 manager 固定、auditor 自擁 (b)(e)(f) 維度、claims 在 v1.27.0 亦為 session 自撰,折損限於 distiller grounding)。runner 從磁碟絕對路徑讀 `spec-2nd-opinion` / `spec-3rd-opinion` SKILL.md **原文照跑**(task-loop 交棒模式,被叫 skill 零改動);brief 素材 = 三件套 + claims 附錄 + pending decisions,拆解維度照 S4 追加。**findings↔修正↔re-audit 迴圈全在 runner 體內**:findings 落檔(I19(b));需改三件套時 top 只搬路徑——一行 SendMessage 給起草 dispatch(有作者 context),改完落檔 + delta 摘要,一行叫 runner 複核;**單元路線無 drafter——spec-doc 修正由 session 做(attributed delta)**(per audit 修訂 7)。runner 的 announce-to-user 步降級為 session 的 at-dispatch 一行宣告(I19(e) 形狀,揭露;per audit C3 friction 2)。**RETURN(per audit 修訂 5)= final plan 路徑 + Gate 2 三件套(verdict、已摺入修正歸因、殘餘風險)+ user 決策類 findings 原文**(I12:runner 永不代決)。收案 stamp 由 runner 寫,session 驗戳才進 Gate 2。**Gate 2 當場實質變更的 targeted re-audit:session 直接派 fresh scoped auditor**(per audit 修訂 6;2nd-opinion 的 deliberate-fresh 字面,最便宜合法形狀)。環境前提 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3`(runner 體內派 auditor child;loop 同款)。**溢位 = STOP 回報**(user 裁定 2026-09-24):嚴禁 truncate、嚴禁把三件套 digest 進 brief(no-digests 規則);session 接手裁量——/clear 分段或不帶旗標重跑該段。
- **靜默死亡紀律**(三 dispatch 一體;**2nd-opinion 級:粗界 + ONE fresh re-dispatch(nothing inherited,揭露)+ 停等;runner 界 tens-of-minutes**——不引 loop 級 watchdog,liveness 定位 per maintainer-review 可否決):死 ≠ 無 findings。
- **不可委派清單(恆在 session)**:grill 對話與建議、Gate 1、S2 路由、user 決策類 findings 轉達、Gate 2 呈現與核准、S5 交棒。
- 續跑時旗標重帶;摘要與 findings 文件都是 S0 磁上素材。**混合模式續跑(旗標沒重帶)→ 一行揭露,不擋**(per audit missed-risk)。
- **I21 consent 映射(per audit 修訂 10)**:旗標叫用 = 對被委派判斷段(S3 起草、S4 仲裁)的 **recorded consent**(eco 的 LOOP:31 形狀);Pre-flight 對 session 剩餘判斷(grill 對話、Gate 1/2、路由、user findings 轉達)照常適用。

## 4. 修訂文字(SKILL.md;final)

新增 `## longrun 模式 — context-longevity 旗標`(S5 之後、Common Mistakes 之前):開頭 byte-identical 宣告 + 動機句 + I21 consent 句 + **第 3 節全部內容逐條落文**(五個 bullet 群 + 續跑/混合模式行 + I21 映射行;per audit 修訂 2:不可委派清單必須在 SKILL 文字內)。

指針與小修:
- S1 開頭:「帶 `longrun` 旗標 → grounding 先行委派(見 §longrun);對話、提問、建議、Gate 1 不變。」
- S3 開頭括號:「帶 `longrun` 旗標 → 起草委派、session 呈現層審閱——**supersede 本行『由本 session 執筆』**;見 §longrun」。
- S4 開頭:「帶 `longrun` 旗標 → 審計跑委派(見 §longrun)。」
- Pre-flight 條件句(per audit 修訂 3/10):「帶 `longrun` 旗標時,S3 起草與 S4 審計跑的判斷移入 TOP-pinned dispatch(旗標叫用 = recorded consent);session 保留的判斷:grill 對話、Gate 1/2、路由、user findings 轉達。」
- 支柱 4 補:「`longrun` 旗標另含兩個 recorded opt-in(S3 起草、S4 審計跑委派,見該節);不帶旗標時本柱原樣成立。」
- Ask 帳補半句:「longrun 不新增 ask(dispatch ≠ ask)。」
- Common Mistakes 補三行:longrun 下自己 bulk-read 繞過 digest(Fix:digest 為底+重用;targeted read 是決策關鍵單檔的例外)/ runner 體內消化 user 決策類 findings(Fix:I12 carve-out——此類 findings 原文必回 top 轉達;runner 永不代決)/ 委派靜默死亡當「無 findings」(Fix:ONE fresh re-dispatch + 揭露;仍死停等)。
- Red Flags 補一條:longrun 下 session 正在親自偵查或重組 brief 全文 → STOP(旗標目的正被自己吃掉)。

配套:README 版頭 1.27.1→1.28.0 + manager family 列補 longrun 一句 + **cost-table row 同步**(per audit 修訂 8:帶旗標 dispatch 帳 +MID grounding、+TOP drafter、+TOP runner;無旗標照 v1.27.0「net: zero」)。CHANGELOG 全條目;**standing-rule note 明文「延伸」v1.26.0 先例**(per audit 修訂 9:pillar-4 與 Ask-帳兩句是無條件非指針新增,超出 v1.26.0 記載的「MODE field + pointer sentences」清單;routing 文字仍零觸碰,免重跑結論不變)。PROTOCOL 不動;description 逐 byte 不變。

## 5. 出貨前審計(spec-2nd-opinion,2026-09-23 派 / 09-24 回)

TOP 唯讀 auditor,7 條可證偽主張 + (b)–(f) checklist。**條件同意——現稿不可出**;十條必要修訂全部採納(見 §3/§4 內聯標注),要點:

- **C1 REFUTED(設計引用錯誤)**:PROTOCOL I19(a) 無「anchor recon may delegate read-only」字樣(grep 證);真實法源 = LOOP:57 Phase 0 recon 用語 + GRILL:30 "(or dispatched)"。已改錨。
- C2 confirmed(depth-3 前提與結構;3rd-opinion 的兩個併發 auditor 亦在 depth-2)。
- C3 confirmed + 兩個 letter-friction:relay 規則(ESC:54)字面是 escalate-scoped,對 runner 的延伸騎 v1.21.0 的已記載泛化;2ND:55 announce-to-user 在 dispatch 內不可滿足 → 降級 I19(e) 宣告(已折)。
- C4 partially:S0 對 digest 無掛鉤 → 修訂 4(已折);stamp 移 writer 是對現行文字的真變更(已折);frontmatter 逐 byte 不變 confirmed。
- C5 partially:免重跑「規則」成立(routing 文字零觸碰),但對 pillar-4/Ask-帳兩句「沿用先例」是 over-cite → 修訂 9 明文延伸(已折)。
- C6 confirmed(longrun/eco 可區分);README cost row 漏列 → 修訂 8(已折)。
- C7 confirmed(grill ground-then-grill 無矛盾)。
- (d) 最強反論 = brief-distiller 獨立性回退 → 知情聲明折入 opt-in #2 補償清單(已折)。
- (e) 無人列過的風險 = manager 自身 I21 Pre-flight 在旗標下前提過時 → 修訂 10 consent 映射(已折,eco 形狀)。
- (f) grill-coverage 洞 = runner context 上限 → **user 裁定 2026-09-24:STOP 回報**(已折;分批/規模上限否決理由見 §2)。
- Missed risks 折入:draft-complete 戳、混合模式揭露、digest 重用、runner announce 降級。**未折(記錄在案)**:manager 三 child 的 liveness 停在 2nd-opinion 級(粗界+一次重派+停等),未引 loop 級 watchdog——maintainer final review 可否決升級。
