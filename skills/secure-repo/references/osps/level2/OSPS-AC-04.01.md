# OSPS-AC-04.01

- **Control:** OSPS-AC-04, Enforce Least Privilege on CI/CD Pipelines (Access Control)
- **Level:** 2+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-ac-0401), the authority

> Summarised in this skill's own words.

- **Requires:** a CI/CD task with no permissions declared runs with the lowest permissions
  in the pipeline.
- **Meet it:** set the repository or organisation default for pipeline credentials to
  read-only, or declare empty permissions at the top of each pipeline.
- **Verify:** check the platform's default token permissions and every pipeline
  definition for tasks that inherit broader access.
