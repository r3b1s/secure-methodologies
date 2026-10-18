# OSPS-VM-05.03

- **Control:** OSPS-VM-05, Publish and Enforce a Dependency Remediation Policy (Vulnerability Management)
- **Level:** 3+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-vm-0503), the authority

> Summarised in this skill's own words.

- **Requires:** every change is checked automatically against a documented policy for
  malicious and known-vulnerable dependencies, and blocked on violation unless declared
  non-exploitable.
- **Meet it:** a required SCA status check on change requests (see
  [tools/categories.md](../../tools/categories.md)). The tool is the human's choice.
  Projects at lower levels may choose to meet this too; see [levels.md](../../levels.md).
- **Verify:** inspect the check and that it is required.
