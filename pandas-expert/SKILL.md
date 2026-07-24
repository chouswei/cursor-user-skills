---
name: pandas-expert
description: >-
  Token-optimized pandas and data manipulation expert pipeline. Provides
  best practices, vectorized operations, and memory optimization for 
  pandas DataFrames and Series. Triggers: pandas, dataframe, series, 
  vectorization, apply, read_csv, performance optimization.
metadata:
  pattern: tool-wrapper
  domain: pandas
  version: 1.0-pandas

pipeline_steps:
  1. Context Analysis
     - Identify the user's current pandas operation (loading data, cleaning, transformation, aggregation, etc.).
  2. Principles Retrieval
     - Call Tool Wrapper: pandas-principles-retriever with query derived from the user context.
  3. Apply Conventions
     - Review the code or suggestion against the retrieved principles. Prioritize vectorization and performance.
  4. Final Output
     - Provide the optimized code or suggestion based on the principles.

system_instruction: |
  Respond in concise mode. Prioritize vectorized operations over loops and .apply() calls. Keep memory efficiency in mind.

token_guardrails: |
  - Context caching on core-pandas-principles.md
  - response_format: plain markdown final output
---

# Pandas expert

**Role:** Vectorized, memory-aware pandas help.

Run **pipeline_steps**. If retriever unavailable, load [references/core-pandas-principles.md](references/core-pandas-principles.md).

**Step 2:** `python tools/pandas-principles-retriever.py "<query>"` or ADK `pandas-principles-retriever`.

**Pairing:** [optimization-planner](../optimization-planner/SKILL.md) for resource-heavy data work.
