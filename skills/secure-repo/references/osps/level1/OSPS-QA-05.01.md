# OSPS-QA-05.01

- **Control:** OSPS-QA-05, Prevent Executables in the Codebase (Quality)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-qa-0501), the authority

> Summarised in this skill's own words.

- **Requires:** no generated executable artifacts in version control.
- **Meet it:** generate them at build time, or fetch them in a documented pipeline step.
- **Verify:** search the tree for compiled executables and build outputs; check ignore
  rules cover build directories.
