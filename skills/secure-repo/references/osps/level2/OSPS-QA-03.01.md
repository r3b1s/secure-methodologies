# OSPS-QA-03.01

- **Control:** OSPS-QA-03, Address Pass/Fail Checks Before Accepting Changes (Quality)
- **Level:** 2+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-qa-0301), the authority

> Summarised in this skill's own words.

- **Requires:** automated status checks on commits to the primary branch pass, or are
  bypassed manually.
- **Meet it:** make the checks required in the branch protection or ruleset. The Baseline
  recommends not making optional checks pass/fail, so approvers are not tempted to bypass
  them.
- **Verify:** inspect the required checks and look for recent merges with failing checks.
