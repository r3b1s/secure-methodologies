# OSPS-AC-01.01

- **Control:** OSPS-AC-01, Use MFA for Sensitive Actions (Access Control)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-ac-0101), the authority

> Summarised in this skill's own words.

- **Requires:** anyone reading or changing sensitive resources in the authoritative
  repository (settings, secrets, protected branches) must pass multi-factor
  authentication. Passkeys count.
- **Meet it:** require MFA through the hosting platform or organisation settings, for every
  account with write or admin access.
- **Verify:** check the platform's organisation or repository setting that enforces MFA.
  Where the platform cannot show it for individual accounts, ask each maintainer and record
  that the answer is self-reported.
