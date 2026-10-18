# OSPS-SA-02.01

- **Control:** OSPS-SA-02, Publish External Interface Descriptions (Security Assessment)
- **Level:** 2+, after a release
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-sa-0201), the authority

> Summarised in this skill's own words.
>
> The Baseline applies this only after a release. This skill recommends doing the
> assessment before a repository is first published as well; see
> [threat-modeling.md](../../threat-modeling.md).

- **Requires:** descriptions of all external software interfaces of released assets.
- **Meet it:** document every interface users or other systems touch (command line,
  APIs, file formats, network protocols, configuration), with expected inputs and outputs.
- **Verify:** compare with the interfaces the code actually exposes.
