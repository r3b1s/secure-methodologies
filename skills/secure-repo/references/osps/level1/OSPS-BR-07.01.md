# OSPS-BR-07.01

- **Control:** OSPS-BR-07, Secure Secrets and Credentials (Build and Release)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-br-0701), the authority

> Summarised in this skill's own words.

- **Requires:** the project prevents unencrypted secrets and credentials being stored in
  version control by accident.
- **Meet it:** ignore files likely to hold secrets, and use automated secret detection
  before commits land (for example a pre-commit hook or platform push protection).
- **Verify:** check the ignore rules and the prevention mechanism, and scan the whole
  history with a secret scanner. Report where anything is found, not its value.
