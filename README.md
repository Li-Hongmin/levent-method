# levent-method

An agent skill (SKILL.md format, for Claude Code / Hermes and similar agents) for attacking hard open math problems with AI agents.

It combines community mechanisms — the round/ledger state machine of Anthropic's `math-proof` (siege), MerLean's evidence grading and skeptic role, statement freezing and audit from formalize-math-paper / LeanAutoformalizationSkills, Buzzard's four Lean questions, lessons from the Erdős problems project — with practices distilled from Levent Alpöge's public work (zeta ≥2/3 zeros, Euler/Navier–Stokes blow-up, the RH/GRH claim): human-supplied analogy and toy model, mandatory control-object tests, harvesting fragments from failed attempts, explicit sprint hand-off, and human compression before release.

Status: v0.3, **not yet validated on a real problem**; parameters adapted from community defaults.

- `SKILL.md` — protocol (Chinese)
- `scripts/ledger.py` — append-only ledger + mechanical verdicts (stdlib only)
- `templates/` — worker brief, skeptic checklist, control objects, Lean statement audit
- `references/` — sources and community mechanism summary

Independent distillation from public sources; not affiliated with or endorsed by Levent Alpöge or Anthropic. License: MIT.
