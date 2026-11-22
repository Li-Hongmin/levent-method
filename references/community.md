# 社区机制摘要（本技能借用了什么）

- **Anthropic math-proof / siege**：orchestrator 不碰数学；每步新子代理、文件传递；账本 PROVED/REFUTED/OPEN + GOAL/AUDIT 标签，只追加、RETRACT 撤销；脚本给唯一机械判定（WAVE/CONCLUDE/RETRY/TAIL）；FLOOR=max(1,⌊0.3n⌋) 判系统故障；≥一半 kind: attempt；升级轮“只缺一个陈述的链”+ 同文件发 3 个深度 worker；目标 replace/raise/come back；END 行判完成；DEGENERATE 筛查。本技能差异：允许 worker 执行代码、增加对照物/FRAGMENT/Skeptic/Librarian/Lean、连续两轮无产出即停。
- **MerLean**：Bronze/Silver/Gold 证据等级与“是否解决”分开报告（平凡命题的 Gold 仍是无进展）；只对弱环做 Lean；skeptic 攻击清单，区分 resolved 与 conceded-by-exhaustion；卡住时换表示而非加审稿人。
- **formalize-math-paper**：先冻结陈述再证明、diff 监控子代理改陈述；不许为可证而弱化；“证明有缺口 ≠ 命题为假”；NEXT.md：在草稿 Lean 写更强陈述，沿原证明走到第一个失败引理即精确障碍。
- **LeanAutoformalizationSkills**：只有证明可临时，陈述批准即冻结；五箱 binder 测试（EXCESS 即失败）；拒绝默认值回退；审计流程必须拦下负向样例；`#print axioms` ≠ 内核重放。
- **Buzzard**：Lean 四问——陈述保真、能否编译、comparator、paranoid 多内核。
- **Tao**：可读证明+Lean > Lean+待重写 > 仅 Lean；人给启发 → 模型验关键步 → 人简化 → 形式化。
- **Erdős problems / OpenAI**：成果集中在长尾；“unsolved 不等于没解决”，查重工具会漏；无 Lean 的稿件一处符号错连带撤回多篇；部分“带 Lean”结果并未形式化主定理；模型会钻误形式化陈述的空子。
- **AlphaEvolve**：多数时候找回已知最优，改进幅度小；数值可用来提猜想。
