# OSPS-QA-06.01

- **Control:** OSPS-QA-06, Use Automated Testing in CI/CD Pipelines (Quality)
- **Level:** 2+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-qa-0601), the authority

> Summarised in this skill's own words.

- **Requires:** at least one automated test suite runs in CI/CD before a commit is
  accepted.
- **Meet it:** run tests on every change request, visible to contributors, in a
  consistent environment that contributors can reproduce locally. Tests CI cannot run
  (for example ones needing special hardware) belong in the project's constraints.
- **Verify:** inspect the pipeline and recent runs.
