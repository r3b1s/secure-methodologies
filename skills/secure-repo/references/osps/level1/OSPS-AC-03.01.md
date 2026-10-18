# OSPS-AC-03.01

- **Control:** OSPS-AC-03, Protect the Primary Branch from Accidental Modification (Access Control)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-ac-0301), the authority

> Summarised in this skill's own words.

- **Requires:** direct commits to the primary branch are blocked by an enforcement
  mechanism.
- **Meet it:** a branch protection rule or ruleset that requires changes to arrive through
  a reviewed change request. The Baseline also accepts a decentralised model where changes
  land elsewhere and merging into the primary repository is a separate deliberate act.
- **Verify:** inspect the rule's configuration, including who may bypass it.
