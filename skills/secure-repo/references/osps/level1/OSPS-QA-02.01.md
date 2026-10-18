# OSPS-QA-02.01

- **Control:** OSPS-QA-02, Publish Software Dependencies (Quality)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-qa-0201), the authority

> Summarised in this skill's own words.

- **Requires:** where the package manager supports it, the repository contains a list of
  direct language dependencies.
- **Meet it:** commit the ecosystem's manifest (for example `package.json`, `go.mod`,
  `Gemfile`).
- **Verify:** compare the manifest with what the code imports.
