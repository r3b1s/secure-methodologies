# OSPS-SA-01.01

- **Control:** OSPS-SA-01, Publish Design Descriptions of System Actors and Actions (Security Assessment)
- **Level:** 2+, after a release
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-sa-0101), the authority

> Summarised in this skill's own words.
>
> The Baseline applies this only after a release. This skill recommends doing the
> assessment before a repository is first published as well; see
> [threat-modeling.md](../../threat-modeling.md).

- **Requires:** design documentation showing all actions and actors in the system.
  Actors include any subsystem or entity that can influence another part.
- **Meet it:** describe the components, who or what drives them, and how they interact;
  keep it current with new features and breaking changes. The system model from
  [threat-modeling.md](../../threat-modeling.md) serves as a starting point.
- **Verify:** check the description against the code (ground rule 3).
