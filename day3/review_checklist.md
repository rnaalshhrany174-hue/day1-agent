# Lab 3.3 — Agentic Code Review Checklist
Review the day's agent codebases (repair agent, Day 2 scaffolding agent)
against every item. Log findings as: [severity] file — finding — owner.

## Correctness & quality
- [ ] Every tool/function has typed parameters and a docstring
- [ ] No mutable default arguments; no dead imports (flake8 clean)
- [ ] Model outputs are parsed defensively (strict JSON + try/except)
- [ ] Every candidate fix/output is VERIFIED by tests, never trusted

## Agentic-specific
- [ ] Loops are bounded (step limits, retry limits, timeouts)
- [ ] Each tool enforces least privilege and validates its arguments
- [ ] Retrieved/model content is treated as untrusted input
- [ ] Every decision is reconstructable from logs/traces (results.jsonl)
- [ ] Costs are visible: tokens and latency recorded per call

## Maintainability
- [ ] Prompts live in named constants/files, versioned like code
- [ ] Small, single-purpose functions/nodes; no god-loop
- [ ] Evaluation can be re-run in one command after any change
- [ ] README says how to run, what it needs, and what it must never do
