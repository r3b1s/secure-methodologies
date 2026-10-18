# OSPS-QA-02.02

- **Control:** OSPS-QA-02, Publish Software Dependencies (Quality)
- **Level:** 3+, after a release
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-qa-0202), the authority

> Summarised in this skill's own words.

- **Requires:** every compiled release asset ships with a software bill of materials.
- **Meet it:** generate SBOMs at build time with a tool whose accuracy has been checked.
  The tool and format are the human's choice.
- **Verify:** check recent compiled assets have SBOMs, and spot-check one against the
  dependency list.
