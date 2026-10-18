# OSPS-AC-04.02

- **Control:** OSPS-AC-04, Enforce Least Privilege on CI/CD Pipelines (Access Control)
- **Level:** 3+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-ac-0402), the authority

> Summarised in this skill's own words.

- **Requires:** every job that is given permissions is given only what its work needs.
- **Meet it:** grant permissions per job, never at a broad level "just in case".
- **Verify:** read each job's permissions against what its steps actually do. A workflow
  security scanner (see [tools/categories.md](../../tools/categories.md)) finds candidates;
  reading confirms them.
