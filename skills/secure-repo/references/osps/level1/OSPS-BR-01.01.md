# OSPS-BR-01.01

- **Control:** OSPS-BR-01, Prevent Untrusted Input When Building & Releasing (Build and Release)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-br-0101), the authority

> Summarised in this skill's own words.

- **Requires:** untrusted metadata used by a pipeline (branch names, commit messages,
  tags, change-request titles, author details) is sanitised and validated before use.
- **Meet it:** never interpolate such values directly into shell commands or scripts; pass
  them as environment variables or arguments, quote them, and reject unexpected values.
- **Verify:** read every pipeline for expressions that place event data into scripts. A
  workflow security scanner finds many of these; confirm each by reading.
