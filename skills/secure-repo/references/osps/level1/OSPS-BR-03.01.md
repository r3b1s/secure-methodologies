# OSPS-BR-03.01

- **Control:** OSPS-BR-03, Use Encrypted Channels for Development & Release Activity (Build and Release)
- **Level:** 1+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-br-0301), the authority

> Summarised in this skill's own words.

- **Requires:** every URI the project lists as an official channel is served only over
  encrypted connections.
- **Meet it:** use HTTPS or SSH for the repository, website, documentation and any other
  official links, and fix plain `http://` links.
- **Verify:** list the official channels named in the README and documentation, and check
  each one's scheme and whether it redirects or refuses unencrypted access.
