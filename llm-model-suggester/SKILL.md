---
name: llm-model-suggester
description: >-
  Recommend the best LLM for a task using price, latency, context size, and reasoning depth.
  Keep the skill token-light, self-contained, and complete enough to preserve the full model catalog.
metadata:
  pattern: pipeline
  domain: model-routing
  token_focus: high
---

# Model suggester

Choose a model by **task shape + price + context + depth**. Keep outputs short.
Triggers: model choice, which model, best model, cheapest model, fastest model.

## Decision rules

1. **Price first** for tiny tasks or short answers.
2. **Capability first** for hard bugs or deep reasoning.
3. **Context first** when the prompt or repo is huge.
4. **Code-specialized first** when patching or refactoring dominates.
5. Keep all model families in the catalog; do not prune.
6. Tie-break order: huge-context > code-specialized > deep > balanced > cheap.

## Price matrix

| Band | Model | In | CW | CR | Out | Best for |
|---|---|---:|---:|---:|---:|---|
| Cheap | `GPT-5.4 Nano` | 0.2 | - | 0.02 | 1.25 | tiny tasks |
| Cheap | `GPT-5 Mini` | 0.25 | - | 0.025 | 2 | quick edits |
| Cheap | `Gemini 2.5 Flash` | 0.3 | - | 0.03 | 2.5 | rapid simple logic |
| Cheap | `Claude 4.5 Haiku` | 1 | 1.25 | 0.1 | 5 | fast scripts |
| Cheap | `GPT-5.1 Codex Mini` | 0.25 | - | 0.025 | 2 | inline code completion |
| Balanced | `GPT-5.4 Mini` | 0.75 | - | 0.075 | 4.5 | daily coding |
| Balanced | `GPT-5.4` | 2.5 | - | 0.25 | 15 | strong general reasoning |
| Balanced | `Claude 4.5 Sonnet` | 3 | 3.75 | 0.3 | 15 | everyday coding |
| Balanced | `Claude 4.6 Sonnet` | 3 | 3.75 | 0.3 | 15 | newest balanced |
| Balanced | `GPT-5.2` | 1.75 | - | 0.175 | 14 | improved instruction following |
| Deep | `Claude 4.5 Opus` | 5 | 6.25 | 0.5 | 25 | complex logic |
| Deep | `Claude 4.6 Opus` | 5 | 6.25 | 0.5 | 25 | deep bugs |
| Deep | `Claude 4.6 Opus (Fast mode)` | 30 | 37.5 | 3 | 150 | max-intelligence low-latency |
| Deep | `GPT-5.4` | 2.5 | - | 0.25 | 15 | hard logic |
| Deep | `GPT-5 Fast` | 2.5 | - | 0.25 | 20 | fast flagship chat |
| Deep | `Gemini 3.1 Pro` | 2 | - | 0.2 | 12 | complex analysis |
| Deep | `Grok 4.20` | 2 | - | 0.2 | 6 | unconventional reasoning |
| Huge | `Claude 4 Sonnet 1M` | 6 | 7.5 | 0.6 | 22.5 | huge context |
| Huge | `Claude 4 Sonnet` | 3 | 3.75 | 0.3 | 15 | balanced general coding |
| Huge | `GPT-5.1 Codex Max` | 1.25 | - | 0.125 | 10 | large repos |
| Huge | `Gemini 3 Pro` | 2 | - | 0.2 | 12 | broad repo reading |
| Huge | `Gemini 3 Pro Image Preview` | 2 | - | 0.2 | 12 | UI from screenshots/mockups |
| Huge | `Gemini 3 Flash` | 0.5 | - | 0.05 | 3 | rapid reasoning |
| Huge | `Kimi K2.5` | 0.6 | - | 0.1 | 3 | long docs/manuals |
| Code | `GPT-5-Codex` | 1.25 | - | 0.125 | 10 | code gen/refactor |
| Code | `GPT-5.1 Codex` | 1.25 | - | 0.125 | 10 | syntax-heavy work |
| Code | `GPT-5.2 Codex` | 1.75 | - | 0.175 | 14 | better debugging |
| Code | `GPT-5.3 Codex` | 1.75 | - | 0.175 | 14 | newer coding logic |
| Code | `Composer 1` | 1.25 | - | 0.125 | 10 | first-gen multi-file edits |
| Code | `Composer 1.5` | 3.5 | - | 0.35 | 17.5 | better project structure |
| Code | `Composer 2` | 0.5 | - | 0.2 | 2.5 | efficient agentic refactors |

## Legend

- `In` = input
- `CW` = cache write
- `CR` = cache read
- `Out` = output

## Output

- Primary model
- Fallback model
- Price
- Why
- Upgrade / downgrade note

## Selection hints

- Choose the cheapest model that still fits the task.
- Prefer huge-context models only when context is the blocker.
- Prefer code models when editing/reasoning over code dominates.
- Use Grok when unusual reasoning style or lateral thinking is useful.
- Upgrade only when cheaper models are likely to fail.
- If a model appears in multiple bands, use the first matching band in the tie-break order above.

## Token rules

- Keep the skill body short.
- No examples unless asked.
- Prefer one table + one rule block.
- Put price inline with model names.
- Move long lists to a reference only if this file grows too large.
- Preserve all catalog rows; compress by grouping, not deleting.
- Any model above the **$6 / 1M token** tier requires explicit user approval before use.

## Default picks

- **Fastest cheap:** `GPT-5.4 Nano`
- **Best cheap general:** `GPT-5 Mini`
- **Best balanced:** `GPT-5.4 Mini`
- **Best deep reasoning:** `Claude 4.6 Opus`
- **Best huge context:** `Claude 4 Sonnet 1M`
- **Best unusual reasoning:** `Grok 4.20`
