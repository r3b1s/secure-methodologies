# OSPS-BR-01.03

- **Control:** OSPS-BR-01, Prevent Untrusted Input When Building & Releasing (Build and Release)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-br-0103), the authority

> Summarised in this skill's own words.

- **Requires:** pipelines that run untrusted code (for example a contributor's change
  before review) cannot reach privileged credentials or assets.
- **Meet it:** run untrusted changes in jobs without secrets or write access; keep
  privileged steps in separate jobs that never check out or execute untrusted code.
- **Verify:** for every pipeline trigger, establish whose code it runs and what it can
  reach. Pay particular attention to triggers that run with the base repository's
  privileges on contributors' changes.
