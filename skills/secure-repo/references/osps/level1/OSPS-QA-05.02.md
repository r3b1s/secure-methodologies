# OSPS-QA-05.02

- **Control:** OSPS-QA-05, Prevent Executables in the Codebase (Quality)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-qa-0502), the authority

> Summarised in this skill's own words.

- **Requires:** no unreviewable binary artifacts (application binaries, libraries and
  similar). Images, audio and similar media are allowed.
- **Meet it:** remove such files, or replace them with source plus a build step.
- **Verify:** list binary files in the tree and history, and classify each.
