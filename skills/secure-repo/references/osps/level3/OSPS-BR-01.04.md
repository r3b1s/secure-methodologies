# OSPS-BR-01.04

- **Control:** OSPS-BR-01, Prevent Untrusted Input When Building & Releasing (Build and Release)
- **Level:** 3+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-br-0104), the authority

> Summarised in this skill's own words.

- **Requires:** inputs collaborators supply to manually started pipelines are also
  sanitised and validated.
- **Meet it:** treat manual pipeline inputs like untrusted metadata (BR-01.01); restrict
  them to expected values where possible.
- **Verify:** read every manually triggered pipeline's inputs and how they are used.
