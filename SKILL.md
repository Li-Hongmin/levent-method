---
name: levent-method
description: Use when attacking a hard open math problem with AI agents.
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [math, ai-for-math, lean, multi-agent]
---

# Levent Method：人机协作攻坚数学难题

自包含。骨架取自社区成熟做法（Anthropic math-proof/siege 的轮次–账本状态机、MerLean 证据分级与 skeptic、formalize-math-paper / LeanAutoformalizationSkills 的陈述冻结与审计、Buzzard 的 Lean 四问、Erdős problems 的查重教训），叠加 Levent Alpöge 三项工作（zeta ≥2/3、Euler/NS 爆破、RH/GRH）的独有做法：**人给类比与玩具模型、对照物强制测试、失败片段收获、人类压缩发布**。来源见 `references/sources.md`，社区机制摘要见 `references/community.md`。

## When to Use
攻具名开放问题、设计多代理证明搜索、规划 AI 数学结果的形式化与发布。已知论文的形式化不属本技能主场景（用第 6 步即可）。

## 现实预期（先读）
- 公开数据里 AI 的真实战果集中在**长尾、少人关注、标准方法可达**的问题；批量投题命中率低（OpenAI 约 4000 题 → 数百个结果族）。大问题上常见产出是副产品（zeta 2/3 是攻 RH 的副产品）。
- Alpöge 的两样关键资源不可复制：未发布研究版模型与大预算（zeta：3100 万输出 token）；十年级领域直觉（C 档前提）。按自己的模型与预算选题。
- 文中的 650 / 60 / 54 等数字是轶事，不是参数。

## 分工档位（开题写入 `SPEC.md`）
| 档 | 人的输入 | 原型 | 前提 |
|---|---|---|---|
| A 放手 | 大目标 + 鼓励 | zeta 2/3 | 接受副产品；预算充足 |
| B 档案 | 精选线索档案 + 构造策略 | NS 爆破 | 已有带外力/条件版本 |
| C 主线 | 跨领域类比 + toy setting，模型补技术 | RH/GRH | 人有领域直觉 |

## 角色（每步新开子代理，只用文件传递）
- **Orchestrator**：只调度与记账，不做、不评、不转述数学；按 `scripts/ledger.py` 的机械判定行动。
- **Judge**：每轮读账本与答案，写下一波问题、更新账本与 summary。
- **Worker**：只看题面 + 单个问题文件；可执行代码做数值检查（siege 禁止，本方法允许，因 zeta 经验显示数值对照是主要过滤器）。
- **Skeptic**：常驻反驳角色，每个新关键陈述必配一次反驳尝试（攻击清单见模板）。
- **Auditor**：对完整证明逐行复核；两名互不知情。可用时至少一名换厂商/换模型（同源审计有共同盲点）。
- **Librarian**：可联网查重；输出每篇近邻的精确定理号与原文摘录，不凭记忆。
- **人**：第 0–2 步、冲刺交棒、Challenge 陈述审读、最终压缩。

## 流程

### 0. 冻结题面与查重（开跑前）
- `problem.md`：精确陈述、量词、已知界及出处。开跑后不改；改即新 run。
- Librarian 先查“是否已被解决”：“标着 unsolved 不等于没解决”（Erdős 项目过去一年主要进展来自翻出旧解）。命中即停。
- 写 `controls.md`：至少 2 个**对照物**——与目标共享尽可能多结构、但目标结论已知不成立的对象（见 `templates/controls.md`）。找不到对照物时写明，并把第 3 步改为“去掉某假设后的反例”测试。
- 写预算：最大轮数、每轮最大并发、token/金额上限。

### 1. 类比（人；B/C 档）
写 `analogy.md`：已知成立的平行世界及其证明骨架；搬到目标世界时**唯一缺失的机制 X**；主问句“目标世界里什么对象能扮演 X？”。可参考其他 AI 已发布结果中的结构。

### 2. Toy setting（人+模型；C 档）
在玩具情形先拿到完整证明（可仅用符号/正性），入账为 PROVED（toy）。未赢不进主线。玩具模型只证明“接口一致”，不证明目标。

### 3. 轮次循环（模型）
每轮：Judge 写 ≤WAVE 个问题 → `ledger.py check` → Worker 并行 → `ledger.py answers` → 未完成者重跑一次 → Skeptic 攻新陈述 → 下一轮 Judge 先筛 DEGENERATE。
规则：
- 每轮 ≥一半问题为 `kind: attempt`（真尝试，而非综述/特例）。
- 每个 attempt 必须报告在 `controls.md` 对照物上的结果；论证对对照物也成立 → REFUTED（过强）。
- 失败答案中的自洽片段入账 `FRAGMENT`，可被后续问题引用；留意“失败反转”（某界为空 → 反向使用）。
- 依赖先前结果时回读原答案文件，不信 summary 转述。
- 关键不等式用随机实例 + 梯度对抗实例攻击；可用已知数据（零点表等）批量核对。
- 换表示而非加审稿人：同一缺口两轮无进展 → 发一题“只给陈述、不给草图”，并要求换表示/分解。
- 升级轮（默认第 4 轮起）：summary 必须写出一条只缺一个陈述的推导链；该缺口文件原样发 3 个更深的 Worker。
- 目标变更：replace（原目标假/已知）、raise（已证后攻更强，已证结果复制到 `result-so-far.md`）、come back（升级后两波无进展）。

### 4. 结案条件
- GOAL 为 PROVED/REFUTED，且有两条来自不同 Auditor 的 `AUDIT` 行指向同一证明文本；另有一个只看陈述的 Worker 独立重证成功（或记录未成功）。
- Librarian 终态查重：结果是否已知、是否只是已知定理的短推论；主动更正优先权。
- 停机：达预算；或连续 2 轮无新 PROVED/FRAGMENT；或完成数 < max(1, ⌊0.3·本轮问题数⌋)（系统故障，非数学 no-go）。
- `proof.md` 必含 Status 节：`MAIN CLAIM: PROVED / NOT PROVED`、证据等级、开放缺口；不得引用运行中间文件。

### 5. 冲刺交棒（C 档）
人到达技术边界时写 `handoff.md`：正确情形、需要的量级（如“需 ~X 级重数”）、允许模型自选的参数与构造。人此后只判断是否偏离类比主线，并标注自己尚不理解的步骤。

### 6. 形式化即仲裁
1. 先写只依赖 Mathlib 的 `Challenge.lean`（证明 `sorry`），由人或独立审计代理按 `templates/statement-audit.md` 审完后**冻结**；之后用 diff 监控，子代理不得弱化陈述或加假设。
2. 模型写 `Solution.lean`。通过条件（Buzzard 四问）：陈述保真；编译通过；`lake comparator` 确认陈述一致且仅 `propext`/`Classical.choice`/`Quot.sound`；多独立内核重放（nanoda / lean4lean 等）。`#print axioms` 不等于内核检查。
3. 静态扫描 `sorry`/`admit`/`axiom`/`native_decide`/`opaque`/`addDecl`/自定义宏。
4. 自定义定义要审：拒绝零/默认值回退；按性质定义的对象先证存在唯一。当心模型钻误形式化陈述的空子得平凡解。
5. 未全形式化时，按 MerLean 思路只给**弱环**做 Lean：辩论是“耗尽”而非“解决”、承重步、只抽样未穷举的步骤。

### 7. 压缩与发布（人）
- 人独立核对 → 压缩成可读短证明 → 放回文献脉络 → 请领域专家读 → 发布论文 + 附录“证明如何被找到” + Lean 仓库（含 Challenge/comparator 配置）+ 会话记录。
- 不要只发 Lean：Tao 的消化分级是 可读证明+Lean > Lean+待重写文本 > 仅 Lean。论文与 Lean 可能不一致，发布前逐条对照。
- 披露句式："The mathematical argument was discovered and written by <AI>; the listed authors verified it and take responsibility." 撤回/修订保留版本记录。

## 证据等级（报告时与“是否解决问题”分开写）
- **E0**：单一模型自述。
- **E1**：双盲审 + 对照物测试 + 数值对抗通过。
- **E2**：E1 + 弱环 Lean 通过 + 独立重证。
- **E3**：主定理端到端 Lean，过 comparator 与多内核。
- **E4**：E3 + 领域专家读过可读证明。
结论类型：settled / conditional / interface-lemma / no-progress。“平凡命题的 E3 仍是 no-progress。”

## 文件布局
```
run/
  problem.md  controls.md  analogy.md  handoff.md  SPEC.md
  ledger.md   summary.md   state.md    result-so-far.md  proof.md
  rounds/r{N}_q{i}.md  rounds/r{N}_q{i}.answer.md
  lean/Challenge.lean  lean/Solution.lean
```
账本与判定：`python3 scripts/ledger.py {init,add,check,answers,status} run/`（标准库，用法见脚本头注释）。模板：`templates/worker-brief.md`、`templates/skeptic.md`、`templates/controls.md`、`templates/statement-audit.md`。

## 陷阱
- Worker 提示逐字发送；不要转述数学。鼓励只在 A 档会话层使用，“相信”不是证据。
- 脚本只检查账本格式，不检查数学；结案仍靠 Auditor 与 Lean。
- 编译通过 ≠ 陈述正确；没有 Lean 的结果一处符号错可连带撤回多篇依赖稿。
- 查重工具会漏旧解；“新结果”至少两次独立检索。
- 巨量 AI 自然语言稿不是交付物。
- 本方法 v0.3 尚未在实题上验证；首次使用建议先对一个已解决、较新的中等结果做盲复现，记录成本与失败点后再调参。
