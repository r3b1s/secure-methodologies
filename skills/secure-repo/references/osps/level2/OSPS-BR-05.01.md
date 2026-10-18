# OSPS-BR-05.01

- **Control:** OSPS-BR-05, Use Standardized Dependency Management Tools (Build and Release)
- **Level:** 2+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-br-0501), the authority

> Summarised in this skill's own words.

- **Requires:** build and release pipelines ingest dependencies with the ecosystem's
  standard tooling where it exists.
- **Meet it:** use the ecosystem's package manager with a manifest, and a lock file where
  the ecosystem supports one; avoid ad hoc downloads in build scripts.
- **Verify:** read the build and release pipelines and scripts for dependencies fetched
  outside the package manager.
